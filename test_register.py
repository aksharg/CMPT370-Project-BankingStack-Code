import pytest
import json
from register import register
from fileCreation import fileCreation


def test_registerString():
	"""Check that register and fileCreation return the same input values
	after encoding and decoding
    
	Passes dummy values to register and creates a json file with its output.
	Decodes the json file and compares original values to the files values to
	ensure that values remain the same after decoding from the file.

    """
	json_string = register("Steve", "hellowworld", "freeEMAIL@123.com", "54119")
	file_Name = fileCreation("test.json", "test_registerString", json_string)

	with open(file_Name) as json_file:
		data = json.load(json_file)

	# This style of error testing has been used so that all the keys 
	#	will be checked for errors every time, rather then stop when one
	#	assert fails.  Output formatting has also been done to give context
	#	to any failed test.
	errors = []

	if not data["username"] == "Steve":
		errors.append("username: expected " + str(type("Steve")) + " " + "Steve" + 
							", got " + str(type(data["username"])) + " " + str(data["username"]))
	if not data["password"] == "hellowworld":
		errors.append("password: expected " + str(type("hellowworld")) + " " + "hellowworld" + 
							", got " + str(type(data["password"])) + " " + str(data["password"]))
	if not data["email"] == "freeEMAIL@123.com":
		errors.append("email: expected " + str(type("freeEMAIL@123.com")) + " " + "freeEMAIL@123.com" + 
							", got " + str(type(data["email"])) + " " + str(data["email"]))
	if not data["user_ID"] == "54119":
		errors.append("user_ID: expected " + str(type("54119")) + " " + "54119" + 
							", got " + str(type(data["user_ID"])) + " " + str(data["user_ID"]))

	assert not errors, "errors occurred:\n{}".format("\n".join(errors))

def test_registerInt():
	"""Check that integer inputs can be encoded and decoded 
	with same values and type.
    
	Passes dummy values to register and creates a json file with its output.
	Decodes the json file and compares original values to the files values to
	ensure that values remain the same after decoding from the file.

    """
	json_string = register(123, 772, 1, 8)
	file_Name = fileCreation("test.json", "test_registerInt", json_string)

	with open(file_Name) as json_file:
		data = json.load(json_file)

	errors = []

	if not data["username"] == 123:
		errors.append("username: expected " + str(type(123)) + " " + str(123) + 
							", got " + str(type(data["username"])) + " " + str(data["username"]))
	if not data["password"] == 772:
		errors.append("password: expected " + str(type(772)) + " " + str(772) + 
							", got " + str(type(data["password"])) + " " + str(data["password"]))
	if not data["email"] == 1:
		errors.append("email: expected " + str(type(1)) + " " + str(1) + 
							", got " + str(type(data["email"])) + " " + str(data["email"]))
	if not data["user_ID"] == 8:
		errors.append("user_ID: expected " + str(type(8)) + " " + str(8) + 
							", got " + str(type(data["user_ID"])) + " " + str(data["user_ID"]))

	assert not errors, "errors occurred:\n{}".format("\n".join(errors))


def test_registerStringAndInt():
	"""Check that strings and integer values can be passed and 
	retrieved successfully at the same time.
    
	Passes dummy values to register and creates a json file with its output.
	Decodes the json file and compares original values to the files values to
	ensure that values remain the same after decoding from the file.

    """
	json_string = register("name", "pass", 944, 455)
	file_Name = fileCreation("test.json", "test_registerStringAndInt", json_string)

	with open(file_Name) as json_file:
		data = json.load(json_file)

	errors = []

	if not data["username"] == "name":
		errors.append("username: expected " + str(type("name")) + " " + "name" + 
							", got " + str(type(data["username"])) + " " + str(data["username"]))
	if not data["password"] == "pass":
		errors.append("password: expected " + str(type("pass")) + " " + "pass" + 
							", got " + str(type(data["password"])) + " " + str(data["password"]))
	if not data["email"] == 944:
		errors.append("email: expected " + str(type(944)) + " " + str(944) + 
							", got " + str(type(data["email"])) + " " + str(data["email"]))
	if not data["user_ID"] == 455:
		errors.append("user_ID: expected " + str(type(455)) + " " + str(455) + 
							", got " + str(type(data["user_ID"])) + " " + str(data["user_ID"]))

	assert not errors, "errors occurred:\n{}".format("\n".join(errors))

def test_registerFalseString():
	"""Compares original values to false values to ensure that
	they are different.
    
	Passes dummy values to register and creates a json file with its output.
	Decodes the json file and compares original values to false values
	to ensure that distinction is being made.

    """
	json_string = register("what", "who", "foo", "bar")
	file_Name = fileCreation("test.json", "test_registerFalseString", json_string)

	with open(file_Name) as json_file:
		data = json.load(json_file)

	errors = []

	if not data["username"] != "foo":
		errors.append("username: expected " + str(type("foo")) + " " + "foo" + 
							", got " + str(type(data["username"])) + " " + str(data["username"]))
	if not data["password"] != "bar":
		errors.append("password: expected " + str(type("bar")) + " " + "bar" + 
							", got " + str(type(data["password"])) + " " + str(data["password"]))
	if not data["email"] != "hello":
		errors.append("email: expected " + str(type("hello")) + " " + "hello" + 
							", got " + str(type(data["email"])) + " " + str(data["email"]))
	if not data["user_ID"] != "world":
		errors.append("user_ID: expected " + str(type("world")) + " " + "world" + 
							", got " + str(type(data["user_ID"])) + " " + str(data["user_ID"]))

	assert not errors, "errors occurred:\n{}".format("\n".join(errors))
