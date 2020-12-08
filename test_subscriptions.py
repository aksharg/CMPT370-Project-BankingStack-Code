print("Begining subscription tests")

#import pytest
import os
import json
from subscriptions import *


def test_addSubcription():
    """
    Check that data inputted is passed through addSubscriptions and goes to createSubscriptionsJson correctly
    """
    addSubscription("fakecompany1", 69, "Monthly", 10, "10/09/2020")
    file = open("userSubscriptions.json", "r")
    data = json.load(file)
    

    errors = []

    if not data[0]["company"] == "fakecompany1":
        errors.append("compnay: expected " + str(type("fakecompany1")) + " " + "fakecompany1" + 
                            ", got " + str(type(data[0]["company"])) + " " + str(data[0]["company"]))

    if not data[0]["amount"] == 69:
        errors.append("amount: expected " + str(type(69)) + " " + str(69) + 
                            ", got " + str(type(data[0]["amount"])) + " " + str(data[0]["amount"]))

    if not data[0]["paymentFrequency"] == "Monthly":
        errors.append("frequency: expected " + str(type("Monthly")) + " " + "Monthly" + 
                            ", got " + str(type(data[0]["paymentFrequency"])) + " " + str(data[0]["paymentFrequency"]))

    if not data[0]["subPeriod"] == 10:
            errors.append("period: expected " + str(type("10")) + " " + str(10) + 
                            ", got " + str(type(data[0]["subPeriod"])) + " " + str(data[0]["subPeriod"]))

    if not data[0]["startDate"] == "10/09/2020":
            errors.append("date: expected " + str(type("10/09/2020")) + " " + "10/09/2020" + 
                            ", got " + str(type(data[0]["startDate"])) + " " + str(data[0]["startDate"]))

    assert not errors, "errors occurred:\n{}".format("\n".join(errors))



def test_editSubcription():
    """
    Tests for successful editing of subscription from file
    """
    file = open("userSubscriptions.json", "r")
    data = json.load(file)
    testingId=data[0]["subId"]
    file.close

    editSubscription(testingId, "fakecompany2", 70, "Monthly", 15, "10/09/2020")

    data = json.load(open("userSubscriptions.json", "r"))
    

    errors = []

    if not data[0]["company"] == "fakecompany2":
        errors.append("compnay: expected " + str(type("fakecompany2")) + " " + "fakecompany2" + 
                            ", got " + str(type(data[0]["company"])) + " " + str(data[0]["company"]))

    if not data[0]["amount"] == 70:
        errors.append("amount: expected " + str(type(70)) + " " + str(70) + 
                            ", got " + str(type(data[0]["amount"])) + " " + str(data[0]["amount"]))

    if not data[0]["paymentFrequency"] == "Monthly":
        errors.append("frequency: expected " + str(type("Monthly")) + " " + "Monthly" + 
                            ", got " + str(type(data[0]["paymentFrequency"])) + " " + str(data[0]["paymentFrequency"]))

    if not data[0]["subPeriod"] == 15:
            errors.append("period: expected " + str(type("15")) + " " + str(15) + 
                            ", got " + str(type(data[0]["subPeriod"])) + " " + str(data[0]["subPeriod"]))

    if not data[0]["startDate"] == "10/09/2020":
            errors.append("date: expected " + str(type("10/09/2020")) + " " + "10/09/2020" + 
                            ", got " + str(type(data[0]["startDate"])) + " " + str(data[0]["startDate"]))

    assert not errors, "errors occurred:\n{}".format("\n".join(errors))




def test_deleteSubscription():
    """
    Tests for successful deletion of subscription from file
    """
    file = open("userSubscriptions.json", "r")
    data = json.load(file)
    testingId=data[0]["subId"]
    file.close
    deleteSubscription(int(testingId))
    data = json.load(open("userSubscriptions.json","r"))
    
    
    errors = []

    if data != []:
        errors.append("expected empty list, got" + str(data))


    assert not errors, "errors occurred:\n{}".format("\n".join(errors))

test_addSubcription()
test_editSubcription()
test_deleteSubscription()

print("Tests completed")
