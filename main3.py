
import discord
from discord.ext import commands

Token = 'NDc5NzE1NTQxMzg1MzQ3MTAy.Dlyb2A.ALzfw-NYt-nx5rQT3EcwZhZ66Wc' 

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	print("bot is ready")

@client.command(pass_context=True)
async def clear(ctx, amount=100):
	channel = ctx.message.channel
	messages = []
	async for msg in client.logs_from(channel, limit=int(amount)):
		messages.append(msg)

	await client.delete_messages(messages)
	await client.say('messages deleted')

client.run(Token)	
