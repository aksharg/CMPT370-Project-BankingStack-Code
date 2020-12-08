import json
import os
import globals
from getEncryptedData import getEncryptedData

def login(username, password):
    """Verify user login

    Checks in users.json to verify if username exists, if so then proceeds
    to the userCredentials.json in the specified path and verifies if
    password matchs what is in the file.

    Args:
        username: A string containing the login attempt username
        password: A string containing the login attempt password
    Returns:
        A tuple with two values, first is whether operations of the function
        executed fully. Second is a context string for where in the process
        the execution was terminated.

    """
    exists = False
    login_path = None
    exit_tuple = None

    if not os.path.exists("users.json"):
        exit_tuple = (False, "No users are currently registered.  Please register first")
        return exit_tuple

    key = globals.general_key

    data = getEncryptedData("users.json", key)
    for users in data["users"]:
        if users["username"] == username:
            exists = True
            login_path = users["path"]
            break
    if exists == False:
        exit_tuple = (False, "Username does not exist")
        return exit_tuple

    user_credential_path = login_path + "\\userCredentials.json"
    data = getEncryptedData(user_credential_path, key)
    if password == data["password"]:
        exit_tuple = (True, user_credential_path)
        return exit_tuple
    exit_tuple = (False, "Incorrect Password")
    return exit_tuple

# def main():
#     print("#### Login ####")
#     username_in = input("Username: ")
#     password_in = input("Password: ")

#     success = login(username_in, password_in)
    
#     print(success[1])
#     # if success[0] == True:
#     #     print(success[1])
#     # elif success[0] == False:
#     #     print(success[1])

# if __name__ == "__main__":
#     main()

