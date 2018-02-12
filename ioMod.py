import json

## module for handing IO for the scratchy discord bot
def read_json(f):
	with open(f) as json_file: 
		data = json.load(json_file)
		print("Loading: ")
		print(data)
		return data

def write_json(obj, fp):
	with open(fp, 'w') as json_file:
		print("writing: ")
		print(obj)
		json.dump(obj, json_file, indent=4)
		
def make_backups():
	print("Making a backup of all .json files...")
	print("Done.")

def test(s):
	print(s)	
#def write_file(f, string):
	

