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
import itertools

global input_text
input_text = []
description = "scratchpad bot"
path = "/home/thallia/code/scratchy/"
file_token = "/home/thallia/key/scratchy-discord-token.txt"
if os.getcwd().find("gector") != -1:
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
def set_entry(args, data = None):
    # set <entry> <field> <value>
    
    value = args[2:]  

    index1 = find_quote(value)
    index2 = find_quote(value, index1+1)

    print(value[index1+1:])
    print("Index1: {}, index2: {}".format(index1, index2))
    print("Arg0: {}, Arg1: {}".format(args[0], args[1]))   
    text = None
    if index2 != None:
        text = ' '.join(value[index1:index2+1]).replace('"', "")
    else:
        text = ' '.join(value[index1:]).replace('"', "")

    print(text)
    
    # Make a temporary backup.
    handler = ioMod.json_handler()
    handler.make_backup()

    if args[1] != "values":
        try:
            data[args[0]][args[1]] = text
            # write_user(obj, user)
            handler.write_user(data, msg_author)
        except KeyError:
            return "Entry not in scratchpad!"
    elif args[1] == "values":
        try:
            data[args[0]][args[1]].insert(0, text)
            handler.write_user(data, msg_author)
        except KeyError:
            return "If you see this, check set function for idiot's coding error."

    return "Success! Try `{}show {}` to display your new scratchpad entry".format(prefix, args[0])

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
        if type(field) == dict and show_all:
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
        elif type(field) == list:
            fill_me += "```\n"
            indent = 4*' '
            fill_me += list(data.keys())[list(data.values()).index(field)]+ "\n"
            for x in range(0, 9):
                if x < len(field) and field[x] != None:
                    fill_me += "({}) ".format(x) + "\"" + field[x] + "\"\n" + indent

        elif show_all == False:
            fill_me = "```\n"
            for f in data.values():
                if type(f) == dict:
                    print(f['title'])
                    fill_me += f['title'] + "\n"
                if type(f) == list:
                    fill_me += list(data.keys())[list(data.values()).index(f)]+ "\n"

            fill_me += "```"
            return fill_me

        fill_me += "```"

    return (fill_me)



with open(file_token, 'r') as file:      # *takes all of gector's code*
    token = file.readline(100).strip()
print("Bot token: " + token)

bot = discord.Client()

global q

@bot.event  # must confirm the connection when it's done connecting
async def on_ready():
    print("Connected!")
    print("Username: " + bot.user.name)
    print("-----------------")
    #await bot.send_message(bot.get_channel("289957526882222080"), "ready")#test)
    while True:
        i = await q.get()
        if type(i) == str:
                await bot.send_message(bot.get_channel("289957526882222080"), i)
                #print(i)

@bot.event
async def on_message(message):
    data = 0;
    user = ioMod.json_handler()
    prefix = "@"
    author = message.author.name.lower()
    messages = bot.messages
    helpmeh = help_meh()
    title = ""

    msg_content = message.content
    msg_author = message.author.name.lower()
    msg_chan = message.channel


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
            return


    if msg_content.startswith(prefix + "set"):
        # set <entry> <field> <value>
        if(len(msg_content.split(' ')) <= 3):
            await bot.send_message(msg_chan, "Incorrect amount or setup of argruments. Try `@set <entry> <field> <value>`.")
            return;

        args = parse_args(msg_content.split(" ")[1:])

        handler = ioMod.json_handler()
        data = handler.read_user(msg_author)
        if type(data) == str:   # Error message was returned
            await bot.send_message(msg_chan, data)
            return # Stop the code.

        if len(args['strings']) >= 3: # We have a correct setup.
            await bot.send_message(msg_chan, set_entry(args['strings'], data=data))
        else:
            await bot.send_message(msg_chan, "Incorrect amount or setup of argruments. Try `@set <entry> <field> <value>`.")

    if msg_content.startswith(prefix + "upload_scratch"):
        if os.path.isfile(msg_author + ".json"):
            await bot.send_message(msg_chan, "Uploading your scratchpad...")
            await bot.send_file(msg_chan, os.getcwd() + "/" + msg_author + ".json")
        else:
            await bot.send_message(msg_chan, "Err: Unable to upload file, check to make sure it exists.")

    if msg_content.startswith(prefix + "ping"): # For testing if I'm on.
        await bot.send_message(msg_chan, "Pong!")

    if message.content.startswith(prefix + "grab"): # checks for the trigger command
        user = ioMod.json_handler()         #user = ioMod.json_handler
        data = user.read_user(msg_author)   #data = user.read_user(0, author)
        usr, title, num, result, result_from = [0, 0, 0, 0, 0]
        usr_pre = 'usr'
        title_pre = 'ti'
        num_pre = 'num'
        msg_args = msg_content.split(" ")
        print("arguments: " + str(msg_args))

        for elem in msg_args:
            if elem.find(":") != -1:
                msg_args[msg_args.index(elem)] = elem.split(":")
                #msgs = [msg_args[0] for elem in msg_args]

        print("arguments: " + str(msg_args))

        def write_the_dang_thing():
            result = result_from
            if num > 0:
                i = num
                while i > 0:
                    if title in data:
                        data[title].insert(0, msg_content) # inserts the message into the file
                        user.write_user(data, msg_author) # writes the file
                        i -= 1

        # smaller deque to shuffle through
        msg_deq = itertools.islice(messages, 0, 200) # makes deque 200 messages

        channel = msg_chan # grabs channel to sort from (chan you sent trigger from)

        def chan_cheq(input_arg): # sorts through messages from specific channels
            if input_arg.channel == channel:  #if the input message is the same as the channel you sent the trigger from, return only those messages
                return input_arg

        def usr_cheq(input_arg): # sorts through specific users
            for usr in input_arg.author: # for the user inputted to copy from in the argument passed, return the message to copy
                return input_arg

        chan_deq = filter(chan_cheq, msg_deq) # filters out specific channel to grab from in the deq

        if title_pre in msg_args:  # title prefix is "ti"
            # not comparing the strings correctly with the if statement, need to fix this. all commented out stuff needs to be adjusted with solution.
            title_place = msg_args.index("ti")
            title_name = title_place + 1
            title = msg_args[title_name].strip()
            print(title)

            if title == 0:
                title = "messages"
                print(title)


        #if usr_pre in msg_args:
        #    usr_place = msg_args.index("usr") # returns where usr is
        #    usr_name = usr_place + 1  # gets position of username
        #    usr = msg_args[usr_name].strip() # gets user to copy from
        #    print(usr)
        #    usr_deq = filter(usr_cheq, chan_deq) # filters deq with username to copy from
         #   result_from = usr_deq

            #if num_pre in msg_args:
            #    num_place = msg_args.index("num") # finds number arg position
            #    num_pos = num_place + 1 # gets actual number
            #    num = msg_args[num_pos].strip()
            #    print(int(num))
            else:
                num = 1
                print(num)
                write_the_dang_thing()
                await bot.send_message(msg_chan, "Saved to " + author + "'s scratchpad!")
                return

        #elif num_pre in msg_args: # copied bc if no user, can't pull from usr_deq
        #    num_place = msg_args.index("num") # finds number arg position
        #    num_pos = num_place + 1 # gets actual number
        #    num = msg_args[num_pos].strip()
        #    print(int(num))
        #    result_from = chan_deq
        else:
            num = 1
            print(num)
            result_from = chan_deq
        write_the_dang_thing()
        await bot.send_message(msg_chan, "Saved to " + author + "'s scratchpad!")

    if message.content.startswith(prefix + "help"):
        await bot.send_message(message.channel, "What command would you like help with?")
        #if message.content.lower().find("grab") !=-1:
        print(helpmeh.with_grab())
        #await bot.send_message(message.channel, "test")

def got_stdin_data(q): # Get input.
    asyncio.async(q.put(sys.stdin.readline()))
    if not q.empty():
        print(list(q.get_nowait()))

q = asyncio.Queue()
loop = asyncio.get_event_loop()
loop.add_reader(sys.stdin, got_stdin_data, q)
tasks = [
        asyncio.gather(bot.run(token))
        ]
try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
        pass;

loop.close()

#bot.run(token)

bot.run(token)
