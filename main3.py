import discord
from discord.ext import commands
import json
import sys
import asyncio
import ioMod
import os
from collections import deque

description = "scratchpad bot"
path = "/home/thallia/code/scratchy/"
file_token = "/home/thallia/key/scratchy-discord-token.txt"
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

def show(data=None, subject = None):
    fill_me = ""
    if subject != None:
        if subject in data:
            data = {key:data[key] for key in [subject]}
        else:
            return "Invalid request, subject not in file"

    for field in data.values():
        #await bot.send_message(message.channel, field)
        if type(field) == list or type(field) == dict:
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
                        try:
                            fill_me += "({}) ".format(x) + "\"" + value[x] + "\"\n" + indent
                        except Exception as e:
                            print("")
        fill_me += "```"

    return (fill_me)
    
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
    prefix = "@"
    author = message.author.name.lower()
    messages = bot.messages

    if message.author.name.lower() == "scratchy":   # prevents triggering of self
        return

    #if message.content.startswith(prefix + " test") !=-1:
    #await bot.send_message(message.channel, "derp")

    print("adding: " + message.content)

    #users["document"].insert(0, message.content)
    if message.content.startswith(prefix + "show"):
        message_args = message.content.split(" ")
        arg1 = None
        try:
            arg1 = message_args[1].strip()
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
                    
    if message.content.startswith(prefix + "grab"): # checks for the trigger command
        user = ioMod.json_handler
        data = user.read_user(0, author)
        #messages.reverse()
        messages.rotate(1)
        usermessage = messages.pop()
        if users[message.author.name.lower()] !=-1: # for the object in that user's file....
            data["messages"].insert(0, usermessage.content) # inserts the message into the file
            user.write(0, data, author + ".json") # writes the file
        await bot.send_message(message.channel, "written to " + author + "'s scratchpad!")

    #messages = bot.messages
    #test = messages.pop()
    #print(test.content)

bot.run(token)
