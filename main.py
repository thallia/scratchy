import discord
from discord.ext import commands
import json
import ioMod
import sys
import asyncio

description = "scratchpad bot"
path = "~/projects/scratchy/"
file_token = "/home/gector/key.txt"
prefix="@"
token = ""

commands = [	  # created just so I know what commands we have so far/commands we want to integrate
	"lastmessage"
	"set"
	"add"
	"test"
]

users = {
	"gector": [],
	"thallia": [],
	"fouric": []
}

with open(file_token, 'r') as file:	  # *takes all of gector's code*
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
	user = 0;
	counter = 1
	
	if message.author.name.lower() == "scratchy":
		return

	if message.content.lower().find(prefix + "test") !=-1:
		name = str(message.author)
		await bot.send_message(message.channel, "Hi, " + name)
	
	print("Adding: " + message.content)
	users[message.author.name.lower()].insert(0, message.content)

	#if message.content.lower().find("!lastmessage"): # !lastmessage <user> <number-of-messages-to-save>
	if message.content.startswith(prefix + 'lastmessage'):
		if message.content.lower().find("fouric") !=-1:
			user = ioMod.json_handler()
		elif message.content.lower().find("gector") !=-1:
			user = ioMod.json_handler()
		elif message.content.lower().find("Jay") !=-1:
			user = ioMod.json_handler()
		elif message.content.lower().find("thallia") !=-1:
			user = ioMod.json_handler()
		elif message.content.lower().find("uelen") !=-1:
			user = ioMod.json_handler()
		elif message.content.lower().find("galois") !=-1:
			user = ioMod.json_handler()
	
		if user != 0:
			last_messages = user.read_user("gector")["messages"]
			for msg in last_messages:
	 			await bot.send_message(message.channel, msg)

	if message.content.startswith(prefix + "add"):
		user = ioMod.json_handler()
		data = user.read_user("gector")
		for msg in users[message.author.name.lower()]:
			data["messages"].insert(0, msg)
		user.write(data, "gector.json")


	'''
		with open(path + message.author.name.lower() + ".txt", 'w') as file: # opens user scratchpad
			file.write(user)
	'''
	### need to get the file.write to write the number of messages you want to copy and put in the scratchpad. ###
	### 1) read in last 50 messages
	### 2) identify how many messages it should copy
	### 3) copy the messages with file.write into scratchpad
	'''
		if message.author.name != bot.user.name: # makes sure scratchy doesn't trigger himself
		await bot.send_message(message.channel, "Saved to your scratchpad!") # confirms it worked
	'''
	### 4) don't save to scratchpad every time someone inputs -- done ###
	### 5) don't reset the scratchpad, indent and add onto

bot.run(token)
