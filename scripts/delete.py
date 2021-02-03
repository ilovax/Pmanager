import getopt, sys
import logging, coloredlogs
from create import log_config, check_name_email, print_help
from db_functions import connect_to_db,disconnect_from_db
from models import Account

def get_options(args, account, email, help_msgs):

	# If user didn't supply options 
	if len(args) == 0 :
		logging.warning("Usage : delete.py -a <account_name> -e <email_address>")
		logging.info("Use -h to show help menu")
		# using costume exit status number
		sys.exit(-666)
	
	try:
	  opts, args = getopt.getopt(args,"ha:e:",["help","account=","email="])
	except:
		logging.warning("Usage : delete.py -a <account_name> -e <email_address>")
		logging.info("Use -h to show help menu")
		sys.exit(-666)
	
	for opt, arg in opts:
		if opt in ("-h","--help"):
			logging.info("Usage : delete.py -a <account_name> -e <email_address>")
			print_help(help_msgs)
			sys.exit()
		elif opt in ("-a","--account"):
			account = arg 
		elif opt in ("-e","--email"):
			email = arg
	return account, email
	

if __name__ == "__main__":
    # config logging  
	log_config(logging,coloredlogs)

    # Default help menu entries
	help_msgs = [
		"-h,--help : Display help menu",
		"-a,--account : Account name [Required]",
		"-e,--email : Account email [default=>'example@gmail.com']"]
    
    # getting the options 
	args = sys.argv[1:]
	account = ""
	email = "example@gmail.com"
	account, email = get_options(args, account, email, help_msgs)

    # connecting to database
	connect_to_db('./config/db.yaml')
	logging.info(f"account = {account}, email = {email}")

    # check if  (name and email) exist 
	if not check_name_email(account, email):
		logging.warning(f"You don't have {account} with {email} as an email")
		sys.exit()

    # Delete the account/email pair  
	account = Account.objects(email=email, name=account)
	account.delete()
	
	# disconnect
	disconnect_from_db()