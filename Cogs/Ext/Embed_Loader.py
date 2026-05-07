from diskord import Embed
import diskord
from Cogs.Ext.General_Functions import err, whatis,edit

empty = [None,""]

def hex_converter(hex_code):
    if "#" in hex_code:
        color = hex_code.replace("#", "")
        col = diskord.Color(value=int(color, 16))
        return col
    else:
        return None

def embeded():
    embed = Embed()
    COLOR = whatis("color_hex_code")
    if not COLOR in empty:
        COLOR = hex_converter(COLOR)
    TITLE = whatis("embed_title")
    THUMBNAIL = whatis("thumbnail_logo_url")
    IMAGE = whatis("image_url")
    FOOTER_TEXT = whatis("embed_footer_text")
    FOOTER_ICON = whatis("embed_footer_url")
    if TITLE in empty:
        TITLE = "Neon Discord Bot"
    if COLOR in empty:
        COLOR = diskord.Color.dark_magenta()
    if FOOTER_TEXT in empty:
        FOOTER_TEXT = "Neon Development"
    if FOOTER_ICON in empty:
        FOOTER_ICON = diskord.embeds.EmptyEmbed
    
    if not THUMBNAIL in empty and not IMAGE in empty:
        embed.set_thumbnail(url=THUMBNAIL)
        embed.set_image(url=IMAGE)
    embed.set_footer(text=FOOTER_TEXT,icon_url=FOOTER_ICON)
    embed.title = title=TITLE
    embed.colour = COLOR

    return embed


def load_message_payload(message,*,context=None,member=None):
    if isinstance(context,diskord.ext.commands.Context):
        message = message.replace("{user_mention}",f"<@{context.author.id}>")
        message = message.replace("{user_name}",f"{context.author.name}")
        message = message.replace("{server}",f"{context.guild.name}")
    elif isinstance(context,diskord.Interaction):
        message = message.replace("{user_mention}",f"<@{context.user.id}>")
        message = message.replace("{user_name}",f"{context.user.name}")
        message = message.replace("{server}",f"{context.guild.name}")
    elif context is None:
        if member is None:
            return False
        message = message.replace("{user_mention}",f"<@{member.id}>")
        message = message.replace("{user_name}",f"{member.name}")
        message = message.replace("{server}",f"{member.guild.name}")
    return message

async def send_with_ping(channel:diskord.TextChannel,*,content=None,embed=None):
    ghost_ping = whatis("ghost_ping")
    pingevery = whatis("ping_everyone")
    pinghere = whatis("ping_here")
    if pingevery is None or pinghere is None:
        return await channel.send(embed=embed)
    msg = ""    
    if pingevery == True:
        if pinghere == True:
            msg = "||@everyone|| ||@here||"
        else:
            msg = "||@everyone||"
    elif pinghere == True:
        if pingevery == True:
            msg = "||@everyone|| ||@here||"
        else:
            msg = "||@here||"

    if ghost_ping == True:
        if embed:
            await channel.send(embed=embed)
            msged = await channel.send(msg)
            await msged.delete()
        else:
            await channel.send(content)
            msged = await channel.send(msg)
            await msg.delete()
    else:
        if embed:
            await channel.send(msg,embed=embed)
        else:
            await channel.send(content+msg)
    

        
        
