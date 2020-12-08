from decryption import decryptData
from cryptography.fernet import Fernet, InvalidToken
import json
import pytest


def test_stringDecryption():
    """Check that encrypted data can be decrypted
    
    Runs the decryptData function on several different encrypted strings to ensure 
    that the encrypted data when decrypted and decoded is the 
    same as the data that was encrypted passed in. Also checks to make sure that 
    if the decrypted data is not decoded it does not match the string 
    that was originally encrypted

    """
    key1 = Fernet.generate_key()
    cipher_suite1 = Fernet(key1)

    this_dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
    }
    string1 = "12345678"
    string2 = "Hello World!"
    string3 = json.dumps(this_dict)
    encrypted_text1 = cipher_suite1.encrypt(string1.encode())
    encrypted_text2 = cipher_suite1.encrypt(string2.encode())
    encrypted_text3 = cipher_suite1.encrypt(string3.encode())
    # with open("test.json","w") as f:
    #     f.write(encrypted_text1.decode())
    #     f.close()

    # with open("test.json","r") as f:
    #     read_encrypted_text =f.read().encode()
    
    assert decryptData(encrypted_text1,key1).decode() == string1
    
    
    assert decryptData(encrypted_text2,key1).decode() == string2
    
    assert decryptData(encrypted_text3,key1).decode() == string3
    assert decryptData(encrypted_text3,key1) != string3
    # encrypted_string =encryptData(string2,key1)
    # assert (cipher_suite1.decrypt(encrypted_string)).decode() == string2

    # assert (cipher_suite1.decrypt(encrypted_string)) != string2

    # encrypted_string =encryptData(string3,key1)
    # assert (cipher_suite1.decrypt(encrypted_string)).decode() == string3

    # assert (cipher_suite1.decrypt(encrypted_string)) != string3





def test_invalidFernetKeyDecryption():
    with pytest.raises(InvalidToken):
        """Checks that only the encryption key will decrypt the data

            Runs the encryptData function and then passes an incorrect key to decryptData 
            to ensure that the data is properly encrypted. An incorrect key will throw the 
            InvalidToken exception. If the test catches this exception it indicates 
            that the function responds properly to invalid key inputs and cannot use 
            them to decrypt

        """
        key1 = Fernet.generate_key()
        key2 = Fernet.generate_key()
        cipher_suite1 = Fernet(key1)
        
        string1 = "12345678"
        encrypted_string =cipher_suite1.encrypt(string1.encode())
        decryptData(encrypted_string,key2)
    

def test_stringValidity():
    """Checks that data encrypted with 2 different keys 
    is still equal after being decoded

    Generates 2 Fernet keys which are used encrypt a string.
    After being encrypted an assertion is run that checks that when 
    decrypted  the strings still match despite having been encrypted with 
    different keys. This is run on 3 different strings.

    """
    key1 = Fernet.generate_key()
    key2 = Fernet.generate_key()
    cipher_suite1 = Fernet(key1)
    cipher_suite2 = Fernet(key2)
    this_dict = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
    }
    string1 = "12345678"
    string2 = "Hello World!"
    string3 = json.dumps(this_dict)

    encrypted_string1 =cipher_suite1.encrypt(string1.encode())
    encrypted_string2 =cipher_suite2.encrypt(string1.encode())

    assert (decryptData(encrypted_string1,key1)).decode() == (decryptData(encrypted_string2,key2)).decode()

    encrypted_string1 =cipher_suite1.encrypt(string2.encode())
    encrypted_string2 =cipher_suite2.encrypt(string2.encode())

    assert (decryptData(encrypted_string1,key1)).decode() == (decryptData(encrypted_string2,key2)).decode()

    encrypted_string1 =cipher_suite1.encrypt(string3.encode())
    encrypted_string2 =cipher_suite2.encrypt(string3.encode())

    assert (decryptData(encrypted_string1,key1)).decode() == (decryptData(encrypted_string2,key2)).decode()


