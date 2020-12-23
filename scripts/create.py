import getopt, sys
import logging, coloredlogs

def log_config(loggin,coloredlogs):
	logger = logging.getLogger(__name__)
	coloredlogs.install(level='DEBUG', logger=logger)
	coloredlogs.install(fmt='%(asctime)s | %(programname)s | %(levelname)s : %(message)s')


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
	  opts, args = getopt.getopt(args,"ha:s:",["account=","secret="])
	except:
		logging.warning("Usage : create.py -a <account_name> -s <secret_word>")
		
		sys.exit(-666)
	for opt, arg in opts:
		if opt == '-h':
			logging.info("Usage : create.py -a <account_name> -s <secret_word>")
			sys.exit(-666)
		elif opt in ("-a","--account"):
			account = arg
		elif opt in ("-s","--secret"):
			secret = arg
	logging.info(f"account = {account} , secret = {secret}")
	