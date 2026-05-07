from discord.abc import PrivateChannel
from discord.enums import ButtonStyle
from discord.errors import Forbidden
from discord.ext import commands
import discord
from Cogs.Ext.Embed_Loader import embeded, load_message_payload
from Cogs.Ext.General_Functions import edit, setup_user_db, whatis,log,count_commands
from discord.utils import get
from Cogs.Ext.Watchers import create_ticket
from main import status_loop


empty = [None,"",0]

class Events(commands.Cog,name="Events"):
    def __init__(self,bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        commands_count = count_commands(self.bot)
        log(f"Logged In As : {self.bot.user}")
        log(f"Total Commands : {commands_count}")
        log("Discord API Version : "+discord.__version__)
        log("Discord API Name : "+discord.__name__)
        status_loop.start()
        #await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"the new updates!"))
            
                


    @commands.Cog.listener()
    async def on_command(self,ctx):
        log(f"Command Used : {ctx.command.name}")
        if whatis("delete_commands") is True:
            try:await ctx.message.delete()
            except:pass


    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        prefix = whatis("prefix")
        embed = embeded()
        embed.description = f"Greetings {guild.owner.name}! Today we want to thank you for choosing us in this journey! :heart: :tada:\nLet us give you some tips before beginning >>>"
        embed.add_field(name="What First?",value="First thing you should do is set the permissions for roles.\n  - ``ticket_perms <give/remove> <role>``\n  - ``giveaway_perms <give/remove> <role>``\n  - ``settings_perms <give/remove> <role>``\netc..",inline=False)    
        embed.add_field(name="What Next?",value=f"Configure things. For this ``{prefix}settings`` will help you configure the bot. But not doing these things wont actually cause some errors! :slight_smile:",inline=False)
        embed.add_field(name="Can I Customize The Appereance?",value="Of course! Response embed, bot's avatar, username... Doing this is optional of course!",inline=False)
        embed.add_field(name="What To Do In Case Of Any Errors?",value="Well, any occured error will be reported to our developers! It will be fixed ASAP.",inline=False)
        embed.add_field(name="Where To Report Our Suggestions?",value="We got you covered! You can join to our discord down below, and let us know your thoughts!",inline=False)
        embed.set_footer(text=f"Created a database for {guild.member_count} members!",icon_url=guild.owner.avatar)
        for member in guild.members:
            if member==self.bot.user or member.bot:
                continue
            setup_user_db(member)
        view = discord.ui.View(timeout=None)
        discord_redirection_button = discord.ui.Button(style=ButtonStyle.link,label="Support Server",url="https://discord.gg/gdBEABg8DX")
        view.add_item(discord_redirection_button)
        await guild.owner.send(embed=embed,view=view)
        


    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        setup_user_db(member)
        if whatis("is_server_locked",3):
            locking_author = whatis("server_locked_by",3)
            user = self.bot.get_user(locking_author)
            await member.send(f"Sorry, this server is locked by {user}. Try again later.")
            return await member.kick(reason=f"Server is locked by {user}.")
        role_id = whatis("role_to_assing_to_joined_member")
        if not role_id in empty:
            role = get(member.guild.roles, id=role_id)
            await member.add_roles(role,reason="Auto-Role system")
        welchanID = whatis("welcome_channel")
        if not welchanID in empty:
            WelChan = await self.bot.fetch_channel(welchanID)
            embed=embeded()
            embed.set_thumbnail(url=member.avatar)
            welcome_description = whatis("member_welcome_description")
            if welcome_description in empty:
                embed.description = f"Welcome to {member.guild.name}, {member.name}!"
            else:
                embed.description = load_message_payload(message=welcome_description,member=member)
            await WelChan.send(content=member.mention,embed=embed)
        if whatis("member_counter")["enabled?"]:
            try:
                channel = self.bot.get_channel(whatis("member_counter")["channel_id"])
                await channel.edit(name=f"Member Count : {member.guild.member_count}")
            except:
                pass


    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        embed = embeded()
        left_description = whatis("member_left_description")
        if left_description in empty:
            embed.description = f"{member.name} just left us!"
        else:
            embed.description = load_message_payload(message=left_description,member=member)
        try:
            byeChanID = whatis("bye-bye_channel")
            byeChan = self.bot.get_channel(byeChanID)
            await byeChan.send(embed=embed)
        except:
            pass


    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author==self.bot.user or message.author.bot:
            return
        is_blacklisted_used=False
        embed = embeded()
        embed.description = "Message Overseer Warning :warning:"
        message_overseer = whatis("message_overseer")
        blacklisted_message_list = whatis("blacklisted_words")
        # Channel Overseer
        for overseer in message_overseer:
            try:
                overseer_blocking_exception_object = overseer[str(message.channel.id)]
                embed.add_field(name="Detected Unauthorized Activity :",value=f"Do not send messages except {overseer_blocking_exception_object} in this channel!!!")
                if overseer_blocking_exception_object=="embeds" and not message.embeds:
                    await message.delete()
                    await message.channel.send(content=message.author.mention,embed=embed,delete_after=10)
                    break
                elif overseer_blocking_exception_object=="attachments" and not message.attachments:
                    await message.delete()
                    await message.channel.send(content=message.author.mention,embed=embed,delete_after=10)
                    break
            except:
                continue
        # Blacklisted_Word_Manager
        for word in blacklisted_message_list:
            if word in message.content:
                try:await message.delete()
                except:pass
                embed.add_field(name="Detected Imporer Act",value=f"Please don't use the blacklisted words.")
                await message.channel.send(content=message.author.mention,embed=embed,delete_after=10)
                is_blacklisted_used = True
        if is_blacklisted_used is False and not isinstance(message.channel,PrivateChannel):
            message_count = whatis("messages",f"Data\\User Data\\{message.author.id}.json")
            message_count += 1
            edit("messages",value=message_count,path=f"Data\\User Data\\{message.author.id}.json")



    @commands.Cog.listener()
    async def on_interaction(self,interaction:discord.Interaction):
        #print(f"{interaction.data}")
        if interaction.data["custom_id"]=='create_ticket_button' and int(whatis("ticket_message"))==int(interaction.message.id):
            if whatis("is_server_locked"):
                return await interaction.response.send_message("Error while creating : Server is locked.")
            ticket_channel = await create_ticket(self.bot,interaction)
            ticket_msg = whatis("ticket_welcome")
            if not ticket_msg in empty:
                embed = embeded()
                ticket_msg = load_message_payload(ticket_msg,interaction)
                embed.description = ticket_msg
                await ticket_channel.send(embed=embed)
        
        if interaction.data["custom_id"]=="role_selector" and not whatis(str(interaction.message.id),2) is None:
            msgpylod = whatis(str(interaction.message.id),2)
            emoji = interaction.data['values'][0]
            role_id = msgpylod[emoji]
            role = discord.utils.get(interaction.guild.roles,id=int(role_id))
            await interaction.user.add_roles(role)
            try:await interaction.response.send_message(f"{role.name} role has been added to {interaction.user.name}!")
            except:pass


    @commands.Cog.listener()
    async def on_invite_create(self, invite:discord.Invite):
        if whatis("is_server_locked",3):
            locking_author = whatis("server_locked_by",3)
            user = self.bot.get_user(locking_author)
            await invite.delete(reason=f"Server is locked by {user}.")


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel:discord.abc.GuildChannel):
        if whatis("channel_counter")["enabled?"]:
            try:
                channel = self.bot.get_channel(whatis("channel_counter")["channel_id"])
                await channel.edit(name=f"Channel Count : {len(channel.guild.channels)}")
            except:
                pass

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel:discord.abc.GuildChannel):
        if whatis("channel_counter")["enabled?"]:
            try:
                channel = self.bot.get_channel(whatis("channel_counter")["channel_id"])
                await channel.edit(name=f"Channel Count : {len(channel.guild.channels)}")
            except:
                pass


    @commands.Cog.listener()
    async def on_guild_role_create(self, role:discord.Role):
        if whatis("role_counter")["enabled?"]:
            try:
                channel = self.bot.get_channel(whatis("role_counter")["channel_id"])
                await channel.edit(name=f"Role Count : {len(role.guild.roles)}")
            except:
                pass
    

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role:discord.Role):
        if whatis("role_counter")["enabled?"]:
            try:
                channel = self.bot.get_channel(whatis("role_counter")["channel_id"])
                await channel.edit(name=f"Role Count : {len(role.guild.roles)}")
            except:
                pass
    
    
        

    
        

def setup(bot:commands.Bot):
    bot.add_cog(Events(bot))