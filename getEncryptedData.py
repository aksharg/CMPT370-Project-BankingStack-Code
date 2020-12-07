import encryption
import json
def getEncryptedData(file_path, key):
    """Reads, decrypts, and returns contents of file

    Opens and retrieves contents of file_name then decrypts the data and
    converts the json string back to a dictionary.

    Args:
        file_path: A string containing the full path to the file
    Returns:
        A dictionary representation of the decrypted contents of the file

    """
    file = open(file_path, "rb")
    encrypted_data = file.read()
    file.close()

    unencrypted_data = encryption.decryptData(encrypted_data, key)
    data = json.loads(unencrypted_data)
    return data
