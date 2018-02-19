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
ioMod.test("Hello, World!")
test = ioMod.read_json("data.json")
ioMod.write_json(data_to_json, "data2.json")
'''
class help_meh():
    def __init__ (self):
        with open('help.json') as json_data:
            self.h = json.load(json_data)
            print(h)
'''

# Test line.
