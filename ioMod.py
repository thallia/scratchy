import json
import os
from datetime import datetime
from shutil import copyfile

## module for handling IO for the scratchy discord bot
class json_handler():
    def __init__(self):
        self.foo = "Hello,"
        self.path_to_me = os.getcwd()
        self.backup_folder = self.path_to_me + "/backups/"
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
	
    def write_user(self, obj, fb):	
    	with open(fb + ".json", 'w') as json_file:
    	    return json.dump(obj, json_file, indent=4)

    def make_backup(self, files=None):
        print("Creating backups.")
        current_files = os.listdir(self.path_to_me)
        time = datetime.now().strftime('%Y-%m-%d-%H:%M')
        
        if files != None:
            if type(files) == list:
                for f in files:
                    if type(f) == str:
                        if open(f):
                            copyfile(f, self.backup_folder + f + time)
                            return;
                        else:
                             raise "ioMod: make_backup: Invalid file name"
                             return;
                    else:
                        raise "ioMod: make_makup: "
                        return;
            else:
                raise "ioMod: 'make_backup()' takes a list of file strings."
                return;                      

        for f in current_files:
            if f.endswith(".json"):
                print("Copying: " + f)
                copyfile(f, self.backup_folder + f + time)

        print("Done.")

    #def backup_user(self, files

def test(s):
    print(s)	

if __name__ == "__main__":
    print("We are main.")
    handle = json_handler()
    handle.foo_method(" world!");
    #handle.make_backup()
    print("I'me at: " + handle.path_to_me)
	

