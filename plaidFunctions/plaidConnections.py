import json
import os
import sys
from cryptography.fernet import Fernet, InvalidToken

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


def linkAccount(api_credentials, plaid, user_id, bank_name):
    # Get user Data. If user data is none then user doesnt exist
    # get user accounts. If an account exists with that name return a message.
    user_creds_file, user_acc_file = getUserFiles(user_id)
    account_name = "aa"
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
        # for acc in accounts['accounts']:
        #     if acc['bank_name'] == bank_name:
        #         print("You have already established a connection with this Banks.\n"+
        #         "Please select a new Bank or choose a command which allows you to access this bank account.")
        #         return False
        
        # account doesnt exist.
        link_token = plaid.getLinkToken()

        # Start webserver
        plaid_response = plaidWebServer.startServer(
            env = api_credentials['environment'],
            client_name = user_creds['name'],
            token = link_token,
            page_title = "Link New Account",
            account_name = "link",
            type = "Link")

        # print(plaid_response)
        if 'public_token' not in plaid_response:
            print("*** ATTENTION ***")
            print("An error occured in the Plaid API connection. No public_token was returned")
            print("Try again with command:")
            print("--link-account '%s' % account_name")
            sys.exit(1)

        public_token = plaid_response['public_token']
        print("")
        print(f"Plaid public_token: {public_token}."
            "Exchanging for access token.")
    
        # Obtain access_token
        try:
            exchange_response = plaid.exchangePublicToken(public_token)
        except PlaidError as excptn:
            print("*** ATTENTION ***")
            print("An error occured when exchanging Plaid public_token for access_token")
            print("Error:\n")
            print(excptn)
            print("--------------------------------------------------------------------")
            print("Try again with command:")
            print("--link-account '%s' % account_name")
            sys.exit(1)
        
        # Get Access_token
        access_token = exchange_response['access_token']
        print("Access token received: %s" % access_token)
        print("")

        # access_token = "access-development-9a0187e5-d5f1-43a3-88b3-09d14f4858ad"
        balance_json = getBalance(plaid,access_token)

        # print(balj)
        # Store the access_token
        accounts_file = open(user_acc_file,"r")
        accounts = json.load(accounts_file)



        for account in balance_json:
            new_account = {
                'account_id': account.account_id,
                'account_name': account.account_name,
                'account_owner': user_creds['name'],
                'account_type': account.account_type,
                'balances': {'balance_current':account.balance_current,'balance_available':account.balance_available,'balance_limit':account.balance_limit}
            }
            print(new_account)

        # print(accounts)
    return 'yes'


def updateAccount(api_credentials, plaid, account_name):
    pass

def getTransactions(access_token):
    pass

def getBalance(plaid,access_token):
    balance = plaid.getAccountBalance(access_token)
    return balance

def getInstitutions(plaid, supported_institutions):
    healthy_status = []

    for institution in supported_institutions:
        ret = plaid.getInstitution(institution)
        if ret.institution_item_login_status == ret.transactions_status == "HEALTHY":
            healthy_status.append("HEALTHY")
        else:
            healthy_status.append("UNHEALTHY")

    return all(x == healthy_status[0] for x in healthy_status)

def apiCredentials():
    with open("plaidFunctions/apiCredentials.json") as json_file:
        json_api_credentials = json_file.read()
        json_file.close()
    
    print(json_api_credentials)

    # if json_api_credentials['environment'] == "sandbox":
    #     plaid = plaidFunctions.plaidAPI(json_api_credentials['client_id'],json_api_credentials['sandbox_secret'],json_api_credentials['environment'])
    # else:
    #     plaid = plaidFunctions.plaidAPI(json_api_credentials['client_id'],json_api_credentials['secret'],json_api_credentials['environment'])
    # return json_api_credentials,plaid

def checkInstitutions():
    institutions_result = getInstitutions(plaid, supported_institutions)

    if institutions_result == True:
        print("All bank features are HEALTHY.")
    else:
        print("Some of the bank features might be unavailable at this moment")

def help():
    print("Supported Commands:")
    print("- help: Prints a list of all possible commands and thier respective use cases")
    print("- link_account: Will prompt the user to enter what they would like to name the account.")
    print("                If that account name is already in use the user will be requested to try again")
    print("- check_balance: Will prompt user to select an account for which they wish to view the balance.")
    print("- view transactions: Will prompt the user to select an account and enter a time range for which they wish to view transactions")


def main(user_id):
    print("Banking Stack Command Line Interface For Plaid Connection")
    print("-----------------------------------------------------------------------")
    help()

    supported_institutions = ["RBC", "CIBC", "BMO", "TD Canada"]
    json_api_credentials = apiCredentials()

    # print("\n")


    # while True:
    #     user_input = input("\nPlease enter a command: ")

    #     if user_input == "help":
    #         help()
    #         continue
    #     elif user_input == "link_account":
    #         user_bank = input("Supported Banks: ['RBC', 'CIBC', 'BMO', 'TD Canada']\nPlease select a bank: ")
    #         linkAccount(json_api_credentials, plaid, user_id, user_bank)
    #     elif user_input == "exit":
    #         sys.exit(0)

    # user_choice = input("Please en")

    # plaid = apiCredentials()
    # checkInstitutions()
    

    # account_name = "RBC_checking"


    # linkAccount(json_api_credentials, plaid, user_id, account_name)
    
        

    # getBalance(plaid,'access-development-9a0187e5-d5f1-43a3-88b3-09d14f4858ad')


main("1")