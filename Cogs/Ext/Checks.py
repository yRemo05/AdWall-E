import diskord
from Cogs.Ext.General_Functions import whatis
from diskord.ext import commands


moderation_cogs = [":shield:Security",":hammer:Moderation"]
settings_cog = ":gear:Settings"
setting_forbid_cmds = ["changelogs","addcl","fixcl","removecl","delcl","improvecl","todocl","sendcl","createcl","settings"]

def is_dev(ctx):
    return ctx.author.id in whatis("Developer_IDs")

def have_any_mod_roles(ctx):
    if ctx.command.cog_name in moderation_cogs:
        for role_id in whatis("mod_perms"):
            for role in ctx.author.roles:
                if int(role_id)==int(role.id):
                    return True
        return False

def have_settings_perms(ctx):
    if ctx.command.cog_name == settings_cog or ctx.command.name in setting_forbid_cmds:
        for role_id in whatis("settings_perms"):
            for role in ctx.author.roles:
                if int(role_id)==int(role.id):
                    return True
        return False

def have_ticket_perms(ctx):
    for role_id in whatis("ticket_perms"):
        for role in ctx.author.roles:
            if int(role_id)==int(role.id):
                return True
    return False

def have_giveaway_perms(ctx):
    for role_id in whatis("giveaway_perms"):
        for role in ctx.author.roles:
            if int(role_id)==int(role.id):
                return True
    return False