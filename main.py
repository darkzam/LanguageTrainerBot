
import discord
from discord.ext import commands
from clsText import Text
from apiRequests import TextService

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

obTextService = None

@client.command(pass_context=True)
async def paragraph(ctx, language, keyword=''):
	global obTextService
	channel = ctx.message.channel

	obTextService = TextService(language)
	if keyword == '':
		keyword = 'a'
	await obTextService.getJsonByKeyword(keyword)
	
	url = obTextService.getUrlNext()
	obText = Text(url)

	await obText.loadArticle()
	txt = obText.getParagraph(300)

	if txt == '':
		await client.say('Paragraph could not be found.')
	else:
		await client.say(txt)
	

@client.command(pass_context=True)
async def next(ctx):
	global obTextService
	
	if obTextService:
		url = obTextService.getUrlNext()
		obText = Text(url)

		await obText.loadArticle()
		txt = obText.getParagraph(300)
	
		if txt == '':
			await client.say('Paragraph could not be found.')
		else:
			await client.say(txt)

	else:
		await client.say('Text not loaded.')

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def mute(ctx, member: discord.Member = None):
	
	if member is None:

	server = ctx.message.server
	await client.say("Welcome to the: " + server.name)

	generalChannel = discord.utils.get(server.channels, name='General')
	testChannel = discord.utils.get(server.channels, name= 'Test')

	mutedRole = discord.utils.get(server.roles, name='muted')

	membersLocal = []

	if generalChannel is not None and testChannel is not None:
		members = generalChannel.voice_members
		
		if len(members) > 0:
			for member in members:
				membersLocal.append(member)
			
			for member in membersLocal:

				for role in member.roles:
					if role is mutedRole:
						break
					else:
						await client.add_roles(member, mutedRole)

				await client.move_member(member, testChannel)
				await client.move_member(member, generalChannel)			
	else:
		await client.say(member.name)			

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def mary(ctx):
	mary = ['Angelito de Fresa', 'Strawberry Angel', 
				'Love Nugget', 'Platinum Nugget',
				 'Mary Bear', 'Brujita', 'Amorcito', 'Ariel',
				 'Bella']
				 
	for names in mary:
		await client.say("Welcome to the: " + server.name)

client.run(Token)

