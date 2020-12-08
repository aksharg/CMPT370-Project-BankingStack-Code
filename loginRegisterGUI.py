from appJar import gui
from register import register
from login import login
import datetime

import globals
import plaidConnections
import getEncryptedData

app = gui("Banking Stack","350x300")

def loginPress():
    app.setTransparency(0)
    app.startSubWindow("Login",modal=True)
    app.setPadding([5,0])
    app.hideTitleBar()
    app.addLabel("spacer", " ")
    app.addLabel("userLab", "Username:", 1, 0)
    app.addEntry("userEnt", 1, 1)
    app.addLabel("passLab", "Password:", 2, 0)
    app.addEntry("passEnt", 2, 1)
    app.addButtons(["Submit","Cancel"], loginButton,colspan=2)
    app.stopSubWindow()
    app.showSubWindow("Login")
    print("login pressed")
  
def registerPress():
    app.setTransparency(0)
    app.startSubWindow("Register",modal=True)
    app.setPadding([5,0])
    app.hideTitleBar()
    app.addLabel("spacer", " ")
    app.addLabel("nameLab", "Name:", 2, 0)
    app.addEntry("userNam", 2, 1)
    app.addLabel("userLab", "Username:", 3, 0)
    app.addEntry("userEnt", 3, 1)
    app.addLabel("mailLab", "Email:", 4, 0)
    app.addEntry("userMail", 4, 1)
    app.addLabel("passLab", "Password:", 5, 0)
    app.addEntry("passEnt", 5, 1)
    app.addLabel("spacer2", " ")
    app.addButtons(["Submit","Cancel"], registerButton,colspan=2)
    app.stopSubWindow()
    app.showSubWindow("Register")
    print("register pressed")
  
def loginButton(btn):
    if btn == "Submit":
        exit_tuple = login(app.getEntry("userEnt"),app.getEntry("passEnt"))
        if exit_tuple[0] == False:
            app.errorBox("Invalid Input",exit_tuple[1])
        else:
            globals.loggedIn = exit_tuple[0]
            globals.credentialPath = exit_tuple[1]
            app.destroySubWindow("Login")
            app.setSize("1500x850")
            app.setLocation("CENTER")
            app.raiseFrame("WELCOME")
            app.showToolbar()
            app.setTransparency(100)
        print("login submit pressed")

    if btn == "Cancel":
        print("login cancel pressed")
        app.destroyAllSubWindows()
        app.setTransparency(100)

def registerButton(btn):
    if btn == "Submit":
        exit_tuple = register(app.getEntry("userEnt"),app.getEntry("passEnt"),app.getEntry("userMail"))
        if exit_tuple[0] == False:
            app.errorBox("Invalid Input",exit_tuple[1])
        else:
            app.destroySubWindow("Register")
            app.setTransparency(100)
        print("register submit pressed")

    if btn == "Cancel":
        print("register cancel pressed")
        app.destroySubWindow("Register")
        app.setTransparency(100)

def exitApplication():
    app.hideToolbar()
    app.setSize("350x300")
    app.raiseFrame("test1")
    globals.credentialPath = ""
    globals.loggedIn = False

def exitPress():
    app.stop()

def welcome():
    app.removeFrame("WELCOME")
    app.startFrame("WELCOME",row=0,column=0,rowspan=7,colspan=7)
    app.setSticky("")

    sys_key = plaidConnections.getSystemKey()
    user_id = plaidConnections.getUserId(globals.credentialPath,sys_key)
    user_creds_data, user_accs_file, message = plaidConnections.getUserFiles(user_id)
    
    app.addImage("bank2","bankingstack.gif")

    app.addLabel("user_info","Username: "+str(user_creds_data['username'])+" | "+
                "Account ID: "+str(user_creds_data['user_id'])+" | "+
                "Account Created: "+str(user_creds_data['creation_date'])[0:10])

    app.addLabel("instructions","Instructions:\n"+
    "- To access Banking features, click on the 2nd icon in the toolbar.\n"+
    "- To access Financial Plan features, click on the 3rd icon in the toolbar.\n"+
    "- To access Subscriptions tracker, click on the 4th icon in the toolbar.\n"+
    "- The 5th icon is to logout of the system\n"+
    "- To see the instructions page again, click on the home icon.")

    app.stopFrame()
    app.raiseFrame("WELCOME")

def closeAccountSubWindow(btn):
    # print(btn)
    if btn == "Back":
        print("Going back to main accounts page")
        print(globals.balanceBtn)
        app.destroySubWindow(str(globals.balanceBtn[5:9])+"Account Balance")
        app.setTransparency(100)

def unlinkAccount(api_credentials,plaid,user_id,bank_name):
    status, message = plaidConnections.deleteAccount(api_credentials,plaid,user_id,bank_name,"sandbox")
    if status == False:
        app.errorBox(bank_name+" balance Error",message)
    else:
        app.infoBox("Unlink"+bank_name+" Account",message)

def obtainBalance(btn,user_id,plaid,bank_name,user_accs_file,user_key):
    globals.balanceBtn = btn
    status, message = plaidConnections.getBalance(user_id,plaid,bank_name)
    if status == False:
        app.errorBox(bank_name+" balance Error",message)
    else:
        bank_accounts = []
        app.startSubWindow(str(btn[5:9])+"Account Balance",modal=True)
        app.setSize("1000x700")
        app.setPadding([5,5])
        app.hideTitleBar()
        accounts = getEncryptedData.getEncryptedData(user_accs_file,user_key)

        for account in accounts["accounts"]:
            if account["bank_name"] == bank_name:
                bank_accounts.append(account)

        first_bank_accounts = bank_accounts[:(len(bank_accounts)//2)]
        second_bank_accounts = bank_accounts[(len(bank_accounts)//2):]

        first_count = 0
        for account in first_bank_accounts:
            app.startLabelFrame(bank_name+" "+account["account_name"],row=first_count+1,column=0)
            app.setPadding([5,0])
            app.setSticky("new")
            app.addLabel(bank_name+"balance"+str(first_count),"Account Type: "+str(account["account_type"]))
            app.addLabel(bank_name+"current_balance"+str(first_count),"Current Balance: $"+str(account["balance"]["current_balance"]))
            if account["balance"]["available_balance"] != None:
                app.addLabel(bank_name+"available_balance"+str(first_count),"Available Balance: $"+str(account["balance"]["available_balance"]))
            app.setSticky("new")
            if account["balance"]["balance_limit"] != None:
                app.addLabel(bank_name+"balance_limit"+str(first_count),"Balance Limit: $"+str(account["balance"]["balance_limit"]))
            first_count += 1
            app.stopLabelFrame()
        
        second_count = 0
        for account in second_bank_accounts:
            app.startLabelFrame(bank_name+" "+account["account_name"],row=second_count+1,column=1)
            app.setPadding([5,0])
            app.setSticky("new")
            app.addLabel(bank_name+"balance_second"+str(second_count),"Account Type: "+str(account["account_type"]))
            app.addLabel(bank_name+"current_balance_second"+str(second_count),"Current Balance: $"+str(account["balance"]["current_balance"]))
            if account["balance"]["available_balance"] != None:
                app.addLabel(bank_name+"available_balance_second"+str(second_count),"Available Balance: $"+str(account["balance"]["available_balance"]))
            app.setSticky("new")
            if account["balance"]["balance_limit"] != None:
                app.addLabel(bank_name+"balance_limit_second"+str(second_count),"Balance Limit: $"+str(account["balance"]["balance_limit"]))
            second_count += 1
            app.stopLabelFrame()

        app.addButton("Back", closeAccountSubWindow,column=2,rowspan=len(first_bank_accounts))
        app.stopSubWindow()
        app.setTransparency(0)
        app.showSubWindow(str(btn[5:9])+"Account Balance")

def obtainTransactions(start_date,end_date,account_name,bank_name):
    if end_date == None or start_date == None:
        app.errorBox("Transaction Date Error","Please select a date range to view transactions.")
        app.hideSubWindow(bank_name+" Transaction Settings")
        app.setTransparency(100)

    elif end_date < start_date:
        app.errorBox("Transaction Date Error","End date must not be a date occuring before start date.")
        app.hideSubWindow(bank_name+" Transaction Settings")
        app.setTransparency(100)

    else:
        transactions = plaidConnections.getTransactions(globals.user_id_global, globals.plaid_global, start_date, end_date, account_name)
        app.hideSubWindow(bank_name+" Transaction Settings")
        app.setTransparency(100)
        return transactions
        
def listTransactionsButton(btn):
    if btn == "Back to Accounts (RBC)":
        app.destroySubWindow("RBC All Transactions")
        globals.tableRbc = False
        app.setTransparency(100)

    if btn == "Back to Accounts (CIBC)":
        app.destroySubWindow("CIBC All Transactions")
        globals.tableCibc = False
        app.setTransparency(100)

    if btn == "Back to Accounts (TD)":
        app.destroySubWindow("TD All Transactions")
        globals.tableTd = False
        app.setTransparency(100)

    if btn == "Back to Accounts (BMO)":
        app.destroySubWindow("BMO All Transactions")
        globals.tableBmo = False
        app.setTransparency(100)

def createTransTable(bank_name,transactions_list):
    app.startSubWindow(bank_name+" All Transactions")
    app.setSize("1000x700")
    app.hideTitleBar()

    data=transactions_list
    app.setSticky("new")
    app.addTable(bank_name+" transactions_table",[["Date","Merchant Name","Amount($)","Category","Description"]],row=0,column=0,rowspan=5)
    for trans in data:
        app.addTableRow(bank_name+" transactions_table",[trans['transaction_date'],trans['merchant_name'],trans['amount'],trans['category'],trans['description']])
    app.setSticky("sew")
    app.addButton("Back to Accounts ("+bank_name+")",listTransactionsButton,row=4,column=0)
    app.stopSubWindow()
    app.showSubWindow(bank_name+" All Transactions")
    globals.tableCibc = True

def transactionOptions(btn):
    print(btn)
    if btn == "CIBC View Transactions":
        start_date = app.getDatePicker("CIBC start_date_dp")
        end_date = app.getDatePicker("CIBC end_date_dp")
        account_name = app.getOptionBox("CIBC Account Options")
        bank_name = "CIBC"
        transactions_list = obtainTransactions(start_date,end_date,account_name,bank_name)

    if btn == "BMO View Transactions":
        start_date = app.getDatePicker("BMO start_date_dp")
        end_date = app.getDatePicker("BMO end_date_dp")
        account_name = app.getOptionBox("BMO Account Options")
        bank_name = "BMO"
        transactions_list = obtainTransactions(start_date,end_date,account_name,bank_name)

    if btn == "TD View Transactions":
        start_date = app.getDatePicker("TD start_date_dp")
        end_date = app.getDatePicker("TD end_date_dp")
        account_name = app.getOptionBox("TD Account Options")
        bank_name = "TD"
        transactions_list = obtainTransactions(start_date,end_date,account_name,bank_name)

    if btn == "RBC View Transactions":
        start_date = app.getDatePicker("RBC start_date_dp")
        end_date = app.getDatePicker("RBC end_date_dp")
        account_name = app.getOptionBox("RBC Account Options")
        bank_name = "RBC"
        transactions_list = obtainTransactions(start_date,end_date,account_name,bank_name)

    app.setTransparency(0)

    if bank_name == "CIBC":
        if globals.tableCibc != True:
            createTransTable(bank_name,transactions_list)
        else:
            app.showSubWindow(bank_name+" All Transactions")
    if bank_name == "RBC":
        if globals.tableRbc != True:
            createTransTable(bank_name,transactions_list)
        else:
            app.showSubWindow(bank_name+" All Transactions")
    if bank_name == "TD":
        if globals.tableTd != True:
            createTransTable(bank_name,transactions_list)
        else:
            app.showSubWindow(bank_name+" All Transactions")
    if bank_name == "BMO":
        if globals.tableBmo != True:
            createTransTable(bank_name,transactions_list)
        else:
            app.showSubWindow(bank_name+" All Transactions")

def hideTransactionsSubWindow(btn):
    if btn == "CIBC back":
        app.hideSubWindow("CIBC Transaction Settings")
        app.setTransparency(100)
    if btn == "RBC back":
        app.hideSubWindow("RBC Transaction Settings")
        app.setTransparency(100)
    if btn == "TD back":
        app.hideSubWindow("TD Transaction Settings")
        app.setTransparency(100)
    if btn == "BMO back":
        app.hideSubWindow("BMO Transaction Settings")
        app.setTransparency(100)

def transactionsSubWindow(accounts,bank_name):

    account_name_list = []

    for acc in accounts:
        account_name_list.append(acc["account_name"])

    app.destroySubWindow(bank_name+" Transaction Settings")
    app.startSubWindow(bank_name+" Transaction Settings")
    app.setSize("1000x700")
    app.setPadding([5,5])
    app.hideTitleBar()
    
    app.startLabelFrame(bank_name+" Account Selection",row=0,column=0,colspan=2)
    app.setPadding([10,5])
    app.setSticky("ew")
    app.addLabel(bank_name+" select_acc_trans", "Select Account: ",row=0,column=0)
    app.addLabelOptionBox(bank_name+" Account Options", account_name_list, row=0, column=1)
    app.stopLabelFrame()

    year_max = int(str(datetime.datetime.now())[0:4])
    year_min = int(str(datetime.datetime.now())[0:4])-1

    app.startLabelFrame(bank_name+" Start Date Select",row=1,column=0,rowspan=2)
    app.setPadding([10,5])
    app.addDatePicker(bank_name+" start_date_dp",row=0,column=0)
    app.setDatePickerRange(bank_name+" start_date_dp", year_min, year_max)
    app.setDatePicker(bank_name+" start_date_dp")
    app.stopLabelFrame()

    app.startLabelFrame(bank_name+" End Date Select",row=1,column=1,rowspan=2)
    app.setPadding([10,5])
    app.addDatePicker(bank_name+" end_date_dp",row=0,column=1)
    app.setDatePickerRange(bank_name+" end_date_dp", year_min, year_max)
    app.setDatePicker(bank_name+" end_date_dp")
    app.stopLabelFrame()

    app.startLabelFrame(bank_name+" Options",row=2,column=0,colspan=2)
    app.setPadding([10,5])
    app.setSticky("ew")
    app.addButtons([bank_name+" View Transactions"], transactionOptions,row=0,column=0)
    app.addButtons([bank_name+" back"], hideTransactionsSubWindow,row=0,column=1)
    app.stopLabelFrame()

    app.stopSubWindow()
    app.setTransparency(0)

    app.showSubWindow(bank_name+" Transaction Settings")
    app.setTransparency(0)

    return True

def accountsButtonLogic(btn):
    globals.widgetCount = 0
    api_credentials,plaid = plaidConnections.apiCredentials("sandbox")
    sys_key = plaidConnections.getSystemKey()
    user_id = plaidConnections.getUserId(globals.credentialPath,sys_key)
    user_creds_data, user_accs_file, message = plaidConnections.getUserFiles(user_id)
    user_key = user_creds_data['secret_key'].encode()

    globals.user_id_global = user_id
    globals.plaid_global = plaid
    
    accounts = getEncryptedData.getEncryptedData(user_accs_file,user_key)["accounts"]

    if btn == "View CIBC Balance":
        print(btn)
        bank_name = "CIBC"
        obtainBalance(btn,user_id,plaid,bank_name,user_accs_file,user_key)

    elif btn == "View BMO Balance":
        print(btn)
        bank_name = "BMO Bank of Montreal"
        obtainBalance(btn,user_id,plaid,bank_name,user_accs_file,user_key)

    elif btn == "View RBC Balance":
        print(btn)
        bank_name = "RBC Royal Bank"
        obtainBalance(btn,user_id,plaid,bank_name,user_accs_file,user_key)

    elif btn == "View TD Balance":
        print(btn)
        bank_name = "TD Canada Trust"
        obtainBalance(btn,user_id,plaid,bank_name,user_accs_file,user_key)

    elif btn == "View CIBC Transactions":
        print(btn)
        app.setTransparency(0)
        transactionsSubWindow(accounts,"CIBC")
        app.destroySubWindow("CIBC All Transactions")

    elif btn == "View BMO Transactions":
        print(btn)
        app.setTransparency(0)
        transactionsSubWindow(accounts,"BMO")
        app.destroySubWindow("BMO All Transactions")


    elif btn == "View RBC Transactions":
        print(btn)
        app.setTransparency(0)
        transactionsSubWindow(accounts,"RBC")
        app.destroySubWindow("RBC All Transactions")

    elif btn == "View TD Transactions":
        print(btn)
        app.setTransparency(0)
        transactionsSubWindow(accounts,"TD")
        app.destroySubWindow("TD All Transactions")

    elif btn == "Unlink CIBC":
        print(btn)
        bank_name = "CIBC"
        unlinkAccount(api_credentials,plaid,user_id,bank_name)

    elif btn == "Unlink BMO":
        print(btn)
        bank_name = "BMO Bank of Montreal"
        unlinkAccount(api_credentials,plaid,user_id,bank_name)

    elif btn == "Unlink RBC":
        print(btn)
        bank_name = "RBC Royal Bank"
        unlinkAccount(api_credentials,plaid,user_id,bank_name)

    elif btn == "Unlink TD":
        print(btn)
        bank_name = "TD Canada Trust"
        unlinkAccount(api_credentials,plaid,user_id,bank_name)

    elif btn == "Link Account":
        print(btn)
        bank_name = app.getEntry("BankName")

        if bank_name == "":
            app.errorBox("Invalid Bank Input","Please enter a bank name from the available banks list.")
        else:
            status, message = plaidConnections.linkAccount(api_credentials,plaid,user_id,bank_name)
            
            if status == False:
                app.errorBox(str(bank_name)+" Link Error: ",message)
            
                # app.startSubWindow(str(btn)+"Account Balance",modal=True)
                # app.setSize("1000x700")
                # app.setPadding([5,0])
                # app.hideTitleBar()
                # accounts = getEncryptedData.getEncryptedData(user_accs_file,user_key)

                # app.addButtons(["back"], closeAccountSubWindow,colspan=2)
                # app.stopSubWindow()
                # app.showSubWindow(str(btn)+"Account Balance")

def banking():
    app.removeFrame("BANKING")
    app.startFrame("BANKING",row=0,column=0)

    banks = ["CIBC","BMO Bank of Montreal","RBC Royal Bank","TD Canada Trust"]
    connected_banks = []
    app.setSticky("")

    api_credentials_temp,plaid_temp = plaidConnections.apiCredentials("development")
    healthy_status = plaidConnections.getInstitutions(plaid_temp,banks)

    api_credentials,plaid = plaidConnections.apiCredentials("sandbox")
    sys_key = plaidConnections.getSystemKey()
    user_id = plaidConnections.getUserId(globals.credentialPath,sys_key)

    print(user_id)

    user_creds_data, user_accs_file, message = plaidConnections.getUserFiles(user_id)
    user_key = user_creds_data['secret_key'].encode()

    accounts = getEncryptedData.getEncryptedData(user_accs_file, user_key)
    # print(accounts)
    # print(connected_banks)
    # if connected_banks:
    #     print("YEYE")
    #     if globals.transactionsSWCibc != True:
            # globals.transactionsSWCibc = transactionsSubWindow(accounts["accounts"],"CIBC")
    #         app.hideSubWindow("CIBC Transaction Settings")
    #     if globals.transactionsSWBmo != True:
    #         globals.transactionsSWBmo = transactionsSubWindow(accounts["accounts"],"BMO")
    #         app.hideSubWindow("BMO Transaction Settings")
    #     if globals.transactionsSWRbc != True:
    #         globals.transactionsSWRbc = transactionsSubWindow(accounts["accounts"],"RBC")
    #         app.hideSubWindow("RBC Transaction Settings")
    #     if globals.transactionsSWTd != True:
    #         globals.transactionsSWTd = transactionsSubWindow(accounts["accounts"],"TD")
    #         app.hideSubWindow("TD Transaction Settings")
    #     app.setTransparency(100)

    if len(accounts["accounts"]) != 0:
        for account in accounts["accounts"]:
            connected_banks.append(account["bank_name"])
    
    unique_banks = list(set(connected_banks))
    for bank in unique_banks:
        for bank_2 in banks:
            if bank_2 == bank:
                banks.remove(bank_2)
    

    if len(unique_banks) != 4:
        app.startLabelFrame("Link Bank Account",row=0,column=0,rowspan=2)
        app.setPadding([5,0])
        app.setSticky("n")
        app.addImage("institute","institute.gif",colspan=2)
        app.addEntry("BankName", 1,1)
        app.addLabel("bankLab", "Bank Name: ", 1,0)
        app.addButtons(["Link Account"],accountsButtonLogic,colspan=2) 
        app.setSticky("n")
        banks_string = ', '.join(banks)
        app.addLabel("avail_banks","Available Banks: "+banks_string,colspan=2)
        app.stopLabelFrame()
        start_idx = 1
    else:
        start_idx = 0

    # Setting up Accounts page Overview
    for i in range(len(unique_banks)):
        app.startLabelFrame(unique_banks[i],row=0,column=i+1+start_idx,rowspan=2)
        app.setSticky("n")
        app.addImage(str(unique_banks[i]),str(unique_banks[i])+".gif")
        if unique_banks[i] == "TD Canada":
            app.addButtons(["View "+str(unique_banks[i][0:2])+" Balance"],accountsButtonLogic)
            app.setSticky("n")
            app.addButtons(["View "+str(unique_banks[i][0:2])+" Transactions"],accountsButtonLogic)
            app.addButtons(["Unlink "+str(unique_banks[i][0:2])],accountsButtonLogic)
        elif unique_banks[i] == "RBC Royal Bank":
            app.addButtons(["View "+str(unique_banks[i][0:3])+" Balance"],accountsButtonLogic)
            app.setSticky("n")
            app.addButtons(["View "+str(unique_banks[i][0:3])+" Transactions"],accountsButtonLogic)
            app.addButtons(["Unlink "+str(unique_banks[i][0:3])],accountsButtonLogic)
        elif unique_banks[i] == "BMO Bank of Montreal":
            app.addButtons(["View "+str(unique_banks[i][0:3])+" Balance"],accountsButtonLogic)
            app.setSticky("n")
            app.addButtons(["View "+str(unique_banks[i][0:3])+" Transactions"],accountsButtonLogic)
            app.addButtons(["Unlink "+str(unique_banks[i][0:3])],accountsButtonLogic)
        elif unique_banks[i] == "TD Canada Trust":
            app.addButtons(["View "+str(unique_banks[i][0:2])+" Balance"],accountsButtonLogic)
            app.setSticky("n")
            app.addButtons(["View "+str(unique_banks[i][0:2])+" Transactions"],accountsButtonLogic)
            app.addButtons(["Unlink "+str(unique_banks[i][0:2])],accountsButtonLogic)
        else:
            app.addButtons(["View "+str(unique_banks[i])+" Balance"],accountsButtonLogic)
            app.setSticky("n")
            app.addButtons(["View "+str(unique_banks[i])+" Transactions"],accountsButtonLogic)
            app.addButtons(["Unlink "+str(unique_banks[i])],accountsButtonLogic)

        app.addLabel("line"+str(i),'===============================================')
        
        # Institution Health Check
        if healthy_status[i][2] == True:
            app.addLabel('item_login_status'+str(i),'Login Status: HEALTHY\n'+
            '@: '+str(datetime.datetime.now())[0:16])
            app.setLabelBg("item_login_status"+str(i), "green")
            app.setLabelFg("item_login_status"+str(i), "white")
        else:
            app.addLabel('item_login_status'+str(i),'Login Status: UNHEALTHY\n'+
            '@: '+str(datetime.datetime.now())[0:16]+
            '\nConnectivity might be unavailable.')
            app.setLabelBg("item_login_status"+str(i), "red")

        if healthy_status[i][1] == True:
            app.addLabel('trans_status'+str(i),'Transactions Status: HEALTHY\n'+
            '@: '+str(datetime.datetime.now())[0:16])
            app.setLabelBg("trans_status"+str(i), "green")
            app.setLabelFg("trans_status"+str(i), "white")
        else:
            app.addLabel('trans_status'+str(i),'Transactions Status: UNHEALTHY\n'+
            '@: '+str(datetime.datetime.now())[0:16]+
            '\nTransactions polling might be unavailable')
            app.setLabelBg("trans_status"+str(i), "red")


        app.stopLabelFrame()
        app.setPadding([5,0])


    app.stopFrame()
    app.raiseFrame("BANKING")

def notesAndNews():
    i=1
    print("CHECK NEWS")
    app.removeFrame("test2")
    app.startFrame("test2",row=0,column=0,rowspan=50,colspan=7)
    app.setSticky("")
    
    for i in range(50):
        app.addButton("Note: "+str(i),exit,row=i+1,column=7)
    for i in range(50):
        app.addButton("Note2: "+str(i),exit,row=i+1,column=1)

    app.stopFrame()
    print("CHECK FOR EXISTING NOTES")
    app.raiseFrame("test2")

def subscriptions():
    app.raiseFrame("test3")

def refresh():
    banking()

def progGUI():

    # Login/Register Frame
    app.startFrame("test1",row=0,column=0,rowspan=7,colspan=7)
    app.setPadding([10,0])
    app.addImage("bank","bankingstack.gif")
    app.addButton("Login",loginPress,row=1,column=0)
    app.addButton("Register",registerPress,row=2,column=0)
    app.addButton("Exit",exitPress,row=3,column=0)
    app.stopFrame()

    # Welcome Frame
    app.startFrame("WELCOME",row=0,column=0,rowspan=3,colspan=2)
    app.setSticky("")
    app.addImage("bank2","bankingstack.gif")
    app.addLabel("greeting","Welcome to BankingStack!")
    app.addLabel("instructions","Instructions:\n"+
    "- To access Banking features, click on the 2nd icon in the toolbar.\n"+
    "- To access Financial Plan features, click on the 3rd icon in the toolbar.\n"+
    "- To access Subscriptions tracker, click on the 4th icon in the toolbar.\n"+
    "- The 5th icon is to logout of the system\n"+
    "- To see the instructions page again, click on the home icon.")
    app.stopFrame()

    # Banking Frame
    app.startFrame("BANKING",row=0,column=0,rowspan=7,colspan=7)
    app.setSticky("")
    app.addLabel("banking_temp",".")
    app.stopFrame()

    # Notes Frame
    app.startFrame("test2",row=0,column=0,rowspan=7,colspan=7)
    app.setSticky("ne")
    app.addLabel("notes_temp",".")
    app.stopFrame()

    # Subscriptions Frame
    app.startFrame("test3",row=0,column=0,rowspan=7,colspan=7)
    app.setSticky("")
    app.addLabel("subscriptions_temp",".")
    app.stopFrame()

    # Toolbar
    app.raiseFrame("test1")
    app.addToolbarButton("Home",welcome,findIcon=True)
    app.addToolbar(["Accounts"],banking,findIcon=True)
    app.addToolbarButton("Financial Plan",notesAndNews,findIcon=True)
    app.addToolbarButton("Subscriptions",subscriptions,findIcon=True)
    app.addToolbarButton("Refresh",refresh,findIcon=True)
    app.addToolbarButton("Logout",exitApplication,findIcon=True)
    app.setToolbarIcon("Home","home")
    app.setToolbarIcon("Accounts","bank")
    app.setToolbarIcon("Financial Plan","document")
    app.setToolbarIcon("Subscriptions","address-book")
    app.setToolbarIcon("Refresh","refresh")
    app.setToolbarBg("light blue")
    app.hideToolbar()
    app.go()

progGUI()
