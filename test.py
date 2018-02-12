import ioMod
import json
import sys

data1 = {
	'title': "Scratchy",
	"desc": "Discord bot for managing user scratchpads",
	"values": ["It's awesome.", "Hello, world!", "Food is good."]
}

data2 = {
	'title': "EET-139 notes",
	"desc": "Some notes from the worst class ever.",
	"values": ["He draws LEDs with circles around them and the arrows pointing up.", 
		"Textbook is horrible.",
		"Food is good."]
}

data_to_json = {
	"scratchy": data1,
	"eet139": data2
}

'''
	I intent to make the json_handler useful in such a way that you will make a new instance of the json_handler for every user. 
Ideally, the json handler would smartly handle the user files in a non-destructive fashion, I'm going to try and make it automatically save/backup
files when they are opened/closed, and since I believe there is an opposite to the __init__ function, it should be possible to execute code when 
the program is stopped. Eg, saving any unsaved changes.
'''
handler = ioMod.json_handler() # make a new json_handler object

ioMod.test("Hello, World!") # Demonstration of calling a function that's part of a module
handler.foo_method(" world") # Demonstration of calling a function that's part of a class/object

print(handler.read("data2.json")) # Read
handler.write(data_to_json, "data2.json") # Write

# The thing is, the json libary "dump" only returns None or it fails. A smart definition would return ether success or an error, but do it in such a way
# 	that it wouldn't break the program. In rust, this is done with a vlaue "pair", which I might end up implementing for this. Alnternatively, for 
# 	failures we can use the built-in error catching, while not as elegant imo, still works great.

