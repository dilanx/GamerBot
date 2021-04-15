import datetime
import json
import urllib

import discord

from message_groups import message_set
import utility


def get_stats(message):
    
    utility.connect_mysql()
    
    username = None
    uuid = None
    
    if " for " in message.content:
        
        name = message.content.partition(" for ")[2]
        
        results = get_uuid(name)
        
        if results is None:
            
            return [None, "i couldn't find a minecraft player with that name :("]
        
        uuid = results[0]
        username = results[1]
        
        result = utility.run_sql("select color from discord_mc where minecraft = '" + uuid + "'")
        
        if not result:

            return [None, "uh oh, i couldn't retrieve the data :("]
        
        result = result.fetchall()
        
        if len(result) == 0:
            
            result = [0x000000]
            
        else: result = result[0]
        
    else:
        
        result = utility.run_sql("select color, minecraft from discord_mc where discord = '" + str(message.author.id) + "'")
        
        if not result:
            
            return [None, "uh oh, i couldn't retrieve the data :("]
        
        result = result.fetchall()
        
        if len(result) == 0:
            
            return [None, "hmm i don't know your minecraft username (you'll have to get dilan to set it manually for now)! instead, you could provide your username in the message you send me."]
        
        result = result[0]
        
        uuid = result[1]
        username = get_username(uuid)
    
        if username is None:
            username = "NULL USERNAME"
        
    
    data = utility.run_sql("select * from wb_stats where uuid = '" + uuid + "'").fetchone()
    
    embed = discord.Embed(title=username.replace("_", "\\_"), color=result[0])
    embed.set_thumbnail(url="https://crafatar.com/avatars/" + uuid)
    embed.set_footer(text="Wed Bars Statistics")
    
    if data is not None:
        
        embed.add_field(name="Wins", value=str(data[1]))
        embed.add_field(name="Losses", value=str(data[2]))
        embed.add_field(name="WLR", value="**"+str(round(data[1] / data[2] if data[2] > 0 else data[1], 2))+"**")
        embed.add_field(name="Kills", value=str(data[3]))
        embed.add_field(name="Deaths", value=str(data[4]))
        embed.add_field(name="KDR", value="**"+str(round(data[3] / data[4] if data[4] > 0 else data[3], 2))+"**")
        embed.add_field(name="Final Kills", value=str(data[5]))
        embed.add_field(name="Final Deaths", value=str(data[6]))
        embed.add_field(name="FKDR", value="**"+str(round(data[5] / data[6] if data[6] > 0 else data[5], 2))+"**")
        embed.add_field(name="Beds Broken", value=str(data[7]))
        embed.add_field(name="Beds Lost", value=str(data[8]))
        embed.add_field(name="BBBLR", value="**"+str(round(data[7] / data[8] if data[8] > 0 else data[7], 2))+"**")
        embed.add_field(name="Deaths by Maids", value="unavailable") #str(data[9])
        embed.add_field(name="Blocks Placed", value=str(data[10]))
        embed.add_field(name="Win Streak", value="unavailable") #str(data[11])
        
    else:
        
        embed.add_field(name="Invalid Wed Bars Player", value="This player doesn't have any stats yet.")
    
    return [embed, utility.r_msg(["here's the stats card :)",
                                  "i think i got it!",
                                  "here's what i found!",
                                  "i got the stats card!"])]
    
def get_username(uuid):
    
    try:
        with urllib.request.urlopen("https://api.mojang.com/user/profiles/" + uuid + "/names") as url:
            data = json.loads(url.read().decode())
            
        if len(data) < 0:
            return None
        
        obj = data[len(data) - 1]
        
        return obj["name"]
    except:
        return None
    
def get_uuid(username):
    
    try:
        with urllib.request.urlopen("https://api.mojang.com/users/profiles/minecraft/" + username) as url:
            data = json.loads(url.read().decode())
        
        return [data["id"], data["name"]]
    except:
        return None
    
    
msg_set = [
    message_set(get_stats,
                ["my wed bars stats",
                 "wed bars stats for "],
                [""])
    ]