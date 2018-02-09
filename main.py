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
    if message.content.lower().find("!lastmessage"): # !lastmessage <user> <number-of-messages-to-save>
        if message.content.lower().find("fouric"):
            user = "fouric"
        if message.content.lower().find("gector"):
            user = "gector"
        if message.content.lower().find("Jay"):
            user = "Jay"
        if message.content.lower().find("thallia"):
            user = "thallia"
        if message.content.lower().find("uelen"):
            user = "uelen"
        if message.content.lower().find("galois"):
            user = "galois"
    with open(path + user + ".txt")


