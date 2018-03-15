import discord
import random
from discord.ext import commands
import json
import sys
import asyncio
import ioMod
import os
from collections import deque
from subprocess import check_output
import itertools

global msg_author
global msg_content
global msg_chan

b_details = {
        "description":"Scratchpad bot",
        "path":-1,
        "token":-1,
        "prefix":'@'
}

if os.getcwd().find("gector") != -1:
    with open("/home/gector/key.txt", 'r') as f:
        b_details['token'] = f.readline(100).strip() # TODO, fix readline
elif os.getcwd().find("thallia") != -1:
    with open("/home/thallia/key/scratchy-discord-token.txt", 'r') as f:
        b_details['token'] = f.readline(100).strip() # TODO, fix readline

# Functions {{{
def find_quote(msg_list, index = 0):
    for x in msg_list[index:]:
        print(x)
        if x.find('"') != -1:
            return msg_list.index(x)

def rm(entry_name, value):
    handler = ioMod.json_handler()
    return handler.remove_entry(msg_author, entry_name, value)

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

    return "Success! Try `{}show {}` to display your new scratchpad entry".format(b_details['prefix'], args[0])

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
                    fill_me += f'{element}: {value}\n' #element + ": " + value + "\n"
                elif type(value) == list:
                    indent = 6*' '
                    fill_me += f'{element}: \n {indent}'#element + ": " + "\n" + indent
                    for x in range(0, 9):
                        if x < len(value) and value[x] != None:
                            fill_me += f'({x}) "{value[x]}"\n {indent}'#"({}) ".format(x) + "\"" + value[x] + "\"\n" + indent
                    if len(value) > 10:
                        fill_me += f'... and {len(value) -9} more'
                        
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

def parse_args(args): # return argruments seperated into their different data types
    # TODO:
    # This eats numbers if you put a string in with numbers in it. 
    # Use a for loop to search for and grab entries between "" and count it as a string

    return_type = {
            "integers": [],
            "strings": []
    }

    for elem in args:
        try:
            x = int(elem)
            return_type['integers'].append(x)
        except:
            if elem.find(':') != -1 and elem.find("u:") == -1 and elem.find("t:") == -1: 
                s = elem.split(":")
                if len(s) == 2: # we have a correctly formatted range
                    try:
                        digit1 = int(s[0])
                        digit2 = int(s[1])
                        for n in range(digit1, digit2):
                            return_type['integers'].append(n)
                    except:
                        print("Parse args failed.")
                        pass;

            else:
                return_type['strings'].append(elem)

    return return_type;
# }}}

print("Bot token: " + b_details['token'])

bot = discord.Client()

global q

@bot.event  # must confirm the connection when it's done connecting
async def on_ready():
    print("\n" + (' '*20) + "Connected!")
    print((' '*20) + "Username: " + bot.user.name)
    print((' '*20) + "Prefix: " + b_details['prefix'])
    print('-'*50)
    while True:
        i = await q.get()
        if type(i) == str:
                await bot.send_message(bot.get_channel("289957526882222080"), i)
                #print(i)

@bot.event
async def on_message(message):
    global msg_author
    global msg_content
    global msg_chan

    if message.author.bot:
        return;

    data = 0;
    user = ioMod.json_handler()
    author = message.author.name.lower()
    messages = bot.messages
    title = ""

    msg_content = message.content
    msg_author = message.author.name.lower()
    msg_chan = message.channel

    if message.content.startswith(b_details['prefix'] + "show"):             # Show values or entries of a user's scratchpad
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

    if msg_content.startswith(b_details['prefix'] + "new"):                  # Add a new entry
        message_args = msg_content.split(" ")
        arg1 = None
        try:
            arg1 = str(message_args[1].strip())
        except Exception as e:
            await bot.send_message(msg_chan, "Err: Unable to parse args. Are you using `new <entry_name>`?") # Report error
            await bot.send_message(msg_chan, "{}".format(e))
            
        data = None
        handler = ioMod.json_handler()
        try:
            data = handler.read_user(msg_author)
            if data == None:
                # new_file(user, fp = None)
                handler.new_file(msg_author)
                data = handler.read_user(msg_author)
    
            # new(user, entry_name):
            handler.new(msg_author, arg1)
            await bot.send_message(msg_chan, "Success! Try `{}show {}` to display your new scratchpad entry".format(b_details['prefix'], arg1))
        except Exception as e:
            await bot.send_message(msg_chan, "{}".format(e))

    
        
    if msg_content.startswith(b_details['prefix'] + "set"):                  # Set a value in a user's scratchpad
        # set <entry> <field> <value>
        if(len(msg_content.split(' ')) <= 3):
            await bot.send_message(msg_chan, "Incorrect amount or setup of arguments. Try `@set <entry> <field> <value>`.") # not argruments lol
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

    if msg_content.startswith(b_details['prefix'] + "bytecode"):             # Show some of my bytecode
        me = check_output(["python3", "-m", "dis", os.getcwd() + "/" + __file__]).decode("utf-8")
        r1 = random.randint(0, len(me))
        r2 = random.randint(r1, len(me))
        me = me[r1:r2]
        await bot.send_message(message.channel, "```\n" + me + "```")

    if msg_content.startswith(b_details['prefix'] + "upload_scratch"):       # Upload scratchpad
        if os.path.isfile(msg_author + ".json"):
            await bot.send_message(msg_chan, "Uploading your scratchpad...")
            await bot.send_file(msg_chan, os.getcwd() + "/" + msg_author + ".json")
        else:
            await bot.send_message(msg_chan, "Err: Unable to upload file, check to make sure it exists.")
    
    if msg_content.startswith(b_details['prefix'] + "grab"):
        arguments = parse_args(msg_content.split(' ')[1:])
        index_title = -1
        index_usr = -1
        num = 1 #arguments['integers'][0]
        for elem in arguments['strings']:
            if elem.find('t:') != -1:
                index_title = arguments['strings'].index(elem)
            if elem.find('u:') != -1:
                index_usr = arguments['strings'].index(elem)
        if len(arguments['integers']) == 1:
            num = arguments['integers'][0]

        print("Index_title: " + str(index_title))
        print("Index_usr: " + str(index_usr))
        print("Num: " + str(num))
        print(arguments)
        
        g_usr = arguments['strings'][index_usr].split(':')[1]
        g_title = arguments['strings'][index_title].split(':')[1]
        
        counter = 0;
        msg_list = [];
        for n in range(len(bot.messages)-1, 0, -1):
            msg = bot.messages[n]
            if msg.author.name.lower() == g_usr.lower() and msg.content != msg_content:
                msg_list.append("{}: {}".format(msg.author.name, msg.content))
                counter += 1
            if counter >= num:
                break; 
        print(msg_list)
        if len(bot.messages) < num or len(msg_list) < num:
            await bot.send_message(msg_chan, "I don't have that many messages cached!")
            return;
        handler = ioMod.json_handler()
        data = handler.read_user(msg_author)
        print(data)
        if data == None:
            await bot.send_message(msg_chan, "Error reading file, does that entry exist?")
            return;
    
        if data[g_title]:
            print("Adding {} messages to {}".format(num, g_title))
            for msg in msg_list:
                if not msg in data[g_title]['values']:
                    data[g_title]['values'].append(msg)
            print(handler.write_user(data, msg_author))
        await bot.send_message(msg_chan, "Success!")

    if msg_content.startswith(b_details['prefix'] + "ping"):                 # For testing if I'm on.
        await bot.send_message(msg_chan, "Pong!")


def got_stdin_data(q): # Get input.
    asyncio.async(q.put(sys.stdin.readline()))
    if not q.empty():
        print(list(q.get_nowait()))

q = asyncio.Queue()
loop = asyncio.get_event_loop()
loop.add_reader(sys.stdin, got_stdin_data, q)
tasks = [
        asyncio.gather(bot.run(b_details['token']))
        ]
try:
    loop.run_until_complete(asyncio.wait(tasks))
except KeyboardInterrupt:
        pass;

loop.close()

bot.run(token)
