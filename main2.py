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


    if message.content.startswith(prefix + "grab"): # checks for the trigger command
        user = ioMod.json_handler
        data = user.read_user(0, author)
        usr, title, num = [0, 0, 0]
        usr_pre = "usr"
        title_pre = "t"
        num_pre = "num"
        messageargs = msg_content.split(" ").split(";")

        def write_the_dang_thing(result):
            result = result_from
            if num != 0:
                i = num
                while i > 0:
                    if users[message.author.name.lower()] !=-1: 
                        data[title].insert(0, result.content) # inserts the message into the file
                        user.write(0, data, author + ".json") # writes the file
                        i = i - 1

        # smaller deque to shuffle through
        msg_deq = messages[:200] # makes deque 200 messages
        channel = msg_chan # grabs channel to sort from (chan you sent trigger from)

        def chan_cheq(input_arg): # sorts through messages from specific channels
            if input_arg.channel == channel:
                return input_arg

        def usr_cheq(input_arg): # sorts through specific users
            if usr == users:
                return input_arg

        #def grab_num():

        chan_deq = filter(chan_cheq, msg_deq) # filters out specific channel to grab from in the deq

        if title_pre in messageargs:
            title_place = messageargs.index("t")
            title_name = title_place + 1
            title = messageargs[title_name].strip()
            print(title)
        else:
            title = "messages"
            print(title)


        if usr_pre in messageargs:
            usr_place = messageargs.index("usr") # returns where usr is
            usr_name = usr_place + 1  # gets position of username
            usr = messageargs[usr_name].strip() # gets user to copy from
            print(usr)
            usr_deq = filter(usr_cheq, chan_deq) # filters deq with username to copy from
            result_from = usr_deq

            if num_pre in messageargs:
                num_place = messageargs.index("num") # finds number arg position
                num_pos = num_place + 1 # gets actual number
                num = messageargs[num_pos].strip()
                print(int(num))
            else:
                num = 1
                print(num)
                write_the_dang_thing()
                await bot.send_message(msg_chan, "Saved to " + author + "'s scratchpad!")
                return

        elif num_pre in messageargs: # copied bc if no user, can't pull from usr_deq
            num_place = messageargs.index("num") # finds number arg position
            num_pos = num_place + 1 # gets actual number
            num = messageargs[num_pos].strip()
            print(int(num))
            result_from = chan_deq
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
