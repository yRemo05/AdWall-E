from operator import pos
import discord,asyncio
from discord.ext import commands
from random import randint
from Cogs.Ext.Embed_Loader import embeded
from Cogs.Ext.General_Functions import *

empty = [None,"",0]


class Moderation(commands.Cog, name=":hammer:Moderation"):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(
        name="ban",
        usage="ban <member> [reason]",
        description="Bans a member.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self,ctx,member:discord.Member,*,reason="No reason provided."):
        await ctx.message.delete()
        banmsg = whatis("ban_message")
        if not banmsg in empty:
            await member.send(banmsg)
        await member.ban(reason=reason)
        banemb = discord.Embed(title=f"{member} has been banned.",description=f"Who banned : {ctx.author}\nReason : {reason}")
        await ctx.send(embed=banemb)

    @commands.command(
        name="outban",
        usage="outban <user id>",
        description="Ban user who is not in server."
        )
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def outban(self,ctx, user_id,*,reason="No reason provided."):
        ctx.message.delete()
        author = ctx.message.author
        guild = author.guild
        user = guild.get_member(user_id)
        if user is not None:
            return await user.ban()
        await self.bot.http.ban(user_id, guild.id, 0)
        banemb = discord.Embed(title=f"{user_id} has been outbanned.",description=f"Who banned : {ctx.author}\nReason : {reason}")
        await ctx.send(embed=banemb)


    @commands.command(
        name="softban",
        usage="softban <user> [reason]",
        description="Instantly bans and unbans a user.")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self,ctx, member:discord.Member, delay=None,*, reason="No reason provided."):
        ban_message = whatis("ban_message")
        if not ban_message=="":
            await member.send(ban_message)
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member}, waiting {delay} seconds before unbanning..")
        if not delay==0 or not delay=="0" or not delay==None:
            await asyncio.sleep(delay)
        await ctx.guild.unban(member)
        return_msg = "Soft banned member `{}`".format(member.mention)
        if reason:
            return_msg += " for reason `{}`".format(reason)
        return_msg += "."
        await ctx.message.edit(content=return_msg)

    @commands.command(
        name="unban",
        usage="unban <member name + member discriminator>",
        description="Unbans a member.",
        brief="moderation users unban"
    )
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(ctx, *, member):    
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(title=f"Unbanned {user} from **{ctx.guild.name}**",description=f"Who unbanned : {ctx.author}",color=discord.Colour.green())
                await ctx.send(embed=embed)
    

    @commands.command(
        name="kick",
        usage="kick <member> [reason]",
        description="Kicks a member.",
        brief="moderation users kick"
    )
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx,member:discord.Member,*,reason="No reason provided."):
        await ctx.message.delete()
        kick_message = whatis("kick_message")
        if not kick_message is None:
            await member.send(kick_message)
        await member.kick(reason=reason)
        embed = discord.Embed(title=f"{member} has been kicked.",description=f"Who Kicked : {ctx.author}\nReason : {reason}",color=discord.Colour.red())
        await ctx.send(embed=embed)

    @commands.command()
    async def mute(self,ctx:commands.Context,member:discord.Member,seconds):
        
        # ! API doesn't support the `timeout` function yet.
        # ! So instead of doing it with a request, wait for the API to be updated.

        pass
    
    @commands.command(
        name="purge",
        usage="purge [amount]",
        description="Clears amount of messages."
    )
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self,ctx,amount=5):
        await ctx.message.delete()
        if not amount>100:
            await ctx.channel.purge(limit=amount)
        else:
            return await ctx.send("Sorry, I cannot delete more then 100 messages at a time.")
            
    

    @commands.command(
        name="nuke",
        usage="nuke <channel>",
        description="Deletes and re-creates a channel."
    )
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def nuke(self,ctx,channel:discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        if channel.category==None:
            Name = channel.name
            await channel.delete()
            channel = await ctx.guild.create_text_channel(name=Name)
        else:
            Cate = channel.category
            Name = channel.name
            Pos = channel.position
            await channel.delete()
            new_chan = await ctx.guild.create_text_channel(name=Name,category=Cate,position=Pos)
        embed =discord.Embed(title="Nuked the channel.",description="This channel is now reloaded and is now clean!:bomb::radioactive:",color=discord.Colour.orange())
        embed.set_image(url="https://media.giphy.com/media/XUFPGrX5Zis6Y/giphy.gif")
        await new_chan.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lockdown(self,ctx:commands.Context,channel:discord.TextChannel=None):
        embed = embeded()
        embed.description = f":warning:Lockdown Is Triggered!\nThis channel is locked until further notice by <@{ctx.author.id}> !:lock:\nOnly administrators can send messages from now on."
        if channel is None:
            channel = ctx.channel
        await channel.set_permissions(ctx.guild.default_role,send_messages=False,read_messages=True)
        edit("locked_channels",channel.id,path=3)
        await channel.send(embed=embed)
        if channel != ctx.channel:
            await ctx.send("Channel Is Locked!:white_check_mark:",delete_after=10)


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def unlock(self,ctx:commands.Context,channel:discord.TextChannel=None):
        embed = embeded()
        embed.description = f":unlock:Unlocking Is Triggered!\nThis channel is unlocked for use by <@{ctx.author.id}> !"
        if channel is None:
            channel = ctx.channel
        locked_channels = whatis("locked_channels",3)
        if not channel.id in locked_channels:
            return await ctx.send("This channel is not locked!:x:",delete_after=10)
        edit("locked_channels",channel.id,path=3,mode="rem")
        await channel.set_permissions(ctx.guild.default_role,send_messages=True,read_messages=True)
        await channel.send(embed=embed)
        if channel != ctx.channel:
            await ctx.send("Unlocked the channel successfully! :white_check_mark:",delete_after=10)




    @commands.command(
        name="addrole",
        usage="addrole <member> <role>",
        description="Adds a role to someone.")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def addrole(self,ctx,member:discord.Member,role:discord.Role):
        embed = embeded()
        embed.description = "Moderation - Adding Role"
        if ctx.author.top_role.position<role.position and not member==member.guild.owner:
            embed.add_field(name="Error Occured :no_entry: :",value=f"You can't manage a role higher than your top role.")
        else:
            await member.add_roles(role)
            embed.add_field(name="Role Added :white_check_mark: :",value=f"Role <@&{role.id}> has been given to <@{member.id}> successfully!")
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["removerole"])
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def remrole(self,ctx,member:discord.Member,role:discord.Role):
        embed = embeded()
        embed.description = "Moderation - Removing Role"
        if ctx.author.top_role.position<role.position and not member==member.guild.owner:
            embed.add_field(name="Error Occured :no_entry: :",value=f"You can't manage a role higher than your top role.")
        else:
            await member.remove_roles(role)
            embed.add_field(name="Role Removed :white_check_mark: :",value=f"Role <@&{role.id}> has been removed from <@{member.id}> successfully!")
        await ctx.send(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(Moderation(bot))
