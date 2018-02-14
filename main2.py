import discord
from discord.ext import commands
import json
import sys
import asyncio
import ioMod

description = "scratchpad bot"
path = "/home/thallia/code/scratchy/"
file_token = "/home/thallia/key/scratchy-discord-token.txt"
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
    prefix = "@scratchy"
    author = message.author.name.lower()

    if message.author.name.lower() == "scratchy":   # prevents triggering of self
        return

    #if message.content.startswith(prefix + " test") !=-1:
        #await bot.send_message(message.channel, "derp")

    print("adding: " + message.content)
    users[message.author.name.lower()].insert(0, message.content)

    if message.content.startswith(prefix + " lastmessage") != -1: # checks for the trigger command
        user = ioMod.json_handler
        data = user.read_user(0, author)
        #users[message.author.name.lower()].insert(0, message.content)
        for msg in users[message.author.name.lower()]:      # for the object in that user's file....
            data["messages"].insert(0, msg)                 # inserts the message into the file
            user.write(0, data, author + ".json") # writes the file
            await bot.send_message(message.channel, "written to " + author + "'s scratchpad!")
        print("success")

bot.run(token)
