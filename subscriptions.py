import json
import random
import sys
import globals

"""
addSubscription takes input and creates a subscription 
dict and passes to createSubscriptionsJson

Arguments:
    company: A company name for subscription
    amount: how much the user is paying per interval
    paymentFrequency: how often the user is paying
    subscriptionPeriod:  
    startDate: when payment began

Returns: 
    None

"""
def addSubscription(company, amount, paymentFrequency, subscriptionPeriod, startDate):
    
    sub = {"company": company,
            "amount": amount,
            "paymentFrequency": paymentFrequency,
            "subPeriod": subscriptionPeriod,
            "startDate": startDate,
            "subId": generateSubscriptionId()
            }

    createSubscriptionsJson(sub)
    print("Subscription created with ID: "+str(sub["subId"]))


"""
Creates a random ID for subscriptions used for editing and deleting

Arguments:
    None

Returns:
    a random int from 1000-9999

"""
def generateSubscriptionId():
    intToReturn = random.randint(1000, 9999)
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    data = json.load(open(user_dir+"userSubscriptions.json","r"))
    for x in data: 
        if intToReturn in x:
            generateSubscriptionId()
    return intToReturn


"""
Writes to userSubscriptions.json

Arguments:
    subscription dict

Returns:
    None

"""

def createSubscriptionsJson(subscription):
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    file = open(user_dir+"userSubscriptions.json","r")
    data = json.load(file)
    data.append(subscription)
    file.close
    newFile = open(user_dir+"userSubscriptions.json","w")
    newFile.write(json.dumps(data))
    newFile.close


"""
Takes in data for updating a subscription in the userSubscriptions.json file

Arguments:
    subscriptionId: Id for determining which subscription to edit
    company: A company name for subscription
    amount: how much the user is paying per interval
    paymentFrequency: how often the user is paying
    subscriptionPeriod:  
    startDate: when payment began

Returns:
    None

"""

def editSubscription(subscriptionId, company, amount, paymentFrequency, subscriptionPeriod, startDate):
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    file = open(user_dir+"userSubscriptions.json","r+")
    data = json.load(file)
    for x in data:
        if subscriptionId == x["subId"]:
            x["company"]=company
            x["amount"]=amount
            x["paymentFrequency"]=paymentFrequency
            x["subPeriod"]=subscriptionPeriod
            x["startDate"]=startDate
            editSubscriptionJson(data)
    file.close


"""
Edits the json file with the updated data from editSibscription

Arguments:
    updatedData: dict of updated data

Returns:
    None

"""

def editSubscriptionJson(updatedData):
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    file = open(user_dir+"userSubscriptions.json","w")
    file.write(json.dumps(updatedData))
    file.close


"""
deletes a subscription from the json using ID

arguments:
    subscriptionId: ID used to determine which subscription to delete

Returns:
    None

"""

def deleteSubscription(subscriptionId):
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    file = open(user_dir+"userSubscriptions.json","r+")
    data = json.load(file)
    for x in data:
        if subscriptionId == x["subId"]:
            data.remove(x)
    file.close
    file = open(user_dir+"userSubscriptions.json","w")
    file.write(json.dumps(data))
    file.close


"""
lists all subscriptions in the json file

Arguments:
    None

Returns:
    None

"""

def listSubscriptions():
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    string =""
    data = json.load(open(user_dir+"userSubscriptions.json","r"))
    for x in data:
        string+=str(x)+"\n"
    return string


"""
for sending subscription data to GUI

Arguments:
    None

Returns:
    list of dicts data for the gui

"""
def sendSubData():
    user_dir = globals.credentialPath
    user_dir = user_dir[:-20]
    return json.load(open(user_dir+"userSubscriptions.json","r"))



# def main():
#     if sys.argv[1] == "list":
#         print(listSubscriptions())
    
#     if sys.argv[1] == "add":
#         addSubscription(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

#     if sys.argv[1] == "edit":
#         editSubscription(int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5], int(sys.argv[6]), sys.argv[7])

#     if sys.argv[1] == "del":
#         deleteSubscription(int(sys.argv[2]))

#     if sys.argv[1] == "usage":
#         print("add company amount paymentFrequency subscriptionPeriod startDate \n"
#         +"edit subId company amount paymentFrequency subscriptionPeriod startDate \n"
#         +"del subId \n"
#         +"list \n")


# if __name__ == "__main__":
#     main()