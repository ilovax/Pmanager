import logging, coloredlogs
from create import log_config
from db_functions import connect_to_db,disconnect_from_db
from models import Account

if __name__ == "__main__":
	# config logging  
	log_config(logging,coloredlogs)

	# connecting to database
	connect_to_db('./config/db.yaml')

	# Finding all accounts
	accounts= Account.objects()
	for account in accounts:
		logging.info(f"\n[account: {account.name},\nemail: {account.email},\nusername: {account.username}]\n")

	# disconnect
	disconnect_from_db()