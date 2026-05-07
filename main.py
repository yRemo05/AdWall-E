from discord.ext import commands,tasks
import json,os,asyncio,discord
from Cogs.Ext.General_Functions import whatis
from discord import ActivityType,Activity,Game
from time import sleep
import discord

# Get configuration.json
with open("Data\\configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]

# Intents
intents = discord.Intents.all()
# The bot
bot = commands.Bot(command_prefix = prefix, intents = intents, case_insensitive = True)

# add the general checks
#bot.add_check(have_any_mod_roles)
#bot.add_check(have_settings_perms)
#bot.add_check(have_giveaway_perms)
#bot.add_check(have_ticket_perms)

# Load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs."+filename[:-3])
	'''for filename in os.listdir("Backend"):
		if filename.endswith(".py"):
			bot.load_extension(f"Backend."+filename[:-3])'''


@tasks.loop(seconds=15)
async def status_loop():
	statuses = whatis("statuses",5)
	plays = statuses["playing"]
	watches = statuses["watching"]
	listens = statuses["listening"]

	for play in plays:
		print(play)
		await bot.change_presence(activity=Game(play))
		await asyncio.sleep(whatis("loop_delay",5))

	for watch in watches:
		print(watch)
		await bot.change_presence(activity=Activity(type=ActivityType.watching, name =watch))    
		await asyncio.sleep(whatis("loop_delay",5))

	for listen in listens:
		print(listen)
		await bot.change_presence(activity=Activity(type=ActivityType.listening, name =listen))   
		await asyncio.sleep(whatis("loop_delay",5))


os.system("cls")
bot.run(token)
