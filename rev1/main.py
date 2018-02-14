import discord
from discord.ext import commands
import json
import sys
import asyncio

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
    user = ""
    counter = 1
    if message.content.lower().find("!test") !=-1:
        name = str(message.author)
        await bot.send_message(message.channel, "Hi, " + name)

    #if message.content.lower().find("!lastmessage"): # !lastmessage <user> <number-of-messages-to-save>
    if message.content.startswith('!lastmessage'):
        if message.content.lower().find("fouric") !=-1:
            user = "fouric"
        elif message.content.lower().find("gector") !=-1:
            user = "gector"
        elif message.content.lower().find("Jay") !=-1:
            user = "Jay"
        elif message.content.lower().find("thallia") !=-1:
            user = "thallia"
        elif message.content.lower().find("uelen") !=-1:
            user = "uelen"
        elif message.content.lower().find("galois") !=-1:
            user = "galois"
        await bot.send_message(message.channel, "How many messages do you want to copy from " + user + "?") # asks how many messages you want to copy from the user you specified
        #if await bot.wait_for_message(author=message.author, content="1") !=-1:
          #  msgs = 1

        with open(path + message.author.name.lower() + ".txt", 'a') as file: # opens user scratchpad
            file.write(user)


        ### need to get the file.write to write the number of messages you want to copy and put in the scratchpad. ###
        ### 1) read in last 50 messages
        ### 2) identify how many messages it should copy
        ### 3) copy the messages with file.write into scratchpad
            if message.author.name != bot.user.name: # makes sure scratchy doesn't trigger himself
                await bot.send_message(message.channel, "Saved to your scratchpad!") # confirms it worked


                #############################################^thallia's portion^###################################################################

    

bot.run(token)
