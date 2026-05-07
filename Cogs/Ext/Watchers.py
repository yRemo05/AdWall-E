import diskord
from Cogs.Ext.General_Functions import whatis


empty = [0,None,""]

async def create_ticket(bot,interaction:diskord.Interaction):
            ticket_category_id = whatis("ticket_category")
            ticket_category = bot.get_channel(ticket_category_id) if not ticket_category_id in empty else None
            if ticket_category is None:
                chan = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}")
            else:
                chan = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}",category=ticket_category)
            await chan.set_permissions(interaction.user,read_messages=True,send_messages=True)
            await chan.set_permissions(interaction.guild.default_role,read_messages=False,send_messages=False)
            for role_id in whatis("mod_perms"):
                role = diskord.utils.get(interaction.guild.roles,id=role_id)
                await chan.set_permissions(role,read_messages=True,send_messages=True)
            try:
                await interaction.response.send_message(content=f"Your ticket is ready : {chan.mention}")
            except:pass
            return chan