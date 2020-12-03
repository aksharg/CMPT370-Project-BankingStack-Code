import json
import os
import sys
# from cryptography.fernet import Fernet, InvalidToken
import datetime
from dateutil.relativedelta import relativedelta
import plaidFunctions
import plaidWebServer

def getUserFiles(user_id):
    with open(r'plaidFunctions\users.json','r') as user_file:
        users = json.load(user_file)
        user_file.close()
        for i in users['users']:
            if i['user_id'] == user_id:
                return i['credentials_file'],i['accounts_file']
        return None,None

def getUserAccData():
    pass

def getUserCredsData():
    pass

def linkAccount(api_credentials, plaid, user_id, bank_name):
    user_creds_file, user_acc_file = getUserFiles(user_id)

    if user_creds_file == None:
        print("User Doesn't exist")
        print("Re-run with a different name")
        return False

    else:
        creds_file = open(user_creds_file,"r")
        user_creds = json.load(creds_file)
        creds_file.close()

        accounts_file = open(user_acc_file,"r")
        accounts = json.load(accounts_file)
        accounts_file.close()

        # if len(accounts['accounts']) != 0:
        #     for acc in accounts['accounts']:
        #         if acc['bank_name'] == bank_name:
        #             print("You have already established a connection with this Bank.\n"+
        #             "Please select a new Bank or choose a command which allows you to access this bank account.")
        #             return False

        link_token = plaid.getLinkToken()

        print("Please follow the instructions outlined on the newly opened Webpage to connect your bank account.")

        # Start webserver
        plaid_response = plaidWebServer.startServer(
            env = api_credentials['environment'],
            client_name = user_creds['name'],
            token = link_token,
            page_title = "Link New Account for client "+user_creds['name'],
            account_name = bank_name+" Bank Account",
            type = "Link")

        if 'public_token' not in plaid_response:
            print("*** ATTENTION ***")
            print("An error occured in the Plaid API connection. No public_token was returned")
            print("Try again with command: link_account")
            sys.exit(1)

        public_token = plaid_response['public_token']

        try:
            exchange_response = plaid.exchangePublicToken(public_token)
        except PlaidError as excptn:
            print("*** ATTENTION ***")
            print("An error occured when exchanging Plaid public_token for access_token")
            print("Error:\n")
            print(excptn)
            print("--------------------------------------------------------------------")
            print("Try again with command: link_account")
            sys.exit(1)
        
        access_token = exchange_response['access_token']
        print("Access token received: %s" % access_token)
        print("\nThis token will be used by all functions that talk with Plaid.")

        '''
        access_token1 = access-development-9a0187e5-d5f1-43a3-88b3-09d14f4858ad
        access_token2 = access-development-892c3ac3-5b73-4839-91a4-d36604d829bf
        access_token3 = access-development-9615bef6-c9be-4589-b888-dcd2ec13b25b
        '''

        with open(user_acc_file) as accounts_file:
            accounts = json.load(accounts_file)
            acc_modifier = accounts["accounts"]

            for account in plaid_response["accounts"]:
                new_account = {
                    'bank_name' : plaid_response["institution"]["name"],
                    'access_token' : access_token,
                    'account_id': account["id"],
                    'account_name': account["name"],
                    'account_owner': user_creds['name'],
                    'account_type': account["type"]
                }
                acc_modifier.append(new_account)

                with open(user_acc_file,"w") as f: 
                    json.dump(accounts, f, indent=4)
                    f.close()

            accounts_file.close()

    return True

def updateAccount(api_credentials, plaid, account_name):
    pass

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

def getTransactions(user_id, plaid):
    user_creds_file, user_acc_file = getUserFiles(user_id)
    user_choice, account_id, account_name, access_token, start_date, end_date = balanceTransactionsPrintHandler(user_acc_file,"getTransactions")

    if user_choice == account_name == access_token == start_date == end_date == 0:
        return False
    else:
        transactions_list_raw = plaid.getAccountTransactions(access_token, start_date, end_date, [account_id])
        transactions_list_jsonified = []

        for transaction in transactions_list_raw:
            transaction_jsonified = json.loads(transaction.to_json())
            del transaction_jsonified['raw_data']
            transactions_list_jsonified.append(transaction_jsonified)

        with open(user_acc_file) as acc_file:
            acc_data = json.load(acc_file)

        acc_data["accounts"][user_choice-1]["Transactions"] = transactions_list_jsonified

        with open(user_acc_file, "w") as acc_file:
            json.dump(acc_data,acc_file)
            acc_file.close()
        
        with open(user_acc_file) as acc_file:
            acc_data = json.load(acc_file)
        
        print("===============================================================================================================================|")
        print("Account: "+account_name)
        print("Date/Time:",datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
        print("Total Transactions:",len(acc_data["accounts"][user_choice-1]["Transactions"]),"from",start_date.strftime("%d/%m/%Y"),"to",end_date.strftime("%d/%m/%Y"))
        print("-------------------------------------------------------------------------------------------------------------------------------|")
        for transaction in acc_data["accounts"][user_choice-1]["Transactions"]:
            print("Transaction Date:",transaction['date'])
            print("Merchant Name:",transaction['merchant_name'])
            print("Description:",transaction['description'])
            if transaction["status_pending"] == False:
                print("Transaction Status:","Processed Successfully")
            elif transaction["status_pending"] == True:
                print("Transaction Status:","Processing Pending")
            print("Transaction Categories: ",transaction['category'])
            print("Transaction Amount: $"+str(transaction["amount"]))
            print("-------------------------------------------------------------------------------------------------------------------------------|")
        print("===============================================================================================================================|")
        return True

def getBalance(user_id,plaid):
    user_creds_file, user_acc_file = getUserFiles(user_id)
    user_choice, account_name, access_token = balanceTransactionsPrintHandler(user_acc_file,"getBalance")
    print("Checking balance for",account_name)

    if user_choice == account_name == access_token == 0:
        return False
    else:
        balance_list = plaid.getAccountBalance(access_token)

        for account in balance_list:
            if account.account_name == account_name:
                acc_balance = {"current_balance": account.balance_current,
                            "available_balance": account.balance_available,
                            "balance_limit": account.balance_limit}

                # print(acc_balance)
                # print(type(acc_balance))
                with open(user_acc_file) as acc_file:
                    acc_data = json.load(acc_file)
                
                acc_data["accounts"][user_choice-1]["Balance"] = acc_balance

                with open(user_acc_file, "w") as acc_file:
                    json.dump(acc_data,acc_file, indent=4)
                    acc_file.close()

                with open(user_acc_file) as acc_file:
                    acc_data = json.load(acc_file)
                    acc_file.close()

                print("===============================================================================================================================|")
                print("Account: "+account_name)
                print("Date/Time:",datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))
                print("Current Balance:",acc_data["accounts"][user_choice-1]["Balance"]["current_balance"])
                print("Available Balance:",acc_data["accounts"][user_choice-1]["Balance"]["available_balance"])
                print("Balance Limit:",acc_data["accounts"][user_choice-1]["Balance"]["balance_limit"])
                print("===============================================================================================================================|")
        return True

def getInstitutions(plaid, supported_institutions):
    healthy_status = []

    for institution in supported_institutions:
        ret = plaid.getInstitution(institution)
        if ret.institution_item_login_status == ret.transactions_status == "HEALTHY":
            healthy_status.append("HEALTHY")
        else:
            healthy_status.append("UNHEALTHY")

    return all(x == healthy_status[0] for x in healthy_status)

def encryptData(data, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text

def decryptData(encrypted_data,key):
    cipher_suite = Fernet(key)
    data = cipher_suite.decrypt(encrypted_data)
    return data

def apiCredentials(env):
    '''
    Steps to decrypt api credentials
    1. Obtain key from systemKey.key. Encode it to conver it to bytes
    2. Open apiCredentials.json file which contains encrypted data and read it.
    3. encode the encrypted data obtained from apiCredentials.json
    4. use json.loads to convert string to dict object so you can use it as a json.
    '''
    with open("plaidFunctions/systemKey.key", "r") as key_file:
        key = key_file.read().encode()
        key_file.close()

    with open("plaidFunctions/apiCredentials.json") as json_file:
        json_api_credentials = json_file.read()
        json_file.close()

    decrypted_credentials = decryptData(json_api_credentials.encode(),key)
    api_credentials = json.loads(decrypted_credentials)

    if env == "sandbox":
        api_credentials['environment'] = "sandbox"
        plaid = plaidFunctions.plaidAPI(api_credentials['client_id'],api_credentials['sandbox_secret'],api_credentials['environment'])
    if env == "development":
        api_credentials['environment'] = "development"
        plaid = plaidFunctions.plaidAPI(api_credentials['client_id'],api_credentials['secret'],api_credentials['environment'])


    return api_credentials,plaid

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

def main(user_id, env):
    print("===============================================================================================================================|")
    print("-------------------------------------------------------------------------------------------------------------------------------|")
    print("Banking Stack Command Line Interface For Plaid Connection                                                                      |")
    helpPrints()

    supported_institutions = ["RBC Royal Bank", "CIBC", "BMO Bank of Montreal", "TD Canada Trust"]
    api_credentials,plaid = apiCredentials(env)

    while True:
        user_input = input("\nPlease enter a command: ")

        if user_input == "help":
            helpPrints()
            continue

        elif user_input == "link_account":
            status = linkAccountPrints(api_credentials,plaid,user_id)
            if status:
                successfullLinkPrint()
        
        elif user_input == "check_balance":
            status = getBalance(user_id,plaid)
            if not status:
                print("Try Again")
                print("\n")
                helpPrints()

        elif user_input == "view_transactions":
            status = getTransactions(user_id,plaid)
            if not status:
                print("Try Again")
                print("\n")
                helpPrints()

        elif user_input == "exit":
            sys.exit(0)

        else:
            print("Try Again")
            print("\n")
            helpPrints()

# main("1","development")
main("1","sandbox")
