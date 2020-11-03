import json

def fileCreation(file_name, source, data):
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
	file = open(file_name, "w")
	file.write(data)
	file.close()

	return file.name
