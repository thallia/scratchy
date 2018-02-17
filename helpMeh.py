# module for handling the help command
import json

class help_meh():

    with open('help.json') as json_file:
        h = json.load(json_file)
        print("Successfully loaded help.json.")

    #def display_commands(self):
        # display commands
        #i = 0
        #for i == 0 and i < 9:
         #   await bot.send_message(message.channel, h.all_commands.i)
          #  i++

    #def all(self): # if @help all
        #cat she full on file into discord
        #await bot.send_message(message.channel, )

    def with_grab(self): # if @help grab
        #only the grab command: syntax - parameters - description
        # grab the name...
        print(grab)
        # grab the syntax...
        print(grab.syntax)
        #grab the description...
        print(grab.description)


    #def with_add(self):
        #add command: syntax - parameters - description

    #def with_show(self):
        # add command : syntax - params - description
