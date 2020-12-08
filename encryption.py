from cryptography.fernet import Fernet, InvalidToken

def generateKey():
    return Fernet.generate_key()

def encryptData(data, key):
    """Encrypts the passed in data with the given key

    Takes the data and key passed in and performs a fernet encryption
    the encrypted data is returned.

    Args:
        data: A string of unknown format (could be json dump or 
        normal text string). It should not be encoded.
        key: The key with which data will be encrypted. The key 
        type is Fernet
    Returns:
        An encoded string containing the Fernet encrypted data. The 
        only way to access the data is to decrypt it with the same 
        key that was provided as an argument.

    """
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text


def decryptData(encrypted_data,key):
    """Decrypts the received data with the given key
    Takes the encrypted data and encryption key and performs a fernet decryption
    the decrypted data string is then returned

    Args:
        encrypted_data: A Fernet encrypted string, the 
        strings format is unknown
        key:  The key with which data was encrypted and will be 
        decrypted with. The key type is Fernetq

    Returns:
        A string of data completely decrypted and decoded
    """
    cipher_suite = Fernet(key)
    data = cipher_suite.decrypt(encrypted_data)
    return data