import json
## module for handing IO for the scratchy discord bot
class json_handler():
	def __init__(self):
		self.foo = "Hello,"

	## Demonstrate using self values in other places
	def foo_method(self, bar):
		print(self.foo + bar)
	
	def read(self, fp):
		with open(fp) as json_file:
			return json.load(json_file)

	def read_user(self, fp):
		with open(fp + ".json") as json_file:
			return json.load(json_file)

	def write(self, obj, fb):	
		with open(fb, 'w') as json_file:
			return json.dump(obj, json_file, indent=4)
	
	def make_backups(self, files=None):
		print("Creating backups.")

'''
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
'''

def test(s):
	print(s)	

if __name__ == "__main__":
	print("We are main.")
	handle = json_handler()
	handle.foo_method(" world!");
	
#def write_file(f, string):

