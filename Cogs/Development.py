import discord,time,os
from discord.ext import commands
from discord.ext.commands.core import group
from Cogs.Ext.Checks import is_dev
from Cogs.Ext.Embed_Loader import embeded
from Cogs.Ext.General_Functions import edit, restart, whatis


class Development(commands.Cog,name=":mag:Development"):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    
    @commands.command()
    @commands.check(is_dev)
    async def restart(self,ctx):
        await ctx.message.delete()
        await ctx.send("Restarting...")
        restart()

    
    @commands.command(name = "ping",
                    usage="ping",
                    description = "Display the bot's ping.")
    @commands.check(is_dev)
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("🏓 Pong !")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"🏓 Pong !  `{int(ping)} ms`")

    @commands.check(is_dev)
    @commands.command(
        name="devapi",
        usage="devapi",
        description="Shows the API information.")
    async def devapi(self,ctx):
        embed = embeded()
        API_PING = round(self.bot.latency * 1000)
        embed.add_field(name=f"API Name :",value=f"{discord.__name__}",inline=True)
        embed.add_field(name=f"API Latency :",value=f"{API_PING}ms",inline=True)
        embed.add_field(name="API Version",value=f"{discord.__version__}",inline=True)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.check(is_dev)
    async def clear_console(self,ctx):
        try:
            await ctx.message.delete()
        except:pass
        os.system("cls")

    @commands.check(is_dev)
    @commands.command()
    async def privatepurge(self,ctx):
        await ctx.send("Please wait...")
        embed= embeded()
        deleted = 0
        groups = 0
        dms = 0
        failed = 0
        for privc in self.bot.private_channels:
            print(privc)
            
            async for message in privc.history(limit=200):
                if message.author==self.bot.user:
                    try:
                        await message.delete()
                        deleted += 1
                    except:
                        failed += 1
        embed.description = f"Successfully cleared all private channel messages :\n[!] Total DM channels found : `{dms}`\n[!] Total group channels found : `{groups}`\n[!] Total messages found : `{failed+deleted}`\n[+] Deleted messages : `{deleted}`\n[x] Failed Messages : `{failed}`"
        await ctx.send(embed=embed)

    @commands.check(is_dev)
    @commands.command()
    async def specpurge(self,ctx:commands.Context,limit,*,author=None):
        embed = embeded()
        deleted = 0
        dms = 0
        failed = 0
        if author is None:
            author = ctx.author
            await author.create_dm()
            async for message in author.dm_channel.history(limit=int(limit)):
                if message.author==self.bot.user:
                    deleted += 1
                    await message.delete()
            embed.description = f"Cleared __{deleted}__ messages from <@{author.id}> :white_check_mark:"
            return await ctx.send(embed=embed)
        
        elif author=="all":
            msg = await ctx.send("Purging direct messages...")
            for member in ctx.guild.members:
                await member.create_dm()
                author = member
                await msg.edit(content=f"Purging direct messages sent to {member}...")
                if self.bot.user == author:
                    continue
                try:
                    async for message in author.dm_channel.history(limit=int(limit)):
                        if message.author==self.bot.user:
                            try:
                                deleted += 1
                                await message.delete()
                            except:
                                failed += 1
                    dms += 1
                except:
                    pass
            embed.description = f"Successfully cleared all private channel messages :\n[!] Total DM channels found : `{dms}`\n[!] Total messages found : `{failed+deleted}`\n[+] Deleted messages : `{deleted}`\n[x] Failed Messages : `{failed}`"
            return await ctx.send(embed=embed)        

        else:
            author = ctx.author
            await author.create_dm()
            async for message in author.dm_channel.history(limit=int(limit)):
                if message.author==self.bot.user:
                    deleted += 1
                    await message.delete()
            embed.description = f"Cleared __{deleted}__ messages from <@{author.id}> :white_check_mark:"
            return await ctx.send(embed=embed)
        
    @commands.command()
    async def logging(self,ctx,*,toogle):
        embed = embeded()
        embed.description = f"Logging is toogled __{toogle}__"
        if toogle.lower()=="on":
            edit("logging",True,path=1)
        elif toogle.lower()=="off":
            edit("logging",False,path=1)
        else:
            embed.description = f":x: Error Occured!\n\nThere is no such a toogle mode : {toogle}\nTry using `on`/`off`"
            return await ctx.send(embed=embed)
        return await ctx.send(embed=embed)

    @commands.command()
    async def reset_config(self,ctx):
        embed = embeded()
        configuration_json = {
        "application_ID": self.bot.id,
        "token": whatis("token"),
        "prefix": "!",
        "delete_commands": True,
        "settings_perms": [],
        "ticket_perms": [],
        "giveaway_perms": [],
        "mod_perms": [],
        "ticket_category": 0,
        "ticket_message": 0,
        "ticket_welcome": "Hello {user_name}! Thank you for creating a ticket in {server}. Please be patient, our support team will be with you as soon as possible!!! \ud83c\udf89",
        "ticket_information_channel": 0,
        "------------------------Ping_Settings": "Ping_Settings------------------------",
        "ghost_ping": False,
        "ping_everyone": True,
        "ping_here": False,
        "------------------------Embed_Settings": "Embed_Settings------------------------",
        "embed_title": "",
        "image_url": "",
        "thumbnail_logo_url": "",
        "color_hex_code": None,
        "embed_footer_text": "",
        "embed_footer_url": "",
        "------------------------Member_Events": "Member_Events------------------------",
        "member_welcome_description": "Hello {user_name}, please enjoy your time on our server : {server}!",
        "member_left_description": "Hope to see you soon {user_name} \ud83d\ude26",
        "welcome_channel": 0,
        "bye-bye_channel": 0,
        "role_to_assing_to_joined_member": 0,
        "------------------------Moderation_Settings": "Moderation_Settings------------------------",
        "kick_message": "",
        "ban_message": "",
        "blacklisted_words": [],
        "------------------------OverSeers": "OverSeers------------------------",
        "message_overseer": [{}],
        "------------------------Server_Stats": "Server_Stats------------------------",
        "stats_category": 0,
        "channel_counter": {
            "enabled?": False,
            "channel_id": 0
        },
        "role_counter": {
            "enabled?": False,
            "channel_id": 0
        },
        "member_counter": {
            "enabled?": False,
            "channel_id": 0
        },
        "------------------------Development_Credits": "Development_Credits------------------------",
        "logging":True,
        "Developer_IDs": [
            609703131747450880
        ]}
        with open("Data\\configuration.json","w") as f:
            f.write(configuration_json)
            f.close()
        embed.description = "Configuration database is now resetted. :white_check_mark:"
        return await ctx.send(embed=embed)
        
        

def setup(bot:commands.Bot):
    bot.add_cog(Development(bot))