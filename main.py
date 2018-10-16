
import discord
from discord.ext import commands

Token = 'NDc5NzE1NTQxMzg1MzQ3MTAy.Dlyb2A.ALzfw-NYt-nx5rQT3EcwZhZ66Wc' 

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	print("bot is ready")

@client.command()
async def ping():
	await client.say('epa la arepa')

@client.command()
async def echo(*args):
	output = ''
	for word in args:
		output = output + word + ' '
	await client.say(output)

client.run(Token)	

