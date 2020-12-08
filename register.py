import json
import os
import re
import datetime
import globals
from person import generateUserId, generateUserDir
from fileCreation import fileCreation, updateFile
import encryption
from getEncryptedData import getEncryptedData



def register(username, password, email):
    """Register the user

    Verifies args are of acceptable format then checks to see if users.json
    exists.  If not, creates users.json and adds user.  If yes, then
    checks if user already exists and if not adds user to file.  If user was
    added to users.json then proceeds to create the userCredentials.json in
    the user's new directory.

    Args:
        username: A string containing the user's username
        password: A string containing the user's password
        email: A string containing the user's email
    Returns:
        A tuple with two values, first is whether operations of the function
        executed fully. Second is a context string for where in the process
        the execution was terminated.

    """
    exit_tuple = None

    if not usernamePasswordFormatCheck(username):
        exit_tuple = (False, "Invalid username. Please enter only letters or numbers.")
        return exit_tuple
    if not usernamePasswordFormatCheck(password):
        exit_tuple = (False, "Invalid password. Please enter only letters or numbers.")
        return exit_tuple
    if not emailFormatCheck(email):
        exit_tuple = (False, "Invalid email.")
        return exit_tuple

    # code to send email to validated address with a generated code
    # Prompt user to enter the code they received to validate email

    exists = False

    # if not os.path.exists("systemKey.key"):
    #     encryption.generateSystemKey()
    # file = open("systemKey.key", "rb")
    # key = file.read()
    # file.close()

    key=globals.general_key

    if not os.path.exists("users.json"):
        # Have to verify that generateUserID is not the same as a previous
        # user, very small chance but possible
        result = (False, "")
        while result[0] == False:
            user_ID = generateUserId()
            result = generateUserDir(user_ID)
        user_dir = result[1]
        initialize_users = {"users":[
                {"username": username,
                "path": user_dir,
                "user_id":str(user_ID)}]}
        json_string = json.dumps(initialize_users)
        encrypted_data = encryption.encryptData(json_string, key)
        users_file = fileCreation("users.json", encrypted_data, True)
    else:
        data = getEncryptedData("users.json", key)
            
        for users in data["users"]:
            if users["username"] == username:
                exists = True
                exit_tuple = (False, "Username already exists")
                return exit_tuple
        if exists == False:
            result = (False, "")
            while result[0] == False:
                user_ID = generateUserId()
                result = generateUserDir(user_ID)
            user_dir = result[1]
            entry = {"username": username,
                    "path": user_dir}
            data["users"].append(entry)
            data_json_string = json.dumps(data)
            encrypted_data = encryption.encryptData(data_json_string, key)
            updateFile("users.json", encrypted_data, True)

    data_user_credentials = {"username": username,
                            "user_id": user_ID,
                            "password": password,
                            "email": email,
                            "creation_date": str(datetime.datetime.now()),
                            "secret_key": str(encryption.generateKey().decode())}
    data_user_credentials_json_string = json.dumps(data_user_credentials)
    encrypted_data = encryption.encryptData(data_user_credentials_json_string, key)
    user_credential_path = user_dir + "\\userCredentials.json"
    fileCreation(user_credential_path, encrypted_data, True)
    fileCreation(user_dir +"\\userSubscriptions.json","[]",False)

    # data = getEncryptedData("users.json", key)
    # json_string = json.dumps(data)
    # fileCreation("temp_testing.json", json_string)

    # data = getEncryptedData(user_dir + "\\userCredentials.json", key)
    # json_string = json.dumps(data)
    # fileCreation("temp_testing_credentials.json", json_string)

    exit_tuple = (True, user_credential_path)
    return exit_tuple

def usernamePasswordFormatCheck(string_in, search=re.compile(r"^[A-Za-z0-9_]+$").search):
    """Verifies the input for a username or password field

    Args:
        string_in: A string containing a username or password
    Returns:
        True: if input was a valid formatted string
        False: if input was an invalid formatted string
        
    """
    return bool(search(string_in))

def emailFormatCheck(string_in, search=re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$").search):
    """Verifies the input for an email field

    Args:
        string_in: A string containing an email
    Returns:
        True: if input was a valid formatted string
        False: if input was an invalid formatted string
    """
    return bool(search(string_in))

# def main():
#     name_in = input("Enter your name : ")
#     password_in = input("Enter your password : ")
#     email_in = input("Enter your email : ")

#     # name_in = "jim"
#     # password_in = "pass123"
#     # email_in = "123@abc.netz"

#     success = register(name_in, password_in, email_in)
    
#     print(success[1])
#     # if success[0] == True:
#     #     print(success[1])
#     # elif success[0] == False:
#     #     print(success[1])
    
# if __name__ == "__main__":
#     main()


