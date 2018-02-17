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
    
    def new(self, user, entry_name):
        data_to_init = {
            entry_name: {
                "title": "",
                "desc": "",
                "values": []
            }
        }
        
        if os.path.isfile(user.lower() + ".json"): 
            data = None
            with open(user.lower() + ".json", "r") as json_file:
                data = json.load(json_file)
                if entry_name not in data:
                    data[entry_name] = data_to_init
                else:
                    print("ERROR: ioMod: '" + entry_name + "' already in file")

            with open(user.lower() + ".json", "w") as json_file:
                if data != None:
                    json.dump(data, json_file, indent=4)            
        else:
            print("ERROR: ioMod: '" + entry_name + "' file doesn't exist") 
 
    def new_file(self, user, fp = None):
        
        data_to_init = {
            "messages": [],
        }

        if fp == None and not os.path.isfile(user.lower() + ".json"): # if not a special file and if file does not exist
            with open(user.lower() + ".json", "w+") as json_file:
                json.dump(data_to_init, json_file, indent=4)
                print("populated " + user.lower() + ".json")
        else:
            print("ERROR: ioMod: '" + user.lower() + ".json' already exists")


            
    def read(self, fp):
        if not os.path.isfile(fb): 
            print("ERROR: ioMod: '" + user.lower() + ".json' doesn't exist.")
            return;

        with open(fp) as json_file:
    	    return json.load(json_file)
    
    def read_user(self, fp):
        if not os.path.isfile(fb + ".json"):
            print("ERROR: ioMod: '" + user.lower() + ".json' doesn't exist.")
            return;

        with open(fp + ".json") as json_file:
    	    return json.load(json_file)

    def write(self, obj, fb):
        if not os.path.isfile(fb): 
            print("ERROR: ioMod: '" + user.lower() + ".json' doesn't exist.")
            return;

        with open(fb, 'w') as json_file:
    	    return json.dump(obj, json_file, indent=4)
	
    def write_user(self, obj, fb):
        if not os.path.isfile(fb + ".json"):
            print("ERROR: ioMod: '" + user.lower() + ".json' doesn't exist.")
            return;
	
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
    handle.new_file("fouric")
    handle.new("fouric", "test")
    print("I'me at: " + handle.path_to_me)
	

