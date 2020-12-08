from encryption import encryptData
from cryptography.fernet import Fernet, InvalidToken
import json
import pytest


def test_stringEncryption():
    """Check that encrypted data can be decrypted
    
    Runs the encryptData function on several different strings to ensure 
    that they that the encrypted data, when decrypted and decoded is the 
    same as the data that was passed in. Also checks to make sure that 
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

    encrypted_string =encryptData(string1,key1)
    assert (cipher_suite1.decrypt(encrypted_string)).decode() == string1

    assert (cipher_suite1.decrypt(encrypted_string)) != string1

    encrypted_string =encryptData(string2,key1)
    assert (cipher_suite1.decrypt(encrypted_string)).decode() == string2

    assert (cipher_suite1.decrypt(encrypted_string)) != string2

    encrypted_string =encryptData(string3,key1)
    assert (cipher_suite1.decrypt(encrypted_string)).decode() == string3

    assert (cipher_suite1.decrypt(encrypted_string)) != string3


def test_invalidFernetKeyEncryption():
    with pytest.raises(InvalidToken):
        """Checks that only the encryption key will decrypt the data

            Runs the encryptData function and then tries an incorrect key to ensure 
            that the data is properly encrypted. An incorrect key will throw the 
            InvalidToken exception. If the test catches this exception it indicates 
            that the function properly encrypted the passed in data with the passed 
            in key

        """
        key1 = Fernet.generate_key()
        key2 = Fernet.generate_key()
        cipher_suite1 = Fernet(key1)
        cipher_suite2 = Fernet(key2)
        string1 = "12345678"
        encrypted_string =encryptData(string1,key2)
        (cipher_suite1.decrypt(encrypted_string)).decode() 
    

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

    encrypted_string1 =encryptData(string1,key1)
    encrypted_string2 =encryptData(string1,key2)

    assert (cipher_suite1.decrypt(encrypted_string1)).decode() == (cipher_suite2.decrypt(encrypted_string2)).decode()

    encrypted_string1 =encryptData(string2,key1)
    encrypted_string2 =encryptData(string2,key2)

    assert (cipher_suite1.decrypt(encrypted_string1)).decode() == (cipher_suite2.decrypt(encrypted_string2)).decode()

    encrypted_string1 =encryptData(string3,key1)
    encrypted_string2 =encryptData(string3,key2)

    assert (cipher_suite1.decrypt(encrypted_string1)).decode() == (cipher_suite2.decrypt(encrypted_string2)).decode()


