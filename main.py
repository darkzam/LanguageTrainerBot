
import discord
from discord.ext import commands
from clsText import Text
from apiRequests import TextService
import random

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

##maybe add a cooldown to this command later
##maybe create a task to check for muted users and move them on sight
@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def mute(ctx, member: discord.Member = None):
	
	if member is None:

		server = ctx.message.server
		author = ctx.message.author
		await client.say("Welcome to the: " + server.name)

		generalChannel = discord.utils.get(server.channels, name='General')
		testChannel = discord.utils.get(server.channels, name= 'Test')

		mutedRole = discord.utils.get(server.roles, name='muted')

		membersLocal = []

		if generalChannel is not None and testChannel is not None:
			members = generalChannel.voice_members
			
			if len(members) > 0:
				for member in members:
					if member is not author:
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

partyMembers = [] ## keeps track of all the members of the on running party round
tempTurns = []
roundCounter = 1
memberTurn = None

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def create(ctx):
	global partyMembers
	
	server = ctx.message.server
	voiceChannel = discord.utils.get(server.channels, name='General')

	if voiceChannel:

		members = voiceChannel.voice_members

		if members is not None and len(members) > 0:
			
			for member in members:
				partyMembers.append(member) ##appends at the last element in the list
				tempTurns.append(member)
			
			await client.say('Round ' + str(roundCounter) + ' starting ')

			#to-do maybe apply role to author of message
			#run background task to keep watch over members that join, and add them to the party
			# or leave, for now if they leave keep them on the list
		else:
			await client.say('There are not users in the voice channel.')

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def turn(ctx):
	global tempTurns, memberTurn, roundCounter

	if len(partyMembers) > 0:
		if len(tempTurns) > 0:
			
			if len(tempTurns) == len(partyMembers):
				await client.say( 'Round ' + str(roundCounter) + ' starting!')
			
			memberTurn = tempTurns.pop(0)
			
			if len(tempTurns) == 0:
				await client.say('Last turn of Round ' + str(roundCounter) )
			await client.say( memberTurn.name + " It's your turn.")
		else:
			await client.say('Round ' + str(roundCounter) + ' has finished!' )
			roundCounter += 1
			for member in partyMembers:
				tempTurns.append(member)
	else:
		await client.say("Party has not started.")

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def nickname(ctx):

	mary = ['Angelito de Fresa', 'Strawberry Angel', 'Love Nugget', 'Platinum Nugget','Mary Bear', 'Brujita', 'Amorcito', 'Ariel','Bella','Mury','Pastelito','Caramelito','Bombon','Sweetheart','Honey','Mini Mary', 'Shorty','Maryrose','Boom boom', 'Zammy', 'Zamuel','Honey','Princess', 'Zamircito','Angelpac', 'amorcito', 'cielito']

	number = random.randint(0,len(mary)-1)
	
	await client.say('Nickname of the day: ' + mary[number])

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def cute(ctx):
	
	cute = ['Zamirnarvaezpham@gmail.com','Ihavethebestgirlfriendever@yesthatsme.Mury',' Your mommy is the best cook ever. She made the yummiest love nugget','1. Be the cutest thing ever 2. Have the sweetest attitude 3. Spoil your girl with love 4. Stay handsome as hell 5. Name yourself Zamir Narváez',"I'll be the first and last one to love you.", 'Te amo mucho, my one and only','I love you to the moon and back', 'Te amo tanto.']
	
	number = random.randint(0,len(cute)-1)
	
	await client.say('Cute thing of the day: ' + cute[number])

client.run(Token)

