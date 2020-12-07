import re
import datetime
import plaid
import json

class accountBalance:
	def __init__(self,data):
		self.raw_data = data
		self.account_id = data['account_id']
		self.account_name = data['name']
		self.account_type = data['type']
		self.account_subtype = data['subtype']
		self.account_number = data['mask']
		self.currency_code = data['balances']['iso_currency_code']
		self.balance_current = data['balances']['current']
		self.balance_available = data['balances']['available']
		self.balance_limit = data['balances']['limit']
	
	def __str__(self):
		return str(self.__class__)+": "+str(self.__dict__)

class tokenAccountInfo:
	def __init__(self,data):
		self.raw_data = data
		self.institution_id = data['item']['institution_id']
		self.consent_expiration_time = data['item']['consent_expiration_time']
		self.last_failed_update = data['status']['transactions']['last_failed_update']
		self.last_successful_update = data['status']['transactions']['last_successful_update']

	def __str__(self):
		return str(self.__class__)+": "+str(self.__dict__)		

class accountTransaction:
	def __init__(self,data):
		self.raw_data = data
		self.date = data['date']
		self.account_id = data['account_id']
		self.transaction_id = data['transaction_id']
		self.status_pending = data['pending']
		self.merchant_name = data['merchant_name']
		self.description = data['name']
		self.category = data['category']
		self.amount = data['amount']
		self.currency_code = data['iso_currency_code']
	
	def to_json(self):
		return json.dumps(self, default=lambda o: o.__dict__, indent=4)
	
	def __str__(self):
		return str(self.__class__)+": "+str(self.__dict__)

class institutionsStatus:
	def __init__(self,ins_id_search_data):
		self.raw_data = ins_id_search_data
		self.institution_id = ins_id_search_data['institution']['institution_id']
		self.available_products = ins_id_search_data['institution']['products']
		self.institution_item_login_status = ins_id_search_data['institution']['status']['item_logins']['status']

		if any("transactions" in products for products in self.available_products):
			self.transactions_status = ins_id_search_data['institution']['status']['transactions_updates']['status']
		else:
			self.transactions_status = None
	
def raise_plaid(ex: plaid.errors.ItemError):
    if ex.code == 'NO_ACCOUNTS':
        raise PlaidNoApplicableAccounts(ex)
    elif ex.code == 'ITEM_LOGIN_REQUIRED':
        raise PlaidAccountUpdateNeeded(ex)
    else:
        raise PlaidUnknownError(ex)

def wrap_plaid_error(f):
    def wrap(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except plaid.errors.PlaidError as ex:
            raise_plaid(ex)
    return wrap

class PlaidError(Exception):
    def __init__(self, plaid_error):
        super().__init__()
        self.plaid_error = plaid_error
        self.message = plaid_error.message

    def __str__(self):
        return "%s: %s" % (self.plaid_error.code, self.message)

class PlaidUnknownError(PlaidError):
    pass

class PlaidNoApplicableAccounts(PlaidError):
    pass

class PlaidAccountUpdateNeeded(PlaidError):
    pass

class plaidAPI():
	def __init__(self, client_id:str, secret:str, environment:str, supress_warnings=True):
		self.client = plaid.Client(client_id, secret, environment, supress_warnings)

	@wrap_plaid_error
	def getLinkToken(self):
		return self.client.post('/link/token/create', {'user': {'client_user_id': 'BS1'},
		'client_name': 'BankingStack',
		'country_codes': ['CA'],
		'language': 'en',
		'products': ['transactions']})['link_token']
	
	@wrap_plaid_error
	def exchangePublicToken(self, public_token):
		return self.client.Item.public_token.exchange(public_token)
	
	@wrap_plaid_error
	def getUpdatedToken(self, access_token):
		return self.client.post('/item/public_token/create', {'access_token': access_token,})['public_token']
	
	@wrap_plaid_error
	def getTokenAccountInfo(self, access_token):
		resp = self.client.Item.get(access_token)
		return tokenAccountInfo(resp)

	@wrap_plaid_error
	def getAccountBalance(self,access_token):
		response = self.client.Accounts.balance.get(access_token=access_token)
		balance_list = list(map(accountBalance, response['accounts']))
		return balance_list
	
	@wrap_plaid_error
	def getAccountTransactions(self, access_token, start_date, end_date, account_ids=None, status_callback=None):
		ret = []
		total_transactions = None
		while True:
			response = self.client.Transactions.get(
							access_token,
							start_date.strftime("%Y-%m-%d"),
							end_date.strftime("%Y-%m-%d"),
							account_ids=account_ids,
							offset=len(ret),
							count=500)

			total_transactions = response['total_transactions']

			ret += [
				accountTransaction(t)
				for t in response['transactions']
			]

			if status_callback: status_callback(len(ret), total_transactions)
			if len(ret) >= total_transactions: break
		return ret

	@wrap_plaid_error
	def getInstitution(self,institution_query):
		query_response = self.client.Institutions.search(institution_query,products=['auth','balance','transactions'],country_codes=["CA","US"])
		institution_id = query_response['institutions'][0]['institution_id']
		id_search_response = self.client.Institutions.get_by_id(institution_id,country_codes=["CA","US"],_options={'include_status':True})
		institution_status = institutionsStatus(id_search_response)
		return institution_status
	
	@wrap_plaid_error
	def removeAccount(self,access_token):
		return self.client.Item.remove(access_token)

	

