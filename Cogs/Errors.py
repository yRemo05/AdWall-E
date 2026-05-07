from discord.ext import commands
from discord.ext.commands import Cog,Bot
from discord.errors import Forbidden
from Cogs.Ext.Embed_Loader import embeded
from Cogs.Ext.General_Functions import err


class Errors(Cog,name="Errors"):
    def __init__(self,bot:Bot):
        self.bot = bot


    @Cog.listener()
    async def on_command_error(self, ctx:commands.Context, error:commands.CommandError):
        embed = embeded()
        embed.description = ":x: An error occured!"
        embed.color = 0x8c0900
        if isinstance(error, commands.CommandOnCooldown):
            day = round(error.retry_after/86400)
            hour = round(error.retry_after/3600)
            minute = round(error.retry_after/60)
            if day > 0:
                await ctx.send('This command has a cooldown, for '+str(day)+ "day(s)")
            elif hour > 0:
                await ctx.send('This command has a cooldown, for '+str(hour)+ " hour(s)")
            elif minute > 0:
                await ctx.send('This command has a cooldown, for '+ str(minute)+" minute(s)")
            else:
                await ctx.send(f'This command has a cooldown, for {error.retry_after:.2f} second(s)')
        elif isinstance(error,commands.MissingAnyRole):
            embed.add_field(name="Missing Roles",value="You don't have the required roles to execute this command!")
        elif isinstance(error,commands.MissingPermissions):
            embed.add_field(name="Missing Permissions",value="You don't have the required permissions to execute this command!")
        elif isinstance(error,commands.CheckFailure):
            embed.add_field(name="Missing Permissions",value="You are not allowed to use this command!")
        elif isinstance(error,commands.MissingRequiredArgument):
            embed.add_field(name="Missing Required Argument.",value=f"{error.param.name} is a required argument that is missing.")
        elif isinstance(error,commands.CommandNotFound):
            return
            #embed.add_field(name="Invalid Command :",value=f"The command you typed is invalid. Please use `{self.bot.command_prefix}help` to see all commands.",inline=False)
        elif isinstance(error,commands.UserNotFound):
            embed.add_field(name="Invalid User :",value=f"Cannot find such a user.",inline=False)
        elif isinstance(error,commands.RoleNotFound):
            embed.add_field(name="Invalid Role :",value=f"Cannot find such a role. Please make sure that they are valid roles in : **{ctx.guild.name}**",inline=False)
        elif isinstance(error,commands.MemberNotFound):
            embed.add_field(name="Invalid Member :",value=f"Cannot find such a member. Please make sure that they are in the server : **{ctx.guild.name}**",inline=False)
        elif isinstance(error,commands.ChannelNotFound):
            embed.add_field(name="Invalid Channel :",value=f"Cannot find such a channel. Please make sure that they are in the server : **{ctx.guild.name}**",inline=False)
        elif isinstance(error,Forbidden):
            embed.add_field(name="Not Enough Permissions",value=f"You cannot execute the {ctx.command.name} command, not enough permissions.",inline=False)
        elif isinstance(error,commands.BotMissingPermissions):
            embed.add_field(name="Not Enough Permissions",value=f"I am not authorized to execute the {ctx.command.name} command, not enough permissions.",inline=False)
        if len(embed.fields) != 0:
            await ctx.send(embed=embed)
        err(error)


def setup(bot:Bot):
    bot.add_cog(Errors(bot))