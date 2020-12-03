from random import randint
import os
import json
import re
import pytest
import encryption
from getEncryptedData import getEncryptedData
from fileCreation import fileCreation, updateFile
#from test_encryption import decryptData

# user_id = None
# name = None
# email = None
# pswd = None
# #
# validation_flag = None
# date_created = None
# secret_key = None
# accounts_list = None
# financial_plans_list = None

def usernamePasswordFormatCheck(string_in, search=re.compile(
            r"^[A-Za-z0-9_]+$").search):
    """Verifies the input for a username or password field

    Args:
        string_in: A string containing a username or password
    Returns:
        True: if input was a valid formatted string
        False: if input was an invalid formatted string
        
    """
    return bool(search(string_in))

def emailFormatCheck(string_in, search=re.compile(
            r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$").search):
    """Verifies the input for an email field

    Args:
        string_in: A string containing an email
    Returns:
        True: if input was a valid formatted string
        False: if input was an invalid formatted string
    """
    return bool(search(string_in))

def updateUserUsername(file_path, old_username, new_username, key):
    exit_tuple = None
    if not usernamePasswordFormatCheck(new_username):
        exit_tuple = (False, "Invalid username.  Please enter only letters or numbers.")
        return exit_tuple
    data = getEncryptedData(file_path, key)
    for users in data["users"]:
        if users["username"] == old_username:
            users["username"] = new_username
    data_json_string = json.dumps(data)
    encrypted_data = encryption.encryptData(data_json_string, key)
    updateFile(file_path, encrypted_data, True)

    exit_tuple = (True, "Success")
    return exit_tuple

def updateUserCredentialUsername(file_path, new_username, key):        ################## Decide whether to include name field in the files, if going with just username and want to update username then remember to update username in users.json as well, also decide on if other values will be stored in files ex. date_created
    """Update Username

    Verifies that new_username is of an acceptable format then accesses file 
    at path file_name and retrieves the contents of the file.
    Finds the username section of the dictionary and reassigns it's value to 
    new_username.  Encrypts new dictionary data and writes over old contents 
    of file.

    Args:
        file_path: A string containing the full path to the file
        new_username: A string containing the user's new username
    Returns:
        A tuple with two values, first is whether operations of the function
        executed fully. Second is a context string for where in the process
        the execution was terminated.

    """
    exit_tuple = None
    if not usernamePasswordFormatCheck(new_username):
        exit_tuple = (False, "Invalid username.  Please enter only letters or numbers.")
        return exit_tuple
    data = getEncryptedData(file_path, key)
    data["username"] = new_username
    data_json_string = json.dumps(data)
    encrypted_data = encryption.encryptData(data_json_string, key)
    updateFile(file_path, encrypted_data, True)

    exit_tuple = (True, "Success")
    return exit_tuple

def updateEmail(file_path, new_email, key):
    """Update Email

    Verifies that new_email is of an acceptable format then accesses file
    at path file_name and retrieves the contents of the file.
    Finds the email section of the dictionary and reassigns it's value to 
    new_email.  Encrypts new dictionary data and writes over old contents 
    of file.

    Args:
        file_path: A string containing the full path to the file
        new_email: A string containing the user's new email
    Returns:
        A tuple with two values, first is whether operations of the function
        executed fully. Second is a context string for where in the process
        the execution was terminated.

    """
    exit_tuple = None
    if not emailFormatCheck(new_email):
        exit_tuple = (False, "Invalid email.")
        return exit_tuple
    data = getEncryptedData(file_path, key)
    data["email"] = new_email
    data_json_string = json.dumps(data)
    encrypted_data = encryption.encryptData(data_json_string, key)
    updateFile(file_path, encrypted_data, True)

    exit_tuple = (True, "Success")
    return exit_tuple

def changePswd(file_path, new_password, key):
    """Update Email

    Verifies that new_password is of an acceptable format then accesses file
    at path file_name and retrieves the contents of the file.
    Finds the password section of the dictionary and reassigns it's value to
    new_password.  Encrypts new dictionary data and writes over old contents
    of file.

    Args:
        file_path: A string containing the full path to the file
        new_password: A string containing the user's new password
    Returns:
        A tuple with two values, first is whether operations of the function
        executed fully. Second is a context string for where in the process
        the execution was terminated.

    """
    exit_tuple = None
    if not usernamePasswordFormatCheck(new_password):
        exit_tuple = (False, "Invalid password. Please enter only letters or numbers.")
        return exit_tuple
    data = getEncryptedData(file_path, key)
    data["password"] = new_password
    data_json_string = json.dumps(data)
    encrypted_data = encryption.encryptData(data_json_string, key)
    updateFile(file_path, encrypted_data, True)

    exit_tuple = (True, "Success")
    return exit_tuple

def generateUserId():
    """Generates a random 8 digit integer

    Generates a random 8 digit integer.
    
    Returns:
        A random 8 digit integer

    """
    return randint(10000000, 99999999)

def generateUserDir(user_id, test=False):
    """Generates a directory to house a users individual data files

    Finds the full path to the folder that this code was run from then
    appends the generated user_id to the path as a child directory and
    verifies that that directory doesn't already exist, if not then
    creates the directory with the new path.

    Args:
        user_id: A 8 digit integer representing a user's data directory
    Returns:
        A tuple with two values, first is whether the directory already
        existed. Second will be a string with an error message in the
        case that the directory already existed, otherwise it will
        contain a string specifying the full path to the created directory.

    """
    exit_tuple = None

    if not test == False:
        directory_path = test
    else:
        directory_path = os.getcwd()
    directory_path += "\\" + str(user_id)
    if os.path.exists(directory_path):
        exit_tuple = (False, "Directory already exists")
        return exit_tuple
    os.mkdir(directory_path)
    exit_tuple = (True, directory_path)
    return exit_tuple

def createTestFile(file_name, username, password, email, key):
    """For purposes of test functions to create a formatted test file

    """
    file_contents = {"username": username,
                    "password": password,
                    "email": email}
    json_file_contents = json.dumps(file_contents)
    encrypted_data = encryption.encryptData(json_file_contents, key)
    file = open(file_name, "wb")
    file.write(encrypted_data)
    file.close()

def test_updateUsername(tmpdir):
    """
    """
    if not os.path.exists("systemKey.key"):
        encryption.generateSystemKey()
    file = open("systemKey.key", "rb")
    key = file.read()
    file.close()

    file_name = tmpdir / "temptestingFile.json"
    # incase file_name currently exists in directory,
    # don't want to mess with user's file
    while os.path.exists(file_name):
        file_name = file_name[:len(file_name)- 5] + "1" + file_name[len(file_name)- 5:]
    createTestFile(file_name, "bill", "pass123", "abc@123.com", key)
    data = getEncryptedData(file_name, key)
    old_username = data["username"]
    updateUserCredentialUsername(file_name, "jim", key)
    new_data = getEncryptedData(file_name, key)
    new_username = new_data["username"]
    #os.remove(file_name)
    assert old_username != new_username
    assert new_username == "jim"


def test_updateEmail(tmpdir):
    """
    """
    if not os.path.exists("systemKey.key"):
        encryption.generateSystemKey()
    file = open("systemKey.key", "rb")
    key = file.read()
    file.close()
    
    file_name = tmpdir / "temptestingFile.json"
    # incase file_name currently exists in directory,
    # don't want to mess with user's file
    while os.path.exists(file_name):
        file_name = file_name[:len(file_name)- 5] + "1" + file_name[len(file_name)- 5:]
    createTestFile(file_name, "bill", "pass123", "abc@123.com", key)
    data = getEncryptedData(file_name, key)
    old_email = data["email"]
    updateEmail(file_name, "123@gmail.com", key)
    new_data = getEncryptedData(file_name, key)
    new_email = new_data["email"]
    #os.remove(file_name)
    assert old_email != new_email
    assert new_email == "123@gmail.com"


def test_changePswd(tmpdir):
    """
    """
    if not os.path.exists("systemKey.key"):
        encryption.generateSystemKey()
    file = open("systemKey.key", "rb")
    key = file.read()
    file.close()
    
    file_name = tmpdir / "temptestingFile.json"
    # incase file_name currently exists in directory,
    # don't want to mess with user's file
    while os.path.exists(file_name):
        file_name = file_name[:len(file_name)- 5] + "1" + file_name[len(file_name)- 5:]
    createTestFile(file_name, "bill", "pass123", "abc@123.com", key)
    data = getEncryptedData(file_name, key)
    old_pswd = data["password"]
    changePswd(file_name, "secretpswd123", key)
    new_data = getEncryptedData(file_name, key)
    new_pswd = new_data["password"]
    #os.remove(file_name)
    assert old_pswd != new_pswd
    assert new_pswd == "secretpswd123"


def test_generateUserId():
    """
    """
    user_id = generateUserId()
    assert ((user_id >= 10000000) and (user_id <= 99999999))

def test_generateUserDir(tmpdir):
    """
    """
    user_id = 123
    result = (False, "")
    while result[0] == False:
        user_id += 1
        result = generateUserDir(user_id, tmpdir)
    file_path = result[1]
    assert os.path.exists(file_path)
    assert os.path.isdir(file_path)

# def main():
#     if not os.path.exists("systemKey.key"):
#         encryption.generateSystemKey()
#     file = open("systemKey.key", "rb")
#     key = file.read()
#     file.close()

#     createTestFile("temp.json", "asdf", "pass123", "123@asdf.netz", key)
#     data = getEncryptedData("temp.json", key)
#     json_string = json.dumps(data)
#     fileCreation("temp123.json", json_string)
#     result = updateEmail("temp.json", "rrr@gmail.netz", key)
#     print(result[1])
#     if result[0] == True:
#         data = getEncryptedData("temp.json", key)
#         json_string = json.dumps(data)
#         fileCreation("tempabc.json", json_string)
    
    
# if __name__ == "__main__":
#     main()
