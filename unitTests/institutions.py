from plaid import Client

def checkInstitutionSupport(institute_query):
    """Checks whether a certain institution is supported by the API.
    Takes in a query, establishes a client using client_id, and secret
    then it searched for the institution and checks the status of 
    required features.

    Args:
        institute_query (string): a query that will be used to perform
        the search.
        
    Raises:
        Exception: Whenever a non-canadian institution is queried
        Exception: Whenever the status of authentication is not Healthy
        Exception: Whenever the status of transactions is not Healthy
        Exception: Whenever an invalid string is entered

    Returns:
        Boolean: Returns True if a queried institution is available.
    """

    credentials_file = open("apiCredentials.json")
    credentials = json.load(credentials_file)
    credentials_file.close()

    # initialize a client using client_id, and secret
    client = Client(client_id=credentials["client_id"],secret=credentials["secret"],environment=credentials["env"],suppress_warnings=True)

    # Perform institution search using query argument
    institution_info = client.Institutions.search(institute_query,products=['auth','balance','transactions'],country_codes=["CA","US"])

    # print(institution_info['institutions'][0]['country_codes'][0])
    if institution_info['institutions'][0]['country_codes'][0] != 'CA':
        raise Exception("Only Canadian banks are supported at the moment.")

    elif institution_info['institutions']:
        # check the health of the bank conncection
        institution_status = client.Institutions.get_by_id(institution_info['institutions'][0]['institution_id'],country_codes=["CA"],_options={'include_status':True})
        institution_status['institution'].pop('routing_numbers')

        if institution_status['institution']['status']['auth']['status'] != 'HEALTHY':
            raise Exception("Authentication features unavailable. Bank connection not available")
        elif institution_status['institution']['status']['transactions_updates']['status'] != 'HEALTHY':
            raise Exception("Transactions features unavailable. Bank connection not available")
        else:
            return True
    else:
        raise Exception("The specified institution is not available.")