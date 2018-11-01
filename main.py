
import discord
from discord.ext import commands
from clsText import Text
from apiRequests import TextService
from clsSesionLectura import SesionLectura
import random
import json

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
sesion = None

@client.command(pass_context=True)
async def paragraph(ctx, language, keyword=''):
	global obTextService

	if sesion is None:
		await client.say("There's not an ongoing Sesion de Lectura.")

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
		sesion.addParagraph
	

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

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def create(ctx):
	global sesion

	server = ctx.message.server
	voiceChannel = discord.utils.get(server.channels, name='General')

	if voiceChannel:

		members = voiceChannel.voice_members

		if members is not None and len(members) > 0:
			
			sesion = SesionLectura(members)
			
			message = sesion.start()

			await client.say(message)

			#to-do maybe apply role to author of message
			#run background task to keep watch over members that join, and add them to the party
			# or leave, for now if they leave keep them on the list
		else:
			await client.say('There are not users in the voice channel.')

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def turn(ctx):
	global sesion

	if sesion is None:
		await client.say("There's not an ongoing Sesion de Lectura.")
		return

	message = sesion.nextTurn()

	##print(sesion.tempTurns)

	if message != "":
		await client.say( message)
	
	 ##it must return the member whose turn currently is active

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def end(ctx):
	global sesion

	await client.say('Good job everyone!\nParty Stats\nTotal Rounds: ' + str(sesion.roundCounter) + ' Total Turns: ' + str(sesion.turnCounter))

	### MVP of the Sesion, ranking etc, leveling system

	sesion = None

@client.command(pass_context=True)
@commands.has_any_role('Party Master')
async def mistakes(ctx, *args):
	global sesion
	##two options
	##1.Get arguments in a single string and then handle it
	##2.Get arguments already separated in the *args list

	if sesion is None:
		await client.say("There's not an ongoing Sesion de Lectura.")
		return


	print(sesion.getJson())

	json_data = json.dumps(sesion.getJson())

	print(json_data)

	##get current turn member
	
	message = ctx.message

	##get arguments from the message
	## create object that links this sesion member, article and mistakes
	## sesion class generate json object with all the information.
	## generate final json object


"""
{['sesion': ]
 []}

"""

@client.command(pass_context=True)
async def nickname(ctx):

	mary = ['Angelito de Fresa', 'Strawberry Angel', 'Love Nugget', 'Platinum Nugget','Mary Bear', 'Brujita', 'Amorcito', 'Ariel','Bella','Mury','Pastelito','Caramelito','Bombon','Sweetheart','Honey','Mini Mary', 'Shorty','Maryrose','Boom boom', 'Zammy', 'Zamuel','Honey','Princess', 'Zamircito','Angelpac', 'amorcito', 'cielito']

	number = random.randint(0,len(mary)-1)
	
	await client.say('Nickname of the day: ' + mary[number])

@client.command(pass_context=True)
async def cute(ctx):
	
	cute = ["I'll be the first and the last one to love you",'Zamirnarvaezpham@gmail.com','Ihavethebestgirlfriendever@yesthatsme.Mury',' Your mommy is the best cook ever. She made the yummiest love nugget','1. Be the cutest thing ever 2. Have the sweetest attitude 3. Spoil your girl with love 4. Stay handsome as hell 5. Name yourself Zamir Narváez',"I'll be the first and last one to love you.", 'Te amo mucho, my one and only','I love you to the moon and back', 'Te amo tanto.','A lot of the stuff you want, I want it too' ]
	
	number = random.randint(0,len(cute)-1)
	
	await client.say('Cute thing of the day: ' + cute[number])

client.run(Token)

