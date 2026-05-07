import discord
from discord.embeds import E
from discord.ui import Button,Select
from discord.enums import ButtonStyle
from discord.ext import commands
from discord.ui import View
from Cogs.Ext.Embed_Loader import embeded
from Cogs.Ext.General_Functions import edit,set_role_system, whatis

empty = [None,"",0]

class Settings(commands.Cog,name=":gear:Settings"):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def prefix(self,ctx,*,new_prefix):
        embed = embeded()
        old_prefix = self.bot.command_prefix
        self.bot.command_prefix = new_prefix
        embed.description = f"Prefix is changed successfully. Commands will now be executed with the new prefix.\nOld Prefix : `{old_prefix}`\nNew Prefix : `{self.bot.command_prefix}`"
        edit("prefix",str(new_prefix))
        await ctx.send(embed=embed)
    
    @commands.command()
    async def deletecommands(self,ctx,*,toogle):
        embed = embeded()
        if toogle=="on":
            embed.description = "Deleting commands is __on__, from now on the command messages will be deleted."
            edit("delete_commands",value=True)
        elif toogle=="off":
            embed.description = "Deleting commands is __off__, the command messages will not be deleted anymore."
            edit("delete_commands",value=False)
        else:
            return await ctx.send("Invalid mode is chosen, mode should be either `on` or `off`.")
        await ctx.send(embed=embed)

    @commands.command(
        name="createddm",
        usage="createddm <channel>",
        description="Sets up a role system with a dropdown menu.",
        aliases=["createdropdownmenu"])
    async def createddm(self,ctx,channel:discord.TextChannel=None):
        await ctx.message.delete()
        if channel is None:
            channel = ctx.channel
        view = discord.ui.View(timeout=None)
        Select_Menu = Select(custom_id="role_selector",placeholder="Choose a role from here!")
        emoji_role_dict = {}
        done = False
        while 1:
            embed = embeded()
            embed.add_field(name="Input a role :",value=f"``emoji role_id``",inline=False)
            embed.add_field(name="Tip :",value="This will continue forever. If you want to stop adding roles to the menu and complete the setup, type ``done``. If you want to cancel it type ``cancel``.",inline=False)
            msged = await ctx.send(embed=embed)
            def check(m):
                return m.author==ctx.author and ctx.channel==m.channel
            returned_msg = await self.bot.wait_for("message",check=check)
            if returned_msg.content == "done":
                done=True
                break
            elif returned_msg.content == "cancel":
                done=False
                break
            emoji,role_id = returned_msg.content.split(" ")
            emoji_role_dict[str(emoji)] = str(role_id)
            role = discord.utils.get(ctx.guild.roles,id=int(role_id))
            if role is None:
                msg = await ctx.send("Invalid role ID input, please try again.",delete_after=10)
                await msged.delete()
                await returned_msg.delete()
                continue
            await msged.delete()
            await returned_msg.delete()
            Select_Menu.add_option(label=f"{role.name}",value=f"{emoji}",description=f"Click to get {role.name} role!",emoji=emoji)
        if done is False:
            return await ctx.send("Role setup has been canceled.")
        view.add_item(Select_Menu)
        embed = embeded()
        embed.description = f"Custom Role Selector\nGet a role by clicking on it in the select menu down below! Once you click on it, you will instantly get your role! :tada:"
        embed_msg = await channel.send(embed=embed,view=view)
        set_role_system(embed_msg.id,emoji_role_dict)
            
        #set_reaction_role(ctx.message.id,created_list)
        
        if done is None:
            embed = embeded()
            embed.description = "Dropdown Role Menu setup has been canceled! Use ``setuprr <channel>`` to restart."
            return await ctx.send(embed=embed)
        
        embed = embeded()
        embed.description = f"Dropdown Role Menu setup is completed! Setting up the reaction role system in <#{channel.id}>!:tada:"
        await ctx.send(embed=embed)
    

    @commands.command()
    async def deleteddm(self,ctx:commands.Context,*,message_id):
        for channel in ctx.guild.channels:
            try:msg = await channel.fetch_message(int(message_id))
            except:continue
        if msg is None:
            return await ctx.send(f"Cannot find a message with the ID : {message_id}")
        config = whatis(str(msg.id),path=2)
        if config is None:
            return await ctx.send("Message is not found in the database.")
        edit(str(msg.id),mode="remove",path=2)
        chan_id = msg.channel.id
        await msg.delete()
        embed = embeded()
        embed.description = f"Drop down menu in <#{chan_id}> is removed and deleted from the database."
        return await ctx.send(embed=embed)
        
        
        

    @commands.command()
    async def welchannel(self,ctx,*,channel:discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        embed = embeded()
        embed.description = f"<#{channel.id}> is set for logging the joined members. :thumbsup:"
        edit("welcome_channel",channel.id)
        await ctx.send(embed=embed)

    @commands.command()
    async def byechannel(self,ctx,channel:discord.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        await ctx.message.delete()
        embed = embeded()
        embed.description = f"<#{channel.id}> is set for logging the members who left! :thumbsup:"
        edit("bye-bye_channel",channel.id)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def setwelcomemsg(self,ctx):
        embed = embeded()
        embed.description = "Please input a welcome message for the new members. Here are some mentioning methods you can use :\n - `{user_mention}` : Mentions the user.\n - `{user_name}` : Is replaced with the username.\n - `{server}` : Is replaced with the server name."
        emed = await ctx.send(embed=embed)
        def check(m):
            return m.author==ctx.author and m.channel==ctx.channel
        msg = await self.bot.wait_for("message",check=check)
        edit("member_welcome_description",msg.content)
        await msg.delete()
        embed = embeded()
        embed.description = "Member welcoming message is set, and will be used from now on."
        await emed.delete()
        await ctx.send(embed=embed)
    
    
    @commands.command()
    async def setbyemsg(self,ctx):
        embed = embeded()
        embed.description = "Please input a bye message for the leaving members. Here are some mentioning methods you can use :\n - `{user_mention}` : Mentions the user.\n - `{user_name}` : Is replaced with the username.\n - `{server}` : Is replaced with the server name."
        emed = await ctx.send(embed=embed)
        def check(m):
            return m.author==ctx.author and m.channel==ctx.channel
        msg = await self.bot.wait_for("message",check=check)
        edit("member_left_description",msg.content)
        await msg.delete()
        embed = embeded()
        embed.description = "Member bye message is set, and will be used from now on."
        await emed.delete()
        await ctx.send(embed=embed)
    
            
    @commands.command(
        name="autorole",
        usage="autorole <role>",
        description="Gives the mentioned role to new members."
    )
    async def autorole(self,ctx,role:discord.Role):
        edit("role_to_assing_to_joined_member",int(role.id))
        embed = embeded()
        embed.description = f"The Role <@&{role.id}> has been assigned for the auto role system for {ctx.guild.name}!"
        await ctx.send(embed=embed)
        

    @commands.command()
    async def modperms(self,ctx,mode,role:discord.Role):
        await ctx.message.delete()
        embed=embeded()
        if mode=="add":
            embed.description = f"<@&{role.id}> now has access to moderation commands and help."
        elif mode=="rem":
            embed.description = f"<@&{role.id}>'s permissions for moderation commands and help is now removed. They can't use them anymore."
        else:
            return await ctx.send("Mode is not a valid word.")
        edit("mod_perms",int(role.id),mode)
        await ctx.send(embed=embed)
    

    @commands.command()
    async def settingsperms(self,ctx,mode,role:discord.Role):
        await ctx.message.delete()
        embed=embeded()
        if mode=="add" or mode=="give":
            embed.description = f"<@&{role.id}> now has access to settings."
        elif mode=="rem" or mode=="remove":
            embed.description = f"<@&{role.id}>'s permissions for settings is now removed. They can't use them anymore."
        else:
            return await ctx.send("Mode is not a valid word.")
        edit("settings_perms",int(role.id),mode)
        await ctx.send(embed=embed)

    # TODO add ticketperms
    # TODO add giveawayperms


    @commands.command()
    async def ticketsetup(self,ctx:commands.Context,channel:discord.TextChannel=None):
        await ctx.message.delete()
        if channel is None:
            channel = ctx.channel
        embed = embeded()
        embed.description = f"Support Ticket"
        Create_ticket_Button = Button()
        Create_ticket_Button.custom_id = "create_ticket_button"
        Create_ticket_Button.label = "Ticket Support"
        Create_ticket_Button.style = ButtonStyle.blurple
        Create_ticket_Button.emoji = "🎫"
        viewed = View(timeout=None)
        viewed.add_item(Create_ticket_Button)
        msg = await ctx.send(embed=embed,view=viewed)
        edit("ticket_message",msg.id)

    @commands.command(aliases=["setticketwelcome","ticketwelcome","ticketwelcomemsg","ticketwelcomemessage","ticketwelcoming"])
    async def setticketwelcoming(self,ctx):
        embed = embeded()
        embed.description = "Please Input a ticket message. Here are some mentioning methods you can use :\n - `{user_mention}` : Mentions the user.\n - `{user_name}` : Being replaced with the username.\n - `{server}` : Is replaced with the server name."
        emed = await ctx.send(embed=embed)
        def check(m):
            return m.author==ctx.author and m.channel==ctx.channel
        msg = await self.bot.wait_for("message",check=check)
        edit("ticket_welcome",msg.content)
        await msg.delete()
        embed = embeded()
        embed.description = "Ticket message is set! The message will be send to the new tickets! You can change this anytime you want by executing `setticketwelcoming`. :thumbsup:"
        await emed.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def setticketpanel(self,ctx,category_id):
        try:
            embed = embeded()
            if category_id != "off":
                category = self.bot.get_channel(int(category_id))
                edit("ticket_category",int(category.id))
                embed.description = f"{category.name} is now set as a ticket panel. Tickets will be created in here."
            else:
                edit("ticket_category",0)
                embed.description = f"Ticket panels are now closed. Tickets will be created on top of the server."
            await ctx.send(embed=embed)
        except:
            return await ctx.send("Invalid category id.")

    @commands.command()
    async def setticketlog(self,ctx:commands.Context,channel:discord.TextChannel=None):
        await ctx.message.delete()
        embed = embeded()
        if channel is None:
            channel = ctx.channel
        embed.description = f"<#{channel.id}> is set for logging ticket information.:gear: Following will be sent :\n - `Ticket Transcript`\n - `Ticket Owner`\n - ``Ticket Name`\n - `Ticket Panel`\n - `Users In Ticket`"
        edit("ticket_information_channel",channel.id)
        await ctx.send(embed=embed)

    # DESIGN COMMANDS

    @commands.command()
    async def embed_title(self,ctx,*,title=None):
        await ctx.message.delete()
        edit("embed_title",str(title))
        embed = embeded()
        embed.description = f"Title is set and will be used from now on : {title}"
        await ctx.send(embed=embed)
    
    @commands.command()
    async def embed_image(self,ctx,*,image_url=None):
        await ctx.message.delete()
        edit("image_url",str(image_url))
        embed =embeded()
        embed.description = f"Image is set and will be used from now on!"
        await ctx.send(embed=embed)
    
    @commands.command()
    async def embed_thumbnail(self,ctx,*,thumbnail_url=None):
        await ctx.message.delete()
        edit("thumbnail_logo_url",thumbnail_url)
        embed = embeded()
        embed.description = "Thumbnail is set and will be used from now on!"
        await ctx.send(embed=embed)
    
    @commands.command()
    async def embed_footer(self,ctx,icon_url=None,*,text=None):
        await ctx.message.delete()
        edit("embed_footer_text",text)
        if not icon_url is None:
            edit("embed_footer_url",icon_url)
        embed = embeded()
        embed.description = "Footer is set and will be used from now on!"
        await ctx.send(embed=embed)

    @commands.command()
    async def embed_color(self,ctx,*,hex_code=None):
        await ctx.message.delete()
        edit("color_hex_code",str(hex_code))
        embed=embeded()
        embed.description = f"New Color is set for the embed design : {hex_code}"
        await ctx.send(embed=embed)
            
    #STATS

    @commands.command()
    async def channelcounter(self,ctx:commands.Context,mode):
        if not whatis("stats_category") in empty:
            category = self.bot.get_channel(whatis("stats_category"))
        else:
            category = await ctx.guild.create_category("Server-Stats",position=0)
            edit("stats_category",int(category.id))
        
        if mode=="on":
            edit("channel_counter","enabled?",True)
            channels_count = len(ctx.guild.channels)
            channel = await ctx.guild.create_voice_channel(name=f"Channel Count : {channels_count}",category=category)
            await channel.set_permissions(ctx.guild.default_role,connect=False)
            edit("channel_counter","channel_id",int(channel.id))
    
        elif mode=="off":
            edit("channel_counter","enabled?",False)
            try:
                channel = self.bot.get_channel(whatis("channel_counter")["channel_id"])
                await channel.delete()
            except:pass
            edit(object="channel_counter",value="channel_id",alt_value=0)
        else:
            return await ctx.send("Invalid mode, please type either `on` or `off`.")
        embed = embeded()
        embed.description = f"Channel counter is __{mode}__."
        await ctx.send(embed=embed)


    @commands.command()
    async def rolecounter(self,ctx:commands.Context,mode):
        if not whatis("stats_category") in empty:
            category = self.bot.get_channel(whatis("stats_category"))
        else:
            category = await ctx.guild.create_category("Server-Stats",position=0)
            edit("stats_category",int(category.id))
        
        if mode=="on":
            edit("role_counter","enabled?",True)
            roles_count = len(ctx.guild.roles)
            channel = await ctx.guild.create_voice_channel(name=f"Role Count : {roles_count}",category=category)
            await channel.set_permissions(ctx.guild.default_role,connect=False)
            edit("role_counter","channel_id",int(channel.id))
    
        elif mode=="off":
            edit("role_counter","enabled?",False)
            try:
                channel = self.bot.get_channel(whatis("role_counter")["channel_id"])
                await channel.delete()
            except:pass
            edit("role_counter","channel_id",0)
        else:
            return await ctx.send("Invalid mode, please type either `on` or `off`.")
        embed = embeded()
        embed.description = f"Role counter is __{mode}__."
        await ctx.send(embed=embed)

    
    @commands.command()
    async def membercounter(self,ctx:commands.Context,mode):
        if not whatis("stats_category") in empty:
            category = self.bot.get_channel(whatis("stats_category"))
        else:
            category = await ctx.guild.create_category("Server-Stats",position=0)
            edit("stats_category",int(category.id))
        
        if mode=="on":
            edit("member_counter","enabled?",True)
            members_count = ctx.guild.member_count
            channel = await ctx.guild.create_voice_channel(name=f"Member Count : {members_count}",category=category)
            await channel.set_permissions(ctx.guild.default_role,connect=False)
            edit("member_counter","channel_id",int(channel.id))
    
        elif mode=="off":
            edit("member_counter","enabled?",False)
            try:
                channel = self.bot.get_channel(whatis("member_counter")["channel_id"])
                await channel.delete()
            except:pass
            edit("member_counter","channel_id",0)
        else:
            return await ctx.send("Invalid mode, please type either `on` or `off`.")
        embed = embeded()
        embed.description = f"Member counter is __{mode}__."
        await ctx.send(embed=embed)

def setup(bot:commands.Bot):
    bot.add_cog(Settings(bot))
        