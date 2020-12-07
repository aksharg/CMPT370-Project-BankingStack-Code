import encryption
import json
import os

def encryptAPICredentials():
    key_file = open("systemKey.key","rb")
    key = key_file.read()
    key_file.close()

    file = open("apiCredentials.json","r")
    raw_data = file.read()
    file.close()

    raw_json_data = json.dumps(raw_data)
    encrypted_data = encryption.encryptData(raw_json_data,key)

    file = open("apiCredentials.json","wb")
    file.write(encrypted_data)
    file.close()

encryptAPICredentials()