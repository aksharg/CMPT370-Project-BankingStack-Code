import json
import os
import sys
from cryptography.fernet import Fernet, InvalidToken

import plaidFunctions
import plaidWebServer


# * DONE
# ! NOT TESTED
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

# ^ INCOMPLETE
# ! NOT TESTED
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

        if len(accounts['accounts']) != 0:
            for acc in accounts['accounts']:
                if acc['bank_name'] == bank_name:
                    print("You have already established a connection with this Bank.\n"+
                    "Please select a new Bank or choose a command which allows you to access this bank account.")
                    return False

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

        # print(plaid_response)
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

# ^ INCOMPLETE
# ! NOT TESTED
def updateAccount(api_credentials, plaid, account_name):
    pass

# ^ INCOMPLETE
# ! NOT TESTED
def getTransactions(access_token):
    pass




# * DONE
# ! NOT TESTED
def getBalance(plaid):
    user_creds_file, user_acc_file = getUserFiles(user_id)

    with open(user_acc_file,"r") as acc_file:
        list_of_accounts = json.load(accounts_file)
        acc_file.close()

    balance = plaid.getAccountBalance(access_token)
    return balance

# * DONE
# ! NOT TESTED
def getInstitutions(plaid, supported_institutions):
    healthy_status = []

    for institution in supported_institutions:
        ret = plaid.getInstitution(institution)
        if ret.institution_item_login_status == ret.transactions_status == "HEALTHY":
            healthy_status.append("HEALTHY")
        else:
            healthy_status.append("UNHEALTHY")

    return all(x == healthy_status[0] for x in healthy_status)

# * DONE
# * TESTED
def encryptData(data, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text

# * DONE
# * TESTED
def decryptData(encrypted_data,key):
    cipher_suite = Fernet(key)
    data = cipher_suite.decrypt(encrypted_data)
    return data

# * DONE
# ! NOT TESTED
def apiCredentials():
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

    api_credentials['environment'] = "sandbox"

    if api_credentials['environment'] == "sandbox":
        plaid = plaidFunctions.plaidAPI(api_credentials['client_id'],api_credentials['sandbox_secret'],api_credentials['environment'])
    else:
        plaid = plaidFunctions.plaidAPI(api_credentials['client_id'],api_credentials['secret'],api_credentials['environment'])

    return api_credentials,plaid

# * DONE
# ! NOT TESTED
def checkInstitutions():
    institutions_result = getInstitutions(plaid, supported_institutions)

    if institutions_result == True:
        print("All bank features are HEALTHY.")
    else:
        print("Some of the bank features might be unavailable at this moment")

# * DONE
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

def linkAccountPrints(api_credentials,plaid,user_id):
    user_bank = input("Supported Banks: ['RBC Royal Bank', 'CIBC', 'BMO Bank of Montreal', 'TD Canada Trust']\nPlease select a bank: ")
    linkAccount(api_credentials,plaid,user_id,user_bank)

def successfullLinkPrint():
    print("Bank account successfully Linked!")

# ^ INCOMPLETE
# ! NOT TESTED
def main(user_id):
    print("===============================================================================================================================|")
    print("-------------------------------------------------------------------------------------------------------------------------------|")
    print("Banking Stack Command Line Interface For Plaid Connection                                                                      |")
    helpPrints()

    supported_institutions = ["RBC Royal Bank", "CIBC", "BMO Bank of Montreal", "TD Canada Trust"]
    api_credentials,plaid = apiCredentials()

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
            pass

        elif user_input == "exit":
            sys.exit(0)


main("1")