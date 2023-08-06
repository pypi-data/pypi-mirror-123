import yaml
import os
from neo4j import GraphDatabase

TWNEO_CONFIG = []
config_path = os.environ['twneo_config_path'] if 'twneo_config_path' in os.environ else "/Users/pankaj/dev/git/twneo/twneo/config/config_dev.yaml"
if not os.path.exists(config_path):
    print("config path does not exist using default config_yaml")
    config_path = "config.yaml"

with open (config_path ) as f :
    TWNEO_CONFIG = yaml.load(f)

def get_graph_driver():
    global TWNEO_CONFIG
    TWNEO_CONFIG=TWNEO_CONFIG['TWNEO_CONFIG']
    uri = TWNEO_CONFIG['NEO4J']['uri']
    user = TWNEO_CONFIG['NEO4J']['user']
    password = TWNEO_CONFIG['NEO4J']['password']
    driver = GraphDatabase.driver(  uri, auth=( user, password))
    return driver