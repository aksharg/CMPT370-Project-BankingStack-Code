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
import globals

def getSystemKey():
    return globals.general_key

def getUserId(user_dir_path,key):
    creds_data = getEncryptedData.getEncryptedData(user_dir_path,key)
    return str(creds_data["user_id"])

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
                print('ysdsd')
                access_token = acc["access_token"]
                account_id = acc["account_id"]
                acc["transactions"] = []
                break

        encrypted_acc = encryption.encryptData(json.dumps(accounts),user_key)
        register.updateFile(user_acc_file,encrypted_acc, True)

        transaction_objects = plaid.getAccountTransactions(access_token,start_date,end_date,[account_id],status_callback=None)
        acc_idx = 0
        accounts_two = getEncryptedData.getEncryptedData(user_acc_file,user_key)
        for acc in accounts_two["accounts"]:
                for trans in transaction_objects:
                    if acc["account_id"] == trans.account_id:
                        acc_idx = accounts_two["accounts"].index(acc)
                        trans_dict = {"transaction_date":trans.date,
                                        "transaction_id":trans.transaction_id,
                                        "merchant_name": trans.merchant_name,
                                        "amount": trans.amount,
                                        "category": trans.category,
                                        "description": trans.description}
                        acc["transactions"].append(trans_dict)
            
        encrypted_acc_two = encryption.encryptData(json.dumps(accounts_two),user_key)
        register.updateFile(user_acc_file,encrypted_acc_two, True)
        print(accounts_two["accounts"][acc_idx]["transactions"])
        return accounts_two["accounts"][acc_idx]["transactions"]

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

    return healthy_status

def apiCredentials(env):
    key =getSystemKey()

    decrypted_credentials = getEncryptedData.getEncryptedData("apiCredentials.json",key)
    api_credentials = json.loads(decrypted_credentials)

    if env == "sandbox":
        api_credentials['environment'] = "sandbox"
        plaid = plaidFunctions.plaidAPI(api_credentials['client_id'],api_credentials['sandbox_secret'],api_credentials['environment'])
    if env == "development":
        api_credentials['environment'] = "development"
        plaid = plaidFunctions.plaidAPI(api_credentials['client_id'],api_credentials['secret'],api_credentials['environment'])

    return api_credentials,plaid
