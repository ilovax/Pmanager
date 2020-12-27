import getopt, sys
import logging, coloredlogs
import string, random
from hashlib import sha1
from db_functions import connect_to_db

# to config the logging format and adding coloring 
def log_config(loggin,coloredlogs):
	logger = logging.getLogger(__name__)
	coloredlogs.install(level='DEBUG', logger=logger)
	coloredlogs.install(fmt='%(asctime)s | %(programname)s | %(levelname)s : %(message)s')

# somme of characters code of a single word 
def char_code_somme(word):
	somme = 0
	for i in word:
		somme += ord(i)
	return somme

# if arguments are empty use  the string empty
def create_pass(account="empty",secret="empty"):
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

if __name__ == "__main__":
	# config logging  
	log_config(logging,coloredlogs)

	# getting the options 
	args = sys.argv[1:]
	account = ""
	secret = ""
	
	if len(args) == 0 :
		logging.warning("Usage : create.py -a <account_name> -s <secret_word>")
		# using costume exit status number
		sys.exit(-666)
	
	try:
	  opts, args = getopt.getopt(args,"ha:s:",["help","account=","secret="])
	except:
		logging.warning("Usage : create.py -a <account_name> -s <secret_word>")
		sys.exit(-666)
	
	for opt, arg in opts:
		if opt in ("-h","--help"):
			logging.info("Usage : create.py -a <account_name> -s <secret_word>")
			sys.exit(-666)
		elif opt in ("-a","--account"):
			account = arg
		elif opt in ("-s","--secret"):
			secret = arg
	# creating password 
	password = create_pass(account,secret)
	logging.info(f"account = {account} , password = {password}")
	
	# connecting to database
	connect_to_db('./config/db.yaml')
	