import getopt, sys
import logging, coloredlogs
import string, random
from hashlib import sha1
from db_functions import connect_to_db,disconnect_from_db
from models import Account
from crypt_functions import crypt

# to config the logging format and adding coloring 
def log_config(loggin, coloredlogs):
	logger = logging.getLogger(__name__)
	coloredlogs.install(level='DEBUG', logger=logger)
	coloredlogs.install(fmt='%(asctime)s | %(programname)s | %(levelname)s : %(message)s')

# somme of characters code of a single word 
def char_code_somme(word):
	somme = 0
	for i in word:
		somme += ord(i)
	return somme

# Creating random password
def create_pass(secret):
	# seed the radnom generator
	randint = random.randint(0,99999999999)
	random.seed(char_code_somme(secret)+randint)

	password_length = 15 + len(secret)
	random_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+-<=>?@[]^_{|}~'
	
	# create random string to use it for password creation
	random_list = [random.choice(random_chars + secret) for i in range(password_length)]
	random_str = ' '.join(random_list)

	# create password from sha1 of the radnom string
	password = sha1(random_str.encode()).hexdigest()
	return password

def print_help(msgs):
	print('COMMAND LINE OPTIONS')
	for msg in msgs:
		print(f'\t {msg}')

def get_options(args, account, secret, username, email):

	# If user didn't supply options 
	if len(args) == 0 :
		logging.warning("Usage : create.py -a <account_name> -s <secret_word>")
		logging.info("Use -h to show help menu")
		# using costume exit status number
		sys.exit(-666)
	
	try:
	  opts, args = getopt.getopt(args,"ha:s:u:e:",["help","account=","secret=","username=","email="])
	except:
		logging.warning("Usage : create.py -a <account_name> -s <secret_word>")
		logging.info("Use -h to show help menu")
		sys.exit(-666)
	
	for opt, arg in opts:
		if opt in ("-h","--help"):
			logging.info("Usage : create.py -a <account_name> -s <secret_word>")
			print_help(help_msgs)
			sys.exit()
		elif opt in ("-a","--account"):
			account = arg 
		elif opt in ("-s","--secret"):
			secret = arg
		elif opt in ("-u","--username"):
			username = arg
		elif opt in ("-e","--email"):
			email = arg
	return account,secret,username,email
	
def save_account(name, password, username, email):
	password,iv = crypt(password)
	account = Account(name=name, password=password, username=username, email=email, iv=iv)
	account.save()
	
def check_name_email(name, email):
	accounts = Account.objects(email=email, name=name)
	return len(accounts)

if __name__ == "__main__":
	# config logging  
	log_config(logging,coloredlogs)

	# Default help menu entries
	help_msgs = [
		"-h,--help : Display help menu",
		"-a,--account : Account name [default=>'empty']",
		"-s,--secret : Secret word for password randomization [default=>'empty']",
		"-u,--username : Account username [default=>'']",
		"-e,--email : Account email [default=>'example@gmail.com']"]
	
	# getting the options 
	args = sys.argv[1:]
	account = "empty"
	secret = "empty"
	username = ""
	email = "example@gmail.com"
	account,secret,username,email = get_options(args, account, secret, username, email)
	
	# creating password 
	password = create_pass(secret)
	
	# connecting to database
	connect_to_db('./config/db.yaml')
	logging.info(f"account = {account} , password = {password}, username = {username}, email = {email}")
	
	# check if  (name and email) exist 
	if check_name_email(account, email):
		logging.warning(f"You already have {account} with {email} as an email")
		sys.exit()


	# Crypting password and saving the account
	save_account(account, password, username, email)
	
	# disconnect
	disconnect_from_db()