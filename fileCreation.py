def fileCreation(file_name, data, encrypted=False):
    """Create a file

    Creates a file and writes the value of data into the file.

    Args:
        file_name: A string describing name of file and path if applicable
        source: Source may be used to specify what formatting or 
        what kind of file to create in the future but right now it does nothing
        data: A string that may be encrypted or unencrypted
    Returns:
        The created file's name.

    """
    if encrypted == False:
        file = open(file_name, "w")
        file.write(data)
        file.close()

        return file.name
    elif encrypted == True:
        file = open(file_name, "wb")
        file.write(data)
        file.close()

        return file.name
    else:
        print("Error: arg 3 in fileCreation() can only be True, False, or omitted from call")

def updateFile(file_name, data, encrypted=False):
    """Writes new data into file and removes old data

    Writes new data into file at start of the file then
    truncates the old data out.

    Args:
        file_name: A string describing name of file or direct path
        data: A string that may be encrypted or unencrypted

    """
    #json_string = json.dumps(data)
    #encrypted_data = encryptData(json_string, secret_key) ##### Need to replace secret_key with proper value

    if encrypted == False:
        with open(file_name,'r+') as f:
            f.seek(0)
            f.write(data)
            f.truncate()
    elif encrypted == True:
        with open(file_name,'rb+') as f:
            f.seek(0)
            f.write(data)
            f.truncate()
    else:
        print("Error: arg 3 in updateFile() can only be True, False, or omitted from call")

# def main():
#     file = open("test.TXT", "r")
#     data = file.read()
#     file.close()

#     print(data)


#     # path = os.getcwd()
#     # path += "\\testDirect"
#     # os.mkdir(path)
    
#     # file = open("testdir", "w")
#     # file.close()

# if __name__ == "__main__":
#     main()