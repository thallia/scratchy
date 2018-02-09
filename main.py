import discord
from discord.ext import commands
import json
import sys
import asyncio

description = "scratchpad bot"
path = "/home/thallia/code/scratchy/"
file_token = "/home/thallia/key/scratchy-discord-token.txt"
token = ""

commands = [      # created just so I know what commands we have so far/commands we want to integrate
    "!lastmessage"
    "!set"
    "!add"
    "!test"
]

with open(file_token, 'r') as file:      # *takes all of gector's code*
    token = file.readline(100).strip()
print("Bot token: " + token)

bot = discord.Client()

@bot.event  # ?
async def on_ready():
    print("Connected!")
    print("Username: " + bot.user.name)
    print("-----------------")


@bot.event
async def on_message(message):
    data = 0;
    user = "test"
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
   # await bot.send_message(message.channel, user)
    with open(path + message.author.name.lower() + ".txt", 'w') as file:
        file.write(user) ## this does not work when the await bot.send command is up
    await bot.send_message(message.channel, "Saved to your scratchpad!")

bot.run(token)
