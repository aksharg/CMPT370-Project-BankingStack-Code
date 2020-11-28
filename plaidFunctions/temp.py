
def encryptApiCreds():
    with open("plaidFunctions\systemKey.key", "r") as key_file:
        key = key_file.read().encode()
        key_file.close()

    with open("plaidFunctions/apiCredentials.json") as json_file:
        json_api_credentials = json_file.read()
        json_file.close()

    encrypted_creds = encryptData(json_api_credentials,key)

    with open("plaidFunctions/apiCredentials.json","w") as creds_file:
        creds_file.write(encrypted_creds.decode())
        creds_file.close()


def tempGenKey():
    key = Fernet.generate_key()
    key_file = open("systemKey.key", "w")
    key_file.write(key.decode())
    key_file.close()