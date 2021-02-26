import getopt, sys
import logging, coloredlogs
from create import log_config, check_name_email, print_help, create_pass
from db_functions import connect_to_db,disconnect_from_db
from models import Account
from crypt_functions import crypt

def get_options(args, account, email, new_password, help_msgs):

	# If user didn't supply options 
	if len(args) == 0 :
		logging.warning("Usage : -a <account_name> -e <email_address> -p <password>")
		logging.info("Use -h to show help menu")
		# using costume exit status number
		sys.exit(-666)
	
	try:
	  opts, args = getopt.getopt(args,"ha:e:p:",["help","account=","email=","password="])
	except:
		logging.warning("Usage : -a <account_name> -e <email_address> -p <password>")
		logging.info("Use -h to show help menu")
		sys.exit(-666)
	
	for opt, arg in opts:
		if opt in ("-h","--help"):
			logging.info("Usage : -a <account_name> -e <email_address> -p <password>")
			print_help(help_msgs)
			sys.exit()
		elif opt in ("-a","--account"):
			account = arg 
		elif opt in ("-e","--email"):
			email = arg
		elif opt in ("-p","--passowrd"):
			new_password = arg
	return account, email, new_password

if __name__ == "__main__":
	# config logging  
	log_config(logging,coloredlogs)

	# Default help menu entries
	help_msgs = [
		"-h,--help : Display help menu",
		"-a,--account : Account name [Required]",
		"-e,--email : Account email [default=>'example@gmail.com']",
		"-p,--password: New password for the account [default=> random password (using fixed secret)]"]

	# getting the options 
	args = sys.argv[1:]
	# creating password 
	new_password = create_pass("random")
	account = ""
	email = "example@gmail.com"
	account, email, new_password = get_options(args, account, email, new_password, help_msgs)

	# connecting to database
	connect_to_db('./config/db.yaml')
	logging.info(f"account = {account}, email = {email}")

	# check if  (name and email) exist 
	if not check_name_email(account, email):
		logging.warning(f"You don't have '{account}' account with {email} as an email")
		sys.exit()

	# Edit password for the account/email pair  
	new_password, iv = crypt(new_password)
	Account.objects(email=email, name=account).update_one(set__password=new_password,set__iv=iv)

	logging.info(f"Password had been changed ✔️")
	# disconnect
	disconnect_from_db()