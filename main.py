
import discord
from discord.ext import commands

Token = 'NDc5NzE1NTQxMzg1MzQ3MTAy.Dlyb2A.ALzfw-NYt-nx5rQT3EcwZhZ66Wc' 

client = commands.Bot(command_prefix = 'epa')

@client.event
async def on_ready():
	print("bot is ready")

@client.event
async def on_message(message):
	author = message.author
	content = message.content
	print('{}:{}'.format(author, content))

@client.event
async def on_message_delete(message):
	author = message.author
	content = message.content
	channel = message.channel
	await client.send_message(channel, '{}:{}'.format(author, content))




client.run(Token)	

