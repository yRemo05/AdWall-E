from disocrd.ext import commands
from Cogs.Ext.Embed_Loader import embeded, send_with_ping
from Cogs.Ext.General_Functions import edit, whatis
import disocrd

empty = ["",None,0]


class Utility(commands.Cog,name=":hammer_pick:Utility"):
    def __init__(self,bot:commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def resetcl(self,ctx,*,name):
        embed = embeded()
        embed.description = f"Resetted the changelog database of the application : `{name}`"
        db_dict = {"added":[],"removed":[],"fixed":[],"improved":[],"todo":[]}
        edit(object=str(name),value=db_dict,path=4)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def basedelcl(self,ctx,*,app_name):
        embed = embeded()
        embed.description = f"Deleted an application from the database : `{app_name}`"
        edit(object=str(app_name),mode="remove")
        await ctx.send(embed=embed)

    @commands.command()
    async def createcl(self,ctx,*,name):
        embed = embeded()
        embed.description = f"Created a changelog database for application : `{name}`"
        db_dict = {"added":[],"removed":[],"fixed":[],"improved":[],"todo":[]}
        edit(object=str(name),value=db_dict,path=4)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def addcl(self,ctx,app_name,*,feature):
        embed = embeded()
        if whatis(str(app_name),4) is None:
            embed.description = f"Error occured while adding a feature to the changelog : :x: Cannot find an application named : `{app_name}`"
            return await ctx.send(embed=embed)
        edit(str(app_name),value="added",alt_value=feature,path=4)
        embed.description = f"A feature is added to the changelog of the application : `{app_name}` :white_check_mark:"
        embed.add_field(name="Added Feature :",value=f"{feature}",inline=False)
        return await ctx.send(embed=embed)
    
    @commands.command()
    async def fixcl(self,ctx,app_name,*,feature):
        embed = embeded()
        if whatis(str(app_name),4) is None:
            embed.description = f"Error occured while adding a fixed feature to the changelog : :x: Cannot find an application named : `{app_name}`"
            return await ctx.send(embed=embed)
        edit(str(app_name),value="fixed",alt_value=str(feature),path=4,mode="add")
        embed.description = f"A feature is added as fixed to the changelog of the application : `{app_name}` :white_check_mark:"
        embed.add_field(name="Fixed Feature :",value=f"{feature}",inline=False)
        return await ctx.send(embed=embed)
    
    @commands.command()
    async def improvecl(self,ctx,app_name,*,feature):
        embed = embeded()
        if whatis(str(app_name),4) is None:
            embed.description = f"Error occured while adding an improvement for a feature to the changelog : :x: Cannot find an application named : `{app_name}`"
            return await ctx.send(embed=embed)
        edit(str(app_name),value="improved",alt_value=str(feature),path=4,mode="add")
        embed.description = f"An improved feature is added to the changelog of the application : `{app_name}` :white_check_mark:"
        embed.add_field(name="Improved Feature :",value=f"{feature}",inline=False)
        return await ctx.send(embed=embed)
    
    @commands.command()
    async def todocl(self,ctx,app_name,*,feature):
        embed = embeded()
        if whatis(str(app_name),4) is None:
            embed.description = f"Error occured while extending the todo list : :x: Cannot find an application named : `{app_name}`"
            return await ctx.send(embed=embed)
        edit(str(app_name),value="todo",alt_value=str(feature),path=4,mode="add")
        embed.description = f"Todo list is extended for the changelog of the application : `{app_name}` :white_check_mark:"
        embed.add_field(name="Todo :",value=f"{feature}",inline=False)
        return await ctx.send(embed=embed)

    @commands.command()
    async def removecl(self,ctx,app_name,*,feature):
        embed = embeded()
        if whatis(str(app_name),4) is None:
            embed.description = f"Error occured while adding a feature to the changelog : :x: Cannot find an application named : `{app_name}`"
            return await ctx.send(embed=embed)
        edit(str(app_name),value="removed",alt_value=str(feature),path=4,mode="add")
        embed.description = f"A feature is removed from the changelog of the application : `{app_name}` :white_check_mark:"
        embed.add_field(name="Removed Feature :",value=f"{feature}",inline=False)
        return await ctx.send(embed=embed)
    
    @commands.command()
    async def delcl(self,ctx,app_name,*,feature):
        embed = embeded()
        app_changelog = whatis(str(app_name),4)
        if app_changelog in empty:
            embed.description = f"Error occured while removing a feature from the changelog : :x: Cannot find an application named : `{app_name}`"
            return await ctx.send(embed=embed)
        embed.description = f"Removed a feature from the changelog for the application : `{app_name}` :white_check_mark:"
        embed.add_field(name="Removed Feature :",value=f"{feature}",inline=False)
        for added in app_changelog["added"]:
            if str(feature).lower()==str(added).lower():
                edit(str(app_name),value="added",alt_value=str(feature),mode="remove",path=4)
                return await ctx.send(embed=embed)
        for fixed in app_changelog["fixed"]:
            if str(feature).lower()==str(fixed).lower():
                edit(str(app_name),value="fixed",alt_value=str(feature),mode="remove",path=4)
                return await ctx.send(embed=embed)
        for improved in app_changelog["improved"]:
            if str(feature).lower()==str(improved).lower():
                edit(str(app_name),value="improved",alt_value=str(feature),mode="remove",path=4)
                return await ctx.send(embed=embed)
        for todo in app_changelog["todo"]:
            if str(feature).lower()==str(todo).lower():
                edit(str(app_name),value="todo",alt_value=str(feature),mode="remove",path=4)
                return await ctx.send(embed=embed)
        return await ctx.send(f"Cannot find the feature in added,improved,fixed,removed and todo lists : `{feature}`")

            
    @commands.command()
    async def sendcl(self,ctx:commands.Context,app_name,channel:disocrd.TextChannel=None):
        if channel is None:
            channel = ctx.channel
        embed = embeded()
        added = []
        improved = []
        fixed = []
        todo = []
        removed = []
        appcl = whatis(str(app_name),4)
        if appcl in empty:
            embed.description = f"Error occured while sending the changelog : :x: Cannot find an application named : `{app_name}`"
            return await ctx.send(embed=embed)
        for add in appcl["added"]:
            added.append(f"[+] {add}\n")
        for imp in appcl["improved"]:
            improved.append(f"[!] {imp}\n")
        for fix in appcl["fixed"]:
            fixed.append(f"[=] {fix}\n")
        for todod in appcl["todo"]:
            todo.append(f"[?] {todod}")
        for removal in appcl["removed"]:
            removed.append(f"[-] {removal}\n")
        if len(added)>0:
            embed.add_field(name="ADDED :",value="".join(filter(None,added)),inline=False)
        if len(removed)>0:
            embed.add_field(name="REMOVED :",value="".join(filter(None,removed)),inline=False)
        if len(improved)>0:
            embed.add_field(name="IMPROVED :",value="".join(filter(None,improved)),inline=False)
        if len(fixed)>0:
            embed.add_field(name="FIXED :",value="".join(filter(None,fixed)),inline=False)
        if len(todo)>0:
            embed.add_field(name="TODO :",value="".join(filter(None,todo)),inline=False)
        def check(m):
            return m.author==ctx.author and m.channel==ctx.channel
        delmsg = await ctx.send("Enter a version for your application just. Example : `0.0.1`, `0.3`, `2.0`, `0.1 Beta`\n(Do not use 'version' word.)")
        msg = await self.bot.wait_for("message",check=check)
        msgcont = msg.content
        await msg.delete()
        await delmsg.delete()
        app_name = app_name.replace("_"," ")
        embed.description = f"{app_name} Version {msgcont}"
        await send_with_ping(channel,embed=embed)
    
    @commands.command()
    async def announce(self,ctx:commands.Context,channel:disocrd.TextChannel,*,message):
        embed = embeded()
        embed.description = str(message)
        if channel is None:
            channel = ctx.channel
        await send_with_ping(channel,embed=embed)
                
        
    
        
            






def setup(bot:commands.Bot):
    bot.add_cog(Utility(bot))