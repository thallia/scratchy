import json
import os
import time
from datetime import datetime
from shutil import copyfile

## module for handling IO for the scratchy discord bot
class json_handler():
    foo = "Hello "
    path_to_me = os.getcwd()
    backup_folder = path_to_me + "/backups/"
    data_folder = path_to_me + "/data/"
    ## Demonstrate using self values in other places

    def verify_file(self, f):
        if not os.path.isfile(fp): 
            print("ERROR: ioMod: '" + user.lower() + ".json' doesn't exist.")
            return False;
        else:
            return True;

    def foo_method(self, bar):
    	print(self.foo + bar)

    def remove_entry(self, user, entry_name, value):
        if entry_name == "messages":
            return "You can't delete the `messages` list."

        if os.path.isfile(user.lower() + ".json"):
            # Do stuff
            with open(self.data_folder + user.lower() + ".json") as json_file:
                data = json.load(json_file)
                if entry_name in data and len(data[entry_name]["values"]) > value:
                    string_at_value = data[entry_name]["values"][value]
                    data[entry_name]["values"].remove(string_at_value)
                    self.write_user(data, user.lower())
                    return "Successfully removed '{}' from '{}'.".format(string_at_value, entry_name)
                else:
                    return "Unable to remove value, are you sure {} exists?".format(entry_name)

        else:
            return "ERR: User file doesn't have a scratchpad! Try running the `@new` command to automatically create a scratchpad."

    def new(self, user, entry_name):
        data_to_init = {
            "title": entry_name,
            "desc": "",
            "values": []
        }
        
        if os.path.isfile(self.data_folder + user.lower() + ".json"): 
            data = None
            with open(self.data_folder + user.lower() + ".json", "r") as json_file:
                data = json.load(json_file)
                if entry_name not in data:
                    data[entry_name] = data_to_init
                else:
                    print("ERROR: ioMod: '" + entry_name + "' already in file")

            with open(self.data_folder + user.lower() + ".json", "w") as json_file:
                if data != None:
                    json.dump(data, json_file, indent=4)            
                    self.make_backup()
        else:
            print("ERROR: ioMod: '" + entry_name + "' file doesn't exist") 
 
    def new_file(self, user, fp = None):
        
        data_to_init = {
            "messages": [],
        }

        if fp == None and not os.path.isfile(self.data_folder + user.lower() + ".json"): # if not a special file and if file does not exist
            with open(self.data_folder + user.lower() + ".json", "w+") as json_file:
                json.dump(data_to_init, json_file, indent=4)
                print("populated " + user.lower() + ".json")
        else:
            print("ERROR: ioMod: '" + user.lower() + ".json' already exists")


            
    def read(self, fp):
        self.verify_file(fp)

        with open(fp) as json_file:
    	    return json.load(json_file)
    
    def read_user(self, fp):
        if not os.path.isfile(self.data_folder + fp + ".json"):
            print("ERROR: ioMod: '" + user.lower() + ".json' doesn't exist.")
            return None;

        with open(self.data_folder + fp + ".json") as json_file:
    	    return json.load(json_file)

    def write(self, obj, fp):
        if not os.path.isfile(fp): 
            print("ERROR: ioMod: '" + user.lower() + ".json' doesn't exist.")
            return;

        with open(fp, 'w') as json_file:
    	    return json.dump(obj, json_file, indent=4)
	
    def write_user(self, obj, fp):
        if not os.path.isfile(self.data_folder + fp + ".json"):
            print("ERROR: ioMod: '" + user.lower() + ".json' doesn't exist.")
            return;
	
        with open(self.data_folder + fp + ".json", 'w') as json_file:
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
                            copyfile(f, self.backup_folder + time + f)
                            return;
                        else:
                             return "ioMod: make_backup: Invalid file name";
                    else:
                        return "ioMod: make_makup: ";
            else:
                return "ioMod: 'make_backup()' takes a list of file strings.";                      

        for f in current_files:
            if f.endswith(".json"):
                print("Copying: " + f)
                copyfile(f, self.backup_folder + time + f)

        print("Done.")
    
    def cleanup_backups(self):
        print("Removing old backups...")
        backups = os.listdir(self.backup_folder)
        now = time.time()
        
        one_day_ago = now - 60*60*24

        for backup in backups:
            print(backup)
            file_time = os.path.getctime(self.backup_folder + backup)
            if file_time < one_day_ago:
                print("Found old backup: ")
                print(backup)
                os.remove(self.backup_folder + backup)
        print("Done.")
                
        
        
    #def backup_user(self, files

def test(s):
    print(s)	

if __name__ == "__main__":
    print("We are main.")
    handle = json_handler()
    handle.foo_method(" world!");
    #handle.make_backup()
    print("-"*20)
    handle.cleanup_backups()
    print("-"*20)
    handle.new_file("test_user")
    handle.new("test_user", "test")
    #remove_entry(user, entry_name, value):
    print(handle.remove_entry("test_user", "test", 0))
    print("I'm at: " + handle.path_to_me)
	

