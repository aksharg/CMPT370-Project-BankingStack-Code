import json

def register(username, password, email, user_ID):
	"""Register the user

	Stores args in a dictionary which is converted into a json string 
	for storage.

    Args:
		username: A string containing the user's username
        password: A string containing the user's password
		email: A string containing the user's email
		user_ID: An integer containing the user's given ID
    Returns:
		A json string that contains the user's registration information
		which will be saved to a json file.

    """
	register = {"username": username,
			"password": password,
			"email": email,
			"user_ID": user_ID}
	
	json_string = json.dumps(register)
	return json_string
