import discord
from discord.ext import commands
from random import randint
from Cogs.Ext.Checks import have_settings_perms, is_dev
from Cogs.Ext.Embed_Loader import embeded
from Cogs.Ext.General_Functions import whatis

class HelpCog(commands.Cog, name=":regional_indicator_h:Help"):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
  

	@commands.command(name = 'help',
					usage="help",
					description = "Display the help message.",
					aliases = ['h', '?'])
	async def help (self, ctx):
		embed = embeded()
		prefix = whatis("prefix")
		for cog in self.bot.cogs:
			if cog=="Events" or cog=="Errors":
				continue
			cog_name = cog.split(":")[2]
			embed.add_field(name=cog,value=f"``{prefix}{cog_name}``",inline=True)
		await ctx.send(embed=embed)
	
	

	@commands.command(
		name="config",
		usage="config",
		description="Shows all configuration commands.",
		aliases=["configuration","settings"])
	async def config(self,ctx):
		embed = embeded()
		p = self.bot.command_prefix
		embed.description = f"Setting commands for {self.bot.user.name}. These commands are useful for customization."
		embed.add_field(name=f"{p}prefix <prefix>",value="Sets a new prefix for command execution.",inline=False)
		embed.add_field(name=f"{p}ddroles",value="Shows all drop down role menu commands.",inline=False)
		embed.add_field(name=f"{p}permissions",value="Shows all grantable permissions.",inline=False)
		embed.add_field(name=f"{p}stats",value="Shows all server stats manager settings.",inline=False)
		embed.add_field(name=f"{p}statuses",value="Shows all custom status settings.",inline=False)
		embed.add_field(name=f"{p}tickets",value="Shows all ticket settings.",inline=False)
		embed.add_field(name=f"{p}gating",value="Shows all gating commands.",inline=False)
		embed.add_field(name=f"{p}design",value="Shows all design settings.",inline=False)
		await ctx.send(embed=embed)



	@commands.command()
	async def ddroles(self,ctx):
		embed = embeded()
		p = self.bot.command_prefix
		embed.description = f"Drop down role menu configuration commands. These commands helps building drop down menus for role assignment."
		embed.add_field(name=f"{p}createddm [channel]",value="Sets up a reaction role menu for the mentioned channel.",inline=False)
		embed.add_field(name=f"{p}deleteddm <message id>",value="Deletes the dropdown menu from the database.",inline=False)
		embed.set_footer(text="⚠️ You should use deleting command instead of deleting the message manually. This may cause unexpected errors.")
		await ctx.send(embed=embed)


	@commands.command()
	async def gating(self,ctx):
		embed = embeded()
		p = self.bot.command_prefix
		embed.description = f"Gate configuration commands. These commands will help managing the joining and leaving member events."
		embed.add_field(name=f"{p}welchannel [channel]",value="Sets a channel to log the new members.",inline=False)
		embed.add_field(name=f"{p}byechannel [channel]",value="Sets a channel to log the leaving members.",inline=False)
		embed.add_field(name=f"{p}autorole <role>",value="Sets a role to give to new members.",inline=False)
		embed.add_field(name=f"{p}setwelcomemsg",value="Sets a welcome message to be sent to the log channel when a member is joined.",inline=False)
		embed.add_field(name=f"{p}setbyemsg",value="Sets a goodbye message to be sent to the log channel when a member is left.",inline=False)
		await ctx.send(embed=embed)

	@commands.command()
	async def tickets(self,ctx):
		p = self.bot.command_prefix
		embed = embeded()
		embed.description = "Ticket configuration commands. These commands will help you set up the entire ticket system."
		embed.add_field(name=f"{p}ticketsetup [channel]",value="Sets up a ticket with an easier ui to use for members.",inline=False)
		embed.add_field(name=f"{p}setticketwelcoming",value="Sets a message which will be sent to the ticket after creation.",inline=False)
		embed.add_field(name=f"{p}setticketpanel <category id/off>",value="Sets a category as a panel where tickets are created in.",inline=False)
		embed.add_field(name=f"{p}setticketlog [channel]",value="Sets a logging channel for ticket information.",inline=False)
		await ctx.send(embed=embed)
	
	
	@commands.command()
	async def permissions(self,ctx):
		p = self.bot.command_prefix
		embed=embeded()
		embed.description = "Permission granting commands.\n:warning:**WARNING** : Please be aware that these commands can grant access to risky commands."
		embed.add_field(name=f"{p}modperms <add/rem> <role>",value="Gives access to the moderation permissions to a role.",inline=False)
		embed.add_field(name=f"{p}ticketperms <add/rem> <role>",value="Gives access to the ticket permissions to a role.",inline=False)
		embed.add_field(name=f"{p}settingsperms <add/rem> <role>",value="Gives access to the settings permissions to a role.",inline=False)
		embed.add_field(name=f"{p}giveawayperms <add/rem> <role>",value="Gives access to the giveaway permissions to a role.",inline=False)
		await ctx.send(embed=embed)

	@commands.command()
	async def stats(self,ctx):
		p = self.bot.command_prefix
		embed = embeded()
		embed.add_field(name=f"{p}channelcounter <on/off>",value="Toogles channel count overseer.",inline=False)
		embed.add_field(name=f"{p}rolecounter <on/off>",value="Toogles role count overseer.",inline=False)
		embed.add_field(name=f"{p}membercounter <on/off>",value="Toogles member count overseer.",inline=False)
		embed.add_field(name=f"{p}shutdownstats",value="Clears the stats cache.",inline=False)
		embed.set_footer(text="Do not delete a created category or the channels manually since it may cause unexpected errors. Using the off mode with commands is highly recommended!!!")
		await ctx.send(embed=embed)

	@commands.command()
	async def design(self,ctx):
		p = self.bot.command_prefix
		embed = embeded()
		embed.description = "Embed design commands, note that if the arguments are left unfilled, they will be removed."
		embed.add_field(name=f"{p}embed_title [title]",value="Set the embed title.",inline=False)
		embed.add_field(name=f"{p}embed_image [url]",value="Set the embed image.",inline=False)
		embed.add_field(name=f"{p}embed_thumbnail [url]",value="Set the embed thumbnail.",inline=False)
		embed.add_field(name=f"{p}embed_color [hex code]",value="Set the embed color.",inline=False)
		embed.add_field(name=f"{p}embed_footer [url] [text]",value="Set the embed footer.",inline=False)
		await ctx.send(embed=embed)
	
	@commands.command()
	async def statuses(self,ctx):
		p = self.bot.command_prefix
		embed = embeded()
		embed.description = "Custom status commands. These commands will help editting custom status list."
		embed.add_field(name=f"{p}statuslist",value="Shows the current list of statuses.",inline=False)
		embed.add_field(name=f"{p}addplaying <status>",value=f"Add a `playing` status to statuses list.",inline=False)
		embed.add_field(name=f"{p}addwatching <status>",value=f"Add a `playing` status to statuses list.",inline=False)
		embed.add_field(name=f"{p}addlistening <status>",value=f"Add a `playing` status to statuses list.",inline=False)
		embed.add_field(name=f"{p}removestatus <id>",value="Removes a status from the list.",inline=False)
		await ctx.send(embed=embed)

	@commands.command(aliases=["mod"])
	async def moderation(self,ctx,page=None):
		p = self.bot.command_prefix
		embed = embeded()
		embed.description = "Moderation commands for moderating the server."
		if page is None or page=="1":
			embed.add_field(name=f"{p}ban <member> [reason]",value="Bans a member from the server.",inline=False)
			embed.add_field(name=f"{p}outban <user id>",value="Outbans a member from the server.",inline=False)
			embed.add_field(name=f"{p}softban <member> [delay] [reason]",value="Bans and unbans the member.",inline=False)
			embed.add_field(name=f"{p}unban <name#discriminator>",value="Unbans a user from the server.",inline=False)
			embed.add_field(name=f"{p}kick <member> [reason]",value="Kicks a member from the server.",inline=False)
			embed.add_field(name=f"{p}addrole <member> <role>",value="Adds a role to a member.",inline=False)
			embed.add_field(name=f"{p}removerole <member> <role>",value="Removes a role from a member.",inline=False)
			embed.add_field(name=f"{p}moderation 2",value="Shows the next page of moderation commands.",inline=False)
		elif page=="2":
			embed.add_field(name=f"{p}purge [amount]",value="Deletes an amount of messages.",inline=False)
			embed.add_field(name=f"{p}nuke [channel]",value="Deletes and re-creates a channel.",inline=False)
			embed.add_field(name=f"{p}lockdown [channel]",value="Locks a channel down.",inline=False)
			embed.add_field(name=f"{p}unlock [channel]",value="Unlocks a channel if it is locked.",inline=False)
			embed.add_field(name=f"{p}lockserver",value="Locks the entire server.",inline=False)
			embed.add_field(name=f"{p}unlockserver",value="Unlocks the entire server.",inline=False)
			embed.add_field(name=f"{p}blacklist <add/del> <word>",value="Updates the blacklisted words lists.",inline=False)
		else:
			embed.add_field(name=f"Invalid Page Number!!!",value=f"Currently there are 2 pages of moderation commands.")
		await ctx.send(embed=embed)

	@commands.command(aliases=["dev"])
	@commands.check(is_dev)
	async def devhelp(self,ctx):
		
		embed = embeded()
		p = self.bot.command_prefix
		embed.add_field(name=f"{p}devhelp",value="Help command for developers.",inline=False)
		embed.add_field(name=f"{p}privatepurge",value="Purges private channel messages.",inline=False)
		embed.add_field(name=f"{p}restart",value="Restarts the bot.",inline=False)
		embed.add_field(name=f"{p}ping",value="Calculates the current ping.",inline=False)
		embed.add_field(name=f"{p}api",value="Shows information about the current API.",inline=False)
		embed.add_field(name=f"{p}clear_console",value="Clears the current console.",inline=False)
		await ctx.author.send(embed=embed)

	@commands.command()
	async def utility(self,ctx):
		embed = embeded()
		p = self.bot.command_prefix
		embed.add_field(name=f"{p}changelogs",value="Shows all changelog commands.",inline=False)
		embed.add_field(name=f"{p}announce <channel> <message>",value="Says something with the current ping settings.",inline=False)
		await ctx.send(embed=embed)
	

	@commands.command()
	async def changelogs(self,ctx):
		embed = embeded()
		p = self.bot.command_prefix
		embed.description = "Changelog commands for custom applications. All useful information can be found down below.\n:warning: Warning : Use `_` in application names instead of spaces. It will be edited once the changelog is being sent."
		embed.add_field(name=f"{p}createcl <app name>",value="Creates an application database to log its changes.",inline=False)
		embed.add_field(name=f"{p}resetcl <app name>",value="Resets the changelog of an application.",inline=False)
		embed.add_field(name=f"{p}basedelcl <app name>",value="Deletes an application from the database.",inline=False)
		embed.add_field(name=f"{p}addcl <app name> <feature>",value="Adds an `added` feature to the changelog.",inline=False)
		embed.add_field(name=f"{p}removecl <app name> <feature>",value="Adds an `removed` feature to the changelog.",inline=False)
		embed.add_field(name=f"{p}improvecl <app name> <feature>",value="Adds an `improved` feature to the changelog.",inline=False)
		embed.add_field(name=f"{p}fixcl <app name> <feature>",value="Adds an `fixed` feature to the changelog.",inline=False)
		embed.add_field(name=f"{p}todocl <app name> <feature>",value="Extends the todo list of the changelog.",inline=False)
		embed.add_field(name=f"{p}delcl <app name> <feature>",value="Removes a feature from the database.",inline=False)
		embed.add_field(name=f"{p}sendcl <app name> [channel]",value="Sends the changelog of an application.",inline=False)
		await ctx.send(embed=embed)
		

def setup(bot:commands.Bot):
	bot.remove_command("help")
	bot.add_cog(HelpCog(bot))
