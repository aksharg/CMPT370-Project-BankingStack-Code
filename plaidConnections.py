import json
import os
import sys
import datetime
from dateutil.relativedelta import relativedelta

# Files
import plaidFunctions
import plaidWebServer
import encryption
import getEncryptedData
import register


# ^ Need Testing
def getSystemKey():
    with open("systemKey.key","rb") as key_file:
        key = key_file.read()
        key_file.close()
    return key

def getUserId(user_dir_path,key):
    creds_data = getEncryptedData.getEncryptedData(user_dir_path,key)
    return str(creds_data["user_id"])

# ^ Need Testing
def createAccountsFile(user_dir_path,user_creds_path):
    key = getSystemKey()
    user_creds_data = getEncryptedData.getEncryptedData(user_creds_path,key)
    accs_key = user_creds_data['secret_key'].encode()

    if not os.path.exists(user_dir_path+"\\userAccounts.json"):
        initialize_accs = {"accounts": []}
        json_init_accs = json.dumps(initialize_accs)
        encrypted_json_init_accs = encryption.encryptData(json_init_accs,accs_key)
        accs_file = register.fileCreation(user_dir_path+"\\userAccounts.json",encrypted_json_init_accs,encrypted=True)
        return str(accs_file)
    else:
        return str(user_dir_path+"\\userAccounts.json")

# ^ Need Testing
def getUserFiles(user_id):
    key = getSystemKey()
    users = getEncryptedData.getEncryptedData("users.json",key)
    for i in users['users']:
        if i['user_id'] == user_id:
            user_creds_path = i['path']+"\\userCredentials.json"
            creds_data = getEncryptedData.getEncryptedData(user_creds_path,key)
            user_accs = createAccountsFile(i['path'],user_creds_path)
            return creds_data, user_accs, "Success"
            break

    return None, None, "User Files Not Found"

# ^ Need Testing
def linkAccount(api_credentials, plaid, user_id, bank_name):
    user_creds_data, user_acc_file, message = getUserFiles(user_id)
    user_key = user_creds_data['secret_key'].encode()

    if user_creds_data == None:
        return (False, message)

    elif message == "Success":
        accounts = getEncryptedData.getEncryptedData(user_acc_file,user_key)
        link_token = plaid.getLinkToken()

        if len(accounts["accounts"]) != 0:
            for acc in accounts["accounts"]:
                if acc['bank_name'] == bank_name:
                    return (False, "You have already linked with "+bank_name+". Please select a different institute")
                    break
                    
        print("Webpage Initiated!")

        # Start webserver
        plaid_response = plaidWebServer.startServer(
            env = api_credentials['environment'],
            client_name = user_creds_data['username'],
            token = link_token,
            page_title = "Link New Account for client "+user_creds_data['username'],
            account_name = bank_name+" Bank Account",
            type = "Link")

        if 'public_token' not in plaid_response:
            return (False, "An error occured in the Plaid API connection. Public_token unavailable. Please Try Again")
        else:
            public_token = plaid_response['public_token']

            try:
                exchange_response = plaid.exchangePublicToken(public_token)
            except PlaidError as excptn:
                return (False, "An error occured in the Plaid API connection. Access_token unavailable. Please Try Again")
            else:
                access_token = exchange_response['access_token']

                accounts = getEncryptedData.getEncryptedData(user_acc_file,user_key)
                acc_modifier = accounts["accounts"]

                for account in plaid_response["accounts"]:
                    

                    new_account = {
                        'bank_name' : plaid_response["institution"]["name"],
                        'access_token' : access_token,
                        'account_id': account["id"],
                        'account_name': account["name"],
                        'account_owner': user_creds_data["username"],
                        'account_type': account["type"]
                    }
                    acc_modifier.append(new_account)
                    json_accounts = json.dumps(accounts)
                    encrypted_acc_modified = encryption.encryptData(json_accounts, user_key)
                    register.updateFile(user_acc_file,encrypted_acc_modified,encrypted=True)

                return (True, str(plaid_response["institution"]["name"])+" account has successfully been linked!")

# ^ Need Testing
def deleteAccount(api_credentials, plaid, user_id, bank_name,env):
    
    user_creds_data, user_acc_file, message = getUserFiles(user_id)
    user_key = user_creds_data['secret_key'].encode()
    access_token = None
    if user_creds_data == None:
        return (False, message)
    
    elif message == "Success":
        if env == "sandbox":
            accounts = getEncryptedData.getEncryptedData(user_acc_file,user_key)
            if len(accounts) != 0:
                for acc in accounts['accounts']:
                    if acc['bank_name'] == bank_name:
                        accounts['accounts'].remove(acc)
                    else:
                        continue
            
            modified_accounts = [name for name in accounts['accounts'] if name['bank_name'] != bank_name]
            new_accs_file_content = {"accounts": modified_accounts}
            json_modified_accounts = json.dumps(new_accs_file_content)
            encrypted_accounts = encryption.encryptData(json_modified_accounts, user_key)
            register.updateFile(user_acc_file,encrypted_accounts,encrypted=True)
            return (True, "Successfully Unlinked "+bank_name+" Accounts. Please refresh the page.")

        else:
            accounts = getEncryptedData.getEncryptedData(user_acc_file,user_key)
            if len(accounts) != 0:
                for acc in accounts['accounts']:
                    if acc['bank_name'] == bank_name:
                        access_token = acc['access_token']
                        break
                    else:
                        continue

                if access_token != None:
                    try:
                        resp = plaid.removeAccount("access_token")

                    except plaidFunctions.PlaidUnknownError:
                        for acc in accounts['accounts']:
                            if acc['bank_name'] == bank_name:
                                accounts['accounts'].remove(acc)
                        return (False, "You can't delete a non existing account")
                    else:
                        if resp["removed"] == True:
                            modified_accounts = [name for name in accounts['accounts'] if name['bank_name'] != bank_name]

                            json_modified_accounts = json.dumps(modified_accounts)
                            encrypted_accounts = encryption.encryptData(json_modified_accounts, user_key)
                            register.updateFile(user_acc_file,encrypted_accounts,encrypted=True)
                            return (True, "Account deleted successfully.")

                        else:
                            return (False, "Error Occured Try Again.")
                else:
                    return (False, "You have no connection with this Institution")

# ^ NEED Testing
def getUserAccData(plaid,user_id,bank_name):
    user_creds_data, user_acc_file, message = getUserFiles(user_id)
    user_key = user_creds_data['secret_key'].encode()

    if user_creds_data == None:
        return (False, message)

    elif message == "Success":
        accounts = getEncryptedData.getEncryptedData(user_acc_file,user_key)
    
    for acc in accounts["accounts"]:
        if acc["bank_name"] == bank_name:
            access_token = acc["access_token"]
            break

    try:
        resp = plaid.getTokenAccountInfo(access_token)
    except plaidFunctions.PlaidUnknownError:
        return (False, "Invalid Access Token.")
    else:
        return (True, resp)


# ^ NEED Testing
def getBalance(user_id,plaid,bank_name):
    user_creds_data, user_acc_file, message = getUserFiles(user_id)
    user_key = user_creds_data['secret_key'].encode()
    access_token = ""
    if user_creds_data == None:
        return (False, message)
    
    elif message == "Success":
        accounts = getEncryptedData.getEncryptedData(user_acc_file,user_key)
        if accounts["accounts"]:
            for acc in accounts["accounts"]:
                if acc["bank_name"] == bank_name:
                    access_token = acc["access_token"]
                    break
                else:
                    continue

        else:
            return (False, "You have no linked accounts. Please link an account before viewing balances.")

        try:
            balance_list = plaid.getAccountBalance(access_token)
        except plaidFunctions.PlaidUnknownError:
            return (False, "Error occured. Please try again")
        else:
            for acc in accounts["accounts"]:
                for account in balance_list:
                    
                    acc_balance = { "current_balance": account.balance_current,
                                    "available_balance": account.balance_available,
                                    "balance_limit": account.balance_limit
                                }

                    if account.account_id == acc["account_id"]:
                        acc["balance"] = acc_balance

                    json_modified_accounts = json.dumps(accounts)
                    encrypted_accounts = encryption.encryptData(json_modified_accounts, user_key)
                    register.updateFile(user_acc_file,encrypted_accounts,encrypted=True)

            return (True, "Success")

def getTransactions(user_id, plaid, start_date, end_date, account_name):

    user_creds_data, user_acc_file, message = getUserFiles(user_id)
    user_key = user_creds_data['secret_key'].encode()
    
    if user_creds_data == None:
        return (False, message)
    
    elif message == "Success":
        accounts = getEncryptedData.getEncryptedData(user_acc_file,user_key)

        for acc in accounts["accounts"]:
            if acc["account_name"] == account_name:
                access_token = acc["access_token"]
                account_id = acc["account_id"]
                break

        # print(accounts)
        print(plaid.getAccountTransactions(access_token,start_date,end_date,[account_id],status_callback=None))

        # for acc in accounts["accounts"]:
        #     print(acc)
        #     if acc["account_name"] == account_name:
        #         access_token = acc["access_token"]
        #         account_id = acc["account_id"]
        #         break

        


        # with open(user_acc_file) as acc_file:
        #     acc_data = json.load(acc_file)

        # acc_data["accounts"][user_choice-1]["Transactions"] = transactions_list_jsonified

        # with open(user_acc_file, "w") as acc_file:
        #     json.dump(acc_data,acc_file)
        #     acc_file.close()
        
        # with open(user_acc_file) as acc_file:
        #     acc_data = json.load(acc_file)
        
        # print("===============================================================================================================================|")
        # print("Account: "+account_name)
        # print("Date/Time:",datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
        # print("Total Transactions:",len(acc_data["accounts"][user_choice-1]["Transactions"]),"from",start_date.strftime("%d/%m/%Y"),"to",end_date.strftime("%d/%m/%Y"))
        # print("-------------------------------------------------------------------------------------------------------------------------------|")
        # for transaction in acc_data["accounts"][user_choice-1]["Transactions"]:
        #     print("Transaction Date:",transaction['date'])
        #     print("Merchant Name:",transaction['merchant_name'])
        #     print("Description:",transaction['description'])
        #     if transaction["status_pending"] == False:
        #         print("Transaction Status:","Processed Successfully")
        #     elif transaction["status_pending"] == True:
        #         print("Transaction Status:","Processing Pending")
        #     print("Transaction Categories: ",transaction['category'])
        #     print("Transaction Amount: $"+str(transaction["amount"]))
        #     print("-------------------------------------------------------------------------------------------------------------------------------|")
        # print("===============================================================================================================================|")
        # return True

def getInstitutions(plaid, supported_institutions):
    healthy_status = []
    item_login = False
    transactions_status = False

    for institution in supported_institutions:
        ret = plaid.getInstitution(institution)
        if ret.institution_item_login_status == "HEALTHY":
            item_login = True
            if ret.transactions_status == "HEALTHY":
                transactions_status = True
            else:
                transactions_status = False
        else:
            item_login = False
            if ret.transactions_status == "HEALTHY":
                transactions_status = True
            else:
                transactions_status = False
        healthy_status.append([institution,item_login,transactions_status])

    # print(healthy_status)
    return healthy_status


'''
    sdfsdf
    dsfsdf
    def balanceTransactionsPrintHandler(user_acc_file,request_source):
        count = 1
        with open(user_acc_file,"r") as acc_file:
            list_of_accounts = json.load(acc_file)
            acc_file.close()
        print("===============================================================================================================================|")

        if (len(list_of_accounts['accounts']) == 0) and (request_source == "getBalance"):
            print("There are no linked accounts. Please use <link_account> to link a bank account")
            return 0,0,0
        elif (len(list_of_accounts['accounts']) == 0) and (request_source == "getTransactions"):
            return 0,0,0,0,0,0
        else:
            print("Accounts List:")
            for acc in list_of_accounts['accounts']:
                print(str(count)+". "+acc['account_name'])
                count+=1
            print("===============================================================================================================================|")

            if request_source == "getBalance":
                print("-------------------------------------------------------------------------------------------------------------------------------|")
                print("Please input the number corresponding to the account for which you wish to view the balance.                                   |")
                print("-------------------------------------------------------------------------------------------------------------------------------|")

                user_choice = input("Pick an Account: ")

                account_name = list_of_accounts['accounts'][int(user_choice)-1]['account_name']
                access_token = list_of_accounts['accounts'][int(user_choice)-1]['access_token']

                return int(user_choice),account_name, access_token

            if request_source == "getTransactions":
                user_choice = input("Pick an Account: ")
                print("\n")
                print("===============================================================================================================================|")
                print("Time Range Presets: You can choose one of the following time range presets to view transactions.                               |")
                print("1. One Week                                                                                                                    |")
                print("2. One Month                                                                                                                   |")
                print("3. Three Months                                                                                                                |")
                print("4. Six Months                                                                                                                  |")
                print("===============================================================================================================================|")
                print("-------------------------------------------------------------------------------------------------------------------------------|")
                print("Please input the number corresponding to the account for which you wish to view the transactions.                              |")
                print("                                                                                                                               |")
                print("Note: You can only view 24 months of transaction data. Additionally, a maximum of 500 transactions will be shown for any time  |")
                print("      range you input. Ability to view more than 500 transactions at a time will be available soon! Ability to view custom     |")
                print("      time ranges coming soon.                                                                                                 |")
                print("-------------------------------------------------------------------------------------------------------------------------------|")

                time_range = input("Pick a time range: ")

                if time_range == "1":
                    start_date = (datetime.datetime.now() - datetime.timedelta(days=7)).date()
                    end_date = datetime.datetime.now().date()
                elif time_range == "2":
                    start_date = datetime.datetime.now().date() + relativedelta(months=-1)
                    end_date = datetime.datetime.now().date()
                elif time_range == "3":
                    start_date = datetime.datetime.now().date() + relativedelta(months=-3)
                    end_date = datetime.datetime.now().date()
                elif time_range == "4":
                    start_date = datetime.datetime.now().date() + relativedelta(months=-6)
                    end_date = datetime.datetime.now().date()
                else:
                    print("default time range: 1 Day")
                    start_date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
                    end_date = datetime.datetime.now().date()

                account_name = list_of_accounts['accounts'][int(user_choice)-1]['account_name']
                access_token = list_of_accounts['accounts'][int(user_choice)-1]['access_token']
                account_id   = list_of_accounts['accounts'][int(user_choice)-1]['account_id']

                return int(user_choice), account_id, account_name, access_token, start_date, end_date
'''
'''


    def getUserCredsData():
        pass

    

    def updateAccount(api_credentials, plaid, account_name):
        pass

    

    



    # def encryptData(data, key):
    #     cipher_suite = Fernet(key)
    #     cipher_text = cipher_suite.encrypt(data.encode())
    #     return cipher_text

    # def decryptData(encrypted_data,key):
    #     cipher_suite = Fernet(key)
    #     data = cipher_suite.decrypt(encrypted_data)
    #     return data

    def checkInstitutions():
        institutions_result = getInstitutions(plaid, supported_institutions)

        if institutions_result == True:
            print("All bank features are HEALTHY.")
        else:
            print("Some of the bank features might be unavailable at this moment")

    def helpPrints():
        print("-------------------------------------------------------------------------------------------------------------------------------|")
        print("===============================================================================================================================|")
        print("Supported Commands:                                                                                                            |")
        print("<help>: Prints a list of all possible commands and thier respective use cases                                                  |")
        print("<link_account>: Will prompt the user to enter what they would like to name the account.                                        |")
        print("                If that account name is already in use the user will be requested to try again                                 |")
        print("                                                                                                                               |")
        print("<update_account>: If account credentials have expired, use this command to update the credentials                              |")
        print("<check_balance>: Will prompt user to select an account for which they wish to view the balance.                                |")
        print("<view_transactions>: Will prompt the user to select an account and enter a time range for which they wish to view transactions |")
        print("<add_transaction_note>: Coming Soom!                                                                                           |")

    def linkAccountPrints(api_credentials,plaid,user_id):
        user_bank = input("Supported Banks: ['RBC Royal Bank', 'CIBC', 'BMO Bank of Montreal', 'TD Canada Trust']\nPlease select a bank: ")
        linkAccount(api_credentials,plaid,user_id,user_bank)

    def successfullLinkPrint():
        print("Bank account successfully Linked!")
'''

# ^ NEED Testing
def apiCredentials(env):
    with open("systemKey.key", "r") as key_file:
        key = key_file.read().encode()
        key_file.close()

    # decrypted_credentials = encryption.decryptData(,key)
    decrypted_credentials = getEncryptedData.getEncryptedData("apiCredentials.json",key)
    api_credentials = json.loads(decrypted_credentials)

    if env == "sandbox":
        api_credentials['environment'] = "sandbox"
        plaid = plaidFunctions.plaidAPI(api_credentials['client_id'],api_credentials['sandbox_secret'],api_credentials['environment'])
    if env == "development":
        api_credentials['environment'] = "development"
        plaid = plaidFunctions.plaidAPI(api_credentials['client_id'],api_credentials['secret'],api_credentials['environment'])

    return api_credentials,plaid

# # ! NEED Work
# def main(user_id, env):
#     print("Banking Stack Command Line Interface For Plaid Connection")


#     supported_institutions = ["RBC Royal Bank", "CIBC", "BMO Bank of Montreal", "TD Canada Trust"]
#     api_credentials,plaid = apiCredentials(env)

#     print(supported_institutions)
#     bank_name = input("Choose Bank: ")


#     start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).date()
#     end_date = datetime.datetime.now().date()

#     print(getBalance(user_id,plaid,"CIBC"))
#     getTransactions(
#         user_id=user_id,
#         plaid=plaid,
#         start_date=start_date,
#         end_date=end_date,
        # account_name="Plaid Checking")



'''
    # while True:
    #     user_input = input("\nPlease enter a command: ")

    #     if user_input == "help":
    #         helpPrints()
    #         continue

    #     elif user_input == "link_account":
    #         status = linkAccountPrints(api_credentials,plaid,user_id)
    #         if status:
    #             successfullLinkPrint()
        
    #     elif user_input == "check_balance":
    #         status = getBalance(user_id,plaid)
    #         if not status:
    #             print("Try Again")
    #             print("\n")
    #             helpPrints()

    #     elif user_input == "view_transactions":
    #         status = getTransactions(user_id,plaid)
    #         if not status:
    #             print("Try Again")
    #             print("\n")
    #             helpPrints()

    #     elif user_input == "exit":
    #         sys.exit(0)

    #     else:
    #         print("Try Again")
    #         print("\n")
    #         helpPrints()
'''

# main("13598905","sandbox")
