import json,datetime,os,sys
from colorama import Fore,init

LogsPath = "Data\\Logs"

def restart():
    os.execv(sys.executable,['python']+sys.argv)

def whatis(object,path=None):
    if path is None:
        path = "Data\\configuration.json"
    elif path==2:
        path = "Data\\Reaction_Roles.json"
    elif path==3:
        path = "Data\\Guild.json"
    elif path==4:
        path = "Data\\Changelogs.json"
    elif path==5:
        path = "Data\\Statuses.json"
    
    
    with open(path,"r+") as f:
        cnfg = json.load(f)
        f.close()
    try:
        if not cnfg[object]=="" or cnfg[object]==0 or cnfg[object]==[] or cnfg[object]=={}:
            try:
                return cnfg[object]
            except KeyError:
                return None
        else:
            return None
    except KeyError:
        return None


def edit(object,value=None,*,alt_value=None,path=None,mode=None):
    """
    Paths :
    -------

        1 -) Configuration\n
        2 -) Reaction Roles\n
        3 -) Guild\n
        4 -) Changelogs\n
        5 -) Statuses\n

        If the path is not one of those integers, fill with a `path`.
    """
    if path is None or path == 1:
        path = "Data\\configuration.json"
    elif path==2:
        path = "Data\\Reaction_Roles.json"
    elif path==3:
        path = "Data\\Guild.json"
    elif path==4:
        path = "Data\\Changelogs.json"
    elif path==5:
        path = "Data\\Statuses.json"
    
    with open(path,"r+") as f:
        config = json.load(f)
        f.close()
    # List editting
    if isinstance(config[object],list):
        if alt_value:
            if mode=="add" or mode is None:
                config[object][value].append(alt_value)
            else:
                try:
                    config[object][value].remove(alt_value)
                except ValueError:
                    return False
        else:
            if mode=="add" or mode is None:
                config[object].append(value)
            else:
                try:
                    config[object].remove(value)
                except ValueError:
                    return False
    #Dictionary editting
    elif isinstance(config[object],dict):
        if mode=="add" or mode is None:
            if alt_value is not None:
                if isinstance(config[object][value],list):
                    config[object][value].append(alt_value)
                else:
                    config[object][value] = alt_value
            else:
                config[object] = value
        elif mode=="rem" or mode=="remove":
            if alt_value is not None:
                del config[object][value]
            else:
                try:
                    del config[object]
                except:
                    return False
    # String (casual) editting
    else:
        if mode=="add" or mode is None:
            config[object] = value
        else:
            try:
                del config[object]
            except:
                return False
    

    with open(path,"w") as f:
        json.dump(config,f,indent=4,sort_keys=False)
        f.close()

    return True


def set_role_system(msg_id,message_payload):
    with open("Data\\Reaction_Roles.json","r+") as f:
        config = json.load(f)
        f.close()
    config[str(msg_id)] = message_payload
    with open("Data\\Reaction_Roles.json","w") as f:
        json.dump(config,f,indent=4,sort_keys=False)
        f.close()



def log(data):
    if whatis("logging") == False:
        return
    now = datetime.datetime.now()
    time = now.strftime("[%H:%M:%S] ")
    init(convert=True)
    msg = f"{Fore.GREEN}[LOG]{Fore.RESET} "+data
    print(Fore.LIGHTBLACK_EX+time+Fore.RESET+str(msg))
    today = datetime.date.today()
    d1 = today.strftime("%d.%m.%Y")
    if f"{d1}-Log.txt" in os.listdir(LogsPath):
        FilePath=f"Data\\Logs\\{d1}-Log.txt"
        f = open(FilePath,"a+")
    else:
        FilePath = f"Data\\Logs\\{d1}-Log.txt"
        f = open(FilePath,"x")
        f.close()
        f = open(FilePath,"w")
    f.write(f"{time}{str(data)}\n")
    f.close()

def err(error:str):
    if whatis("logging") == False:
        return
    now = datetime.datetime.now()
    time = now.strftime("[%H:%M:%S] ")
    init(convert=True)
    msg = f"{Fore.RED}[ERROR]{Fore.RESET} {error}"
    print(Fore.LIGHTBLACK_EX+time+Fore.RESET+str(msg))

def setup_user_db(member):
    if os.path.exists(f"Data\\User Data\\{member.id}.json"):
        return
    if member.bot:
        user_dict = {"invites":[]}
    else:
        user_dict = {
            "bank":0,
            "cash":0,
            "messages":0,
            "level":{"current":0,"xp":0},
            "warnings":[],
            "invites":[]}
    with open(f"Data\\User Data\\{member.id}.json","w") as file:
        json.dump(user_dict,file,indent=4,sort_keys=False)
        file.close()
    
    
def count_commands(bot):
    count = 0
    for cmd in bot.walk_commands():
        count += 1
    return count

    
