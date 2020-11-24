import re
import datetime
import plaid

class accountBalance:
	def __init__(self,data):
		"""[summary]

		Args:
			data ([type]): [description]
		"""
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

class tokenAccountInfo:
	def __init__(self,data):
		"""[summary]

		Args:
			data ([type]): [description]
		"""
		self.raw_data = data
		self.institution_id = data['item']['institution_id']
		self.consent_expiration_time = data['item']['consent_expiration_time']
		self.last_failed_update = data['status']['transactions']['last_failed_update']
		self.last_successful_update = data['status']['transactions']['last_successful_update']

class accountOwnerIdentity:
	def __init__(self,data):
		"""[summary]

		Args:
			data ([type]): [description]
		"""
		self.raw_data = data
		self.owner_names = data['names']
		self.owner_emails = data['email']

class accountTransactions:
	def __init__(self,data):
		"""[summary]

		Args:
			data ([type]): [description]
		"""
		self.raw_data = data
		self.date = data['date']
		self.account_id = data['account_id']
		self.transaction_id = data['transaction_id']
		self.status_pending = data['pending']
		self.merchant_name = data['merchant_name']
		self.category = data['category']
		self.amount = data['amount']
		self.currency_code = data['iso_currency_code']

class institutionsStatus:
	def __init__(self,ins_id_search_data):
		"""[summary]

		Args:
			ins_id_search_data ([type]): [description]
		"""
		self.raw_data = ins_id_search_data
		self.institution_id = ins_id_search_data['institution_id']
		self.available_products = ins_id_search_data['products']
		self.institution_item_login_status = ins_id_search_data['status']['item_logins']['status']
		self.transactions_status = ins_id_search_data['status']['transactions_updates']['status']
		self.balance_status = ins_id_search_data['status']['balance']['status']

class PlaidAPI():
	def __init__(self, client_id:str, secret:str, environment:str, supress_warnings=True):
		"""[summary]

		Args:
			client_id (str): [description]
			secret (str): [description]
			environment (str): [description]
			supress_warnings (bool, optional): [description]. Defaults to True.
		"""
		self.client = plaid.Client(client_id, secret, environment, supress_warnings)

	def getLinkToken(self) -> str:
		"""[summary]

		Returns:
			str: [description]
		"""
		return self.client.post('/link/token/create', {'user' {'client_user_id': 'BankingStack1'},
													   'client_name': 'BankingStack',
													   'country_codes': ['CA'],
													   'language': 'en',
													   'products': ['balance','transactions']
													   }
								)['link_token']
		
	def echangePublicToken(self, public_token: str) -> str:
		"""[summary]

		Args:
			public_token (str): [description]

		Returns:
			str: [description]
		"""
		return self.client.Item.public_token.exchange(public_token)
	
	def getUpdatedToken(self, access_token: str) -> str:
		"""[summary]

		Args:
			access_token (str): [description]

		Returns:
			str: [description]
		"""
		return self.client.post('/item/public_token/create', {'access_token': access_token,})['public_token']
	
	# def getAccountInfo(self, access_token: str) -> Account