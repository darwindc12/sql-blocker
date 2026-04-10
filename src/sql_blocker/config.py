import configparser
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'settings.ini')

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

print("Loading config from:", CONFIG_PATH)
print("Sections found:", config.sections())

def save_config(new_values):
    config["database"]["conn_str"] = new_values['conn_str']
    config["monitor"]["kill_threshold"] = str(new_values['kill_threshold'])
    #config["monitor"]["excluded_dbs"] = new_values[['excluded_dbs']]
    #config["monitor"]["dry_run"] = str(new_values['dry_run']).lower()
    #config["schedule"]["start_time"] = new_values['start_time']
    #config["schedule"]["stop_time"] = new_values['stop_time']

    with open(CONFIG_PATH, 'w') as f:
        config.write(f)
