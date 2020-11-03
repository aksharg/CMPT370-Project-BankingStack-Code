from cryptography.fernet import Fernet, InvalidToken


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