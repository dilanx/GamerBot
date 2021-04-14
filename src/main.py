from datetime import datetime
import time

import discord

import utility

utility.load_keys()
utility.connect_mysql()

from message_groups import spd

from sets import learn, remember, interactions, \
    mathematics, northwestern, definitions, stonks, music, \
    chemistry, weather, wbstats

VERSION = "1.12 (more cracked at this game than ever before)"
dev = False

client = discord.Client()

key_discordtoken = utility.keys["DISCORD-TOKEN"]

link_help = "http://docs.blockhead7360.com/GamerBot"

sets = []

def add_message_set(init):
    
    for i in init:
        sets.append(i)

whitelist = ["Blockhead7360#1000"]

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    message.content = message.content.lower()
    
    if message.content.startswith("s!wb "):
        message.content = message.content.replace("s!wb ", "gamer bot wed bars stats for ")
    elif message.content.startswith("s!wb"):
        message.content = message.content.replace("s!wb", "gamer bot my wed bars stats")
        
    
    if "gamer bot" in message.content:
        
        if dev:
            
            if str(message.author) not in whitelist:
                await message.channel.send("aww sorry i can't respond rn. i'm in developer mode. dilan is updating me :)")
                return
            
        history(message)
            
        if message.content.startswith("gamer bot /"):
            
            cmd = message.content.partition("gamer bot /")[2]
            
            if cmd == "version":
                await message.channel.send(VERSION)
                return
                
            if cmd.startswith("spd "):
                
                if str(message.author) in whitelist:
                    
                    split = cmd.partition("spd ")[2].split(" ")
                    
                    if len(split) != 2:
                        await message.channel.send("fail.")
                        return
                    
                    spd.add_to_map(split[0], split[1])
                    
                    await message.channel.send("updated subject pronoun dictionary: " + split[0] + " -> " + split[1])
                    return
                
                else:
                    await message.channel.send("you aren't whitelisted to use /spd.")
                    return
            
            if cmd.startswith("sql "):
                
                if str(message.author) in whitelist:
                    
                    response = utility.run_sql(cmd.partition("sql ")[2])
                    
                    if not response:
                        await message.channel.send("aww i couldn't send that query :(")
                        return
                    
                    await message.channel.send("i sent your query to the server (" + utility.keys["SQL-HOST"] + "/" + utility.keys["SQL-DB"] + ")"
                                                + " and got the following response:\n" + str(response.fetchall()))
                    return
                
                else:
                    await message.channel.send("sorry! i'm not allowed to let you send queries.")
                    return
                
        
        for ls in learn.learn_sets.keys():
        
            if ls in message.content:
            
                message.content = message.content.replace(ls, learn.learn_sets[ls])
        
        for s in sets:
            
            if s.should_activate(message.content):
                val = s.call_function(message)
                
                if val is None: continue
                
                else:
                    
                    if val[0] is None:
                        
                        msg = val[1]
                    
                    elif (type(val[0]) is discord.Embed):
                        
                        if len(val) == 2:
                            await message.channel.send(val[1])
                            
                        await message.channel.send(embed=val[0])
                        return
                    
                    else:
                        
                        msg = s.random_message()
                    
                    if "@everyone" in msg or "@here" in msg:
                        await message.channel.send("don't force gamer bot to ping everyone :(")
                    elif len(msg) > 2000:
                        await message.channel.send("umm discord won't let me send something this long :(")
                    else:
                        await message.channel.send(msg)

                return
    
    # easter egg lmao
    if "s!bw " in message.content or "s!bedwars " in message.content:
        if message.author.id == 396422982857392139 and message.channel.id == 710353578971365399:
            time.sleep(3)
            await message.channel.send(utility.r_msg(["claire you're addicted to bed wars.",
                                                      "dude so much bed wars claire lmaoo.",
                                                      "ahh so addicted to bed wars claire.",
                                                      "claireee so much bed warsss.",
                                                      "ahh yes the traditional claire bed wars addiction.",
                                                      "haha claire go vroom in bed wars.",
                                                      "i see you checking bed wars stats, claire.",
                                                      "just a girlboss doing girlboss things."]))
                
@client.event
async def on_ready():
    listening = discord.Activity(type=discord.ActivityType.listening, name="gamer music")
    await client.change_presence(activity=listening)
    
    interactions.awake_time = datetime.now()
    
def history(message):
    
    with open("data/history/" + str(message.author.id) + ".txt", "a") as writer:
            writer.write("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
                         + "] [" + str(message.channel.id) + "] " + message.content + "\n")

add_message_set(learn.msg_set)
add_message_set(music.msg_set)
add_message_set(wbstats.msg_set)
add_message_set(definitions.msg_set)
add_message_set(northwestern.msg_set)
add_message_set(stonks.msg_set)
add_message_set(weather.msg_set)
add_message_set(chemistry.msg_set)
add_message_set(remember.msg_set)
add_message_set(mathematics.msg_set)
add_message_set(interactions.msg_set)
add_message_set(remember.msg_set_LOW)
learn.main_sets = sets

client.run(key_discordtoken)


