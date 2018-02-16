# module for handling the help commanda

with open('help.json') as json_data:
    h = json.load(json_data)
    print(h)

class help_meh():

    def display_commands(self):
        # display commands
        i = 0
        for i = 0 and i < 9:
            await bot.send_message(message.channel, all_commands.i)
            i++

    def all(self): # if @help all
        #cat the full on file into discord
        await bot.send_message(message.channel, )

    def with_grab(self): # if @help grab
        #only the grab command: syntax - parameters - description
        testmsg = "grabbing information..."
        await bot.send_message(message.channel, testmsg)
        # grab the name...
        await bot.send_message(message.channel, h.grab.command)
        # grab the syntax...
        await bot.send_message(message.channel, h.grab.syntax)
        #grab the description...
        await bot.send_message(message.channel, h.grab.description)


    def with_add(self):
        #add command: syntax - parameters - description

    def with_show(self):
        # add command : syntax - params - description
