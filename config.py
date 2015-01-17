
import json

CONFIG_FILE = 'client_config.json'

def get():
	with open(CONFIG_FILE, 'r') as f:
		return json.load(f)


if __name__ == '__main__':
  print get()