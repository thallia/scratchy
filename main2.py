import discord
from discord.ext import commands
import json
import sys
import asyncio
import ioMod
import os
from collections import deque
import helpMeh
from helpMeh import help_meh

description = "scratchpad bot"
path = "/home/thallia/code/scratchy/"
file_token = "/home/thallia/key/scratchy-discord-token.txt"
prefix = "@"
if os.getcwd().find("gector"):
    file_token = "/home/gector/key.txt"

token = ""

commands = [       # created just so I know what commands we have so far/commands we want to integrate
    "!lastmessage" # for individual scratchpads
    "!set"
    "!add"
    "!test"
    "!pin"         # for pinned messages on discord in a public file for anyone to access: should document the channel, who said it, and the message/link
]

users = {
    "gector": [],
    "thallia": [],
    "fouric": [],
    "jay": [],
    "uelen": [],
    "galois": []
}

def find_quote(msg_list, index = 0):
    for x in msg_list[index:]:
        print(x)
        if x.find('"') != -1:
            return msg_list.index(x)

def new(data=None, arg=None):
    handler = ioMod.json_handler()
    try:
        data = handler.read_user(msg_author)
        if data == None:
            # new_file(user, fp = None)
            handler.new_file(msg_author)
            data = handler.read_user(msg_author)
    
        # new(user, entry_name):
        handler.new(msg_author, arg)
        return "Success! Try `{}show {}` to display your new scratchpad entry".format(prefix, arg)
    except Exception as e:
        if debug:
            return "Error: {}".format(e);
        else:
            return "Unable to complete request! Please contact a developer."


def show(data=None, subject = None):
    show_all = False;
    fill_me = ""
    if subject != None and subject != []:
        if set(subject).issubset(data):
            data = {key:data[key] for key in subject}
            print("Data: {}, \nSubject: {}".format(data, subject))
            show_all = True;
            fill_me = ""
        else:
            return "Invalid request, subject not in file"

    for field in data.values():
        #await bot.send_message(message.channel, field)
        #print(field)
        if type(field) == list or type(field) == dict and show_all:
            fill_me += "```"
            for element in field:
                indent = ''
                value = field[element]
                if type(value) == str:
                    fill_me += element + ": " + value + "\n"
                elif type(value) == list:
                    indent = 6*' '
                    fill_me += element + ": " + "\n" + indent
                    for x in range(0, 9):
                        if x < len(value) and value[x] != None:
                            fill_me += "({}) ".format(x) + "\"" + value[x] + "\"\n" + indent
        elif show_all == False:
            fill_me = "```\n"
            for f in data.values():
                if type(f) == dict:
                    print(f['title'])
                    fill_me += f['title'] + "\n"
            fill_me += "```"
            return fill_me

        fill_me += "```"

    return (fill_me)

def parse_args(args):
   

with open(file_token, 'r') as file:      # *takes all of gector's code*
    token = file.readline(100).strip()
print("Bot token: " + token)

bot = discord.Client()

@bot.event  # must confirm the connection when it's done connecting
async def on_ready():
    print("Connected!")
    print("Username: " + bot.user.name)
    print("-----------------")

@bot.event
async def on_message(message):
    data = 0;
    user = ioMod.json_handler()
    author = message.author.name.lower()
    messages = bot.messages
    helpmeh = help_meh()
    title = ""

    global msg_author
    global msg_chan
    global msg_content

    msg_content = message.content
    msg_author = message.author.name.lower()
    msg_chan = message.channel


    def write_the_dang_thing():
        if users[message.author.name.lower()] !=-1: # for the object in that user's file....
            data[title].insert(0, usermessage.content) # inserts the message into the file
            user.write(0, data, author + ".json") # writes the file

    if message.author.name.lower() == "scratchy":   # prevents triggering of self
        return

    if message.content.startswith(prefix + "show"):
        message_args = message.content.split(" ")
        arg1 = None
        try:
            arg1 = message_args[1:]
        except Exception as e:
            print("no argrument")

        data = None;
        handler = ioMod.json_handler()
        try:
            data = handler.read_user(message.author.name.lower())
        except Exception as e:
            print("ERROR: Failed to read user '{}', does their file exist?".format(message.author.name.lower()))
            await bot.send_message(message.channel, e)
            return;

        if arg1 != "" or arg1 != None:
            await bot.send_message(message.channel, show(data = data, subject = arg1))
        else:
            await bot.send_message(message.channel, show(data = data))

    if msg_content.startswith(prefix + "new"):
        message_args = msg_content.split(" ")
        arg1 = None

        try:
            arg1 = str(message_args[1].strip())
        except Exception as e:
            await bot.send_message(msg_chan, "Err: Unable to parse args. Are you using `new <entry_name>`?") # Report error
            await bot.send_message(msg_chan, "{}".format(e))
            return

        result = new(arg=arg1)
        await bot.send_message(msg_chan, result)


    if msg_content.startswith(prefix + "set"):
        # set <entry> <field> <value>
        message_args = msg_content.split(" ")
        arg1, arg2, arg3 = None, None, None # Way of assignming multiple variables at once.

        try:
            arg1 = str(message_args[1].strip()) # entry
            arg2 = str(message_args[2].strip()) # field

            index1 = find_quote(message_args)
            index2 = find_quote(message_args, index1+1)
            print(message_args[index1+1:])
            print("Index1: {}, index2: {}".format(index1, index2))

            if index2 != None:
                arg3 = ' '.join(message_args[index1:index2+1]).replace('"', "")
            else:
                arg3 = ' '.join(message_args[index1:]).replace('"', "")

            print(arg3)
        except Exception as e:
            await bot.send_message(msg_chan, "Err: Unable to parse args. Are you using `set <entry_name> <field_name> <value>`?") # Report error
            return

        data = None
        handler = ioMod.json_handler()
        try:
            data = handler.read_user(msg_author)
            if arg2 != "values":
                data[arg1][arg2] = arg3
                # write_user(obj, user)
                handler.write_user(data, msg_author)
            elif arg2 == "values":
                data[arg1][arg2].insert(0, arg3)
                handler.write_user(data, msg_author)

            await bot.send_message(msg_chan, "Success! Try `{}show {}` to display your new scratchpad entry".format(prefix, arg1))
        except Exception as e:
            await bot.send_message(msg_chan, "Err: Unable to parse data. '{}'".format(e))
            return


    if msg_content.startswith(prefix + "upload_scratch"):
        if os.path.isfile(msg_author + ".json"):
            await bot.send_message(msg_chan, "Uploading your scratchpad...")
            await bot.send_file(msg_chan, os.getcwd() + "/" + msg_author + ".json")
        else:
            await bot.send_message(msg_chan, "Err: Unable to upload file, check to make sure it exists.")



    if msg_content.startswith(prefix + "upload_scratch"):
        if os.path.isfile(msg_author + ".json"):
            await bot.send_message(msg_chan, "Uploading your scratchpad...")
            await bot.send_file(msg_chan, os.getcwd() + "/" + msg_author + ".json")
        else:
            await bot.send_message(msg_chan, "Err: Unable to upload file, check to make sure it exists.")


    '''
    if message.content.startswith(prefix + "grab"): # checks for the trigger command
        user = ioMod.json_handler
        data = user.read_user(0, author)
<<<<<<< HEAD
        usr_prefix = "usr:"
        title_prefix = "t:"
        num_prefix = "num:"
        messageargs = message.content.split(" ")

        if message.content.lower().find(usr_prefix) !=-1:
            



        #        while i > 0:
        #   messages.rotate(rotate)
        #  usermessage = messages.pop()
        #    write_the_dang_thing()
        #    if i != 0:
        #        x = rotate - 1
        #        rotate = rotate * -1
        #        messages.rotate(rotate)
        #        rotate = x
        #        messages.rotate(rotate)
        #        i - 1
        #    elif i == 0:
        #        await bot.send_message(message.channel, "written to " + author + "'s scratchpad!")
=======
	arg1, arg2, arg3 = [0, 0, 0]
        rotate = 0
        before_rotate = 0
        messages_from = 0
        messageargs = message.content.split(" ")

        arg1 = messageargs[1].strip()
        try:
            arg2 = messageargs[2].strip()
        except Exception:
            arg2 = None
        try:
            arg3 = messageargs[3].strip()
        except Exception:
            arg3 = None

        print("before: " + str(arg1))
        print("before: " + str(arg2))
        print("before: " + str(arg3))

        if before_rotate == 0:
            try:
                rotate = int(arg1)
            except:
                pass
            try:
                rotate = int(arg2)
            except:
                pass
            try:
                rotate = int(arg3)
            except:
                pass

        print("rotate(with int args) " + str(rotate))

        try:

            #if type(arg1) is int:
            #   rotate = arg1
            if type(arg1) is str:
                if arg1 in users:
                    messages_from = arg1
                else:
                    title = arg1
            #if type(arg2) is int:
             #   rotate = arg2
            if type(arg2) is str:
                if arg2 in users:
                    messages_from = arg2
                else:
                    title = arg2
            #if type(arg3) is int:
             #   rotate = arg3
             if arg3 == None:


                 if arg3 != None:
                     if type(arg3) is str:
                         if arg3 in users:
                             messages_from = arg3
                         else:
                             title = arg3
        except Exception:
            pass

        #if messages_from != none:
            # needs to register if a username was provided, cycle through and only pick out those user messages

        if title == None:
            title = "messages"
        if rotate == 0:
             rotate = 1
        i = rotate

        print("argument 1: " + str(arg1))
        print("argument 2: " + str(arg2))
        print("argument 3: " + str(arg3))

        print("rotate: " + str(rotate))
        print("messages_from: " + str(messages_from))
        print("title: " + str(title))

        while i > 0:
            messages.rotate(rotate)
            usermessage = messages.pop()
            write_the_dang_thing()
            if i != 0:
                x = rotate - 1
                rotate = rotate * -1
                messages.rotate(rotate)
                rotate = x
                messages.rotate(rotate)
                i - 1
            elif i == 0:
                await bot.send_message(message.channel, "written to " + author + "'s scratchpad!")

    if message.content.startswith(prefix + "help"):
        await bot.send_message(message.channel, "What command would you like help with?")
        #if message.content.lower().find("grab") !=-1:
        print(helpmeh.with_grab())
        #await bot.send_message(message.channel, "test")

    '''
bot.run(token)

