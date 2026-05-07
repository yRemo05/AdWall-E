import discord
from discord.ext import commands

from Cogs.Ext.Embed_Loader import embeded
from Cogs.Ext.General_Functions import edit,whatis


empty = ["",None,0]

class Security(commands.Cog,name=":shield:Security"):
    
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.command(
        name="blockmsg",
        usage="blockmsg <channel> <exception>",
        description="Deletes messages except exceptions like messages with attachments, embeds etc.."
    )
    async def blockmsg(self,ctx,channel:discord.TextChannel,*,exception):
        await ctx.message.delete()
        embed = embeded()
        block_dict = {str(channel.id):str(exception)}
        edit("message_overseer",block_dict)
        embed.description = "Message Overseer"
        if exception=="embeds" or exception=="attachments":
            embed.add_field(name="New Blocking Added :",value=f"All messages without {exception} will be deleted in <#{channel.id}> from now on.")
            await ctx.send(embed=embed)
    
    @commands.command(
        name="blacklist",
        usage="blacklist <add/rem> <word>",
        description="Blacklists a word.")
    async def blacklist(self,ctx,mode,*,word):
        await ctx.message.delete()
        edit(object="blacklisted_words",value=word,mode=mode)
        embed = embeded()
        situation = "Blacklisted" if mode=="add" else "Unblacklisted"
        embed.description = f"Blacklisted word : ||{word}||\nWho {situation} : {ctx.author}"
        await ctx.send(embed=embed,delete_after=10)

    

    @commands.command()
    async def lockserver(self,ctx:commands.Context):
        embed = embeded()
        embed.description = "Results of locking the server :\n-`All invites will be deleted.`\n-`Anyone who joins will be kicked.`\n-`All channels will be locked.`\n-`Ticket creation will be blocked.`\n-`Thread creation will be blocked.`\nNote that this may take a while."
        msg = await ctx.send(embed=embed)
        for invite in await ctx.guild.invites():
            await invite.delete(reason=f"Server is locked by {ctx.author}.")
        for channel in ctx.guild.channels:
            if channel.permissions_for(ctx.guild.default_role).send_messages:
                if isinstance(channel,discord.TextChannel):
                    await channel.set_permissions(ctx.guild.default_role,send_messages=False,read_messages=True)
                else:
                    await channel.set_permissions(ctx.guild.default_role,connect=False)
                edit("locked_channels",value=channel.id,path=3,mode="add")
        edit("is_server_locked",value=True,path=3)
        edit("server_locked_by",value=ctx.author.id,path=3)
        embed.description = "Results of locking the server :\n-`All invites are deleted.`\n-`Anyone who joins will be kicked from now on.`\n-`All channels are locked.`\n-`Ticket creation is blocked.`\n-`Thread creation is blocked.`\nServer is locked entirely."
        await msg.delete()
        await ctx.send(embed=embed)
        
    @commands.command()
    async def unlockserver(self,ctx:commands.Context):
        embed=embeded()
        embed.description = "Unlocking the entire server :\n-`Invites won't be deleted anymore.`\n-`Users will be able to join.`\n-`All channels will be unlocked.`\n-`Ticket creation will be allowed.`\n-`Thread creation will be allowed.`\nNote that this may take a while."
        msg = await ctx.send(embed=embed)
        locked_channels = whatis("locked_channels",3)
        for channel in ctx.guild.channels:
            if channel.id in locked_channels:
                if isinstance(channel,discord.TextChannel):
                    await channel.set_permissions(ctx.guild.default_role,send_messages=True,read_messages=True)
                else:
                    await channel.set_permissions(ctx.guild.default_role,connect=True)
                edit("locked_channels",value=channel.id,path=3,mode="remove")
        edit("is_server_locked",value=False,path=3)
        edit("server_locked_by",value="",path=3)
        embed.description = "Unlocking the entire server :\n-`Invites will not be deleted anymore.`\n-`Users can now join to the server.`\n-`Locked channels are now unlocked.`\n-`Ticket creation is allowed.`\n-`Thread creation is allowed.`\nServer is now unlocked!"
        await msg.delete()
        await ctx.send(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(Security(bot))