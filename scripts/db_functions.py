from mongoengine import connect
import yaml

def connect_to_db(db_config_file_name="../config/db.yaml"):
    # getting config params from db.yaml 
    with open(db_config_file_name) as db_yaml:
        db_conf = yaml.load(db_yaml, Loader=yaml.FullLoader)
        db = db_conf["db"]
        username = db_conf["username"]
        password = db_conf["password"]
        host = db_conf["host"]
        port = int(db_conf["port"])
    
    # Connecting
    connect(db=db, username=username, password=password, host=host, port=port)
