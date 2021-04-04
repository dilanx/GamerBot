from datetime import datetime

import discord
import utility

utility.load_keys()

from message_groups import spd
from sets import learn, remember, interactions, \
    mathematics, northwestern, definitions, stonks, music, \
    chemistry, weather



VERSION = "1.10 (absolutely cracked at this game)"
dev = False

client = discord.Client()

key_discordtoken = utility.keys["DISCORD-TOKEN"]

link_help = "http://docs.blockhead7360.com/GamerBot"

sets = []
    
    #add_message_set(basics.init())
#    add_message_set(ignore.init())

def add_message_set(init):
    
    for i in init:
        sets.append(i)

whitelist = ["Blockhead7360#1000"]

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    message.content = message.content.lower()
    
    if "gamer bot" in message.content:
        
        if dev:
            
            if str(message.author) not in whitelist:
                await message.channel.send("aww sorry i can't respond rn. i'm in developer mode.")
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
                    
                    else:
                        
                        msg = s.random_message()
                    
                    if "@everyone" in msg or "@here" in msg:
                        await message.channel.send("Don't force gamer bot to ping everyone :(")
                    else:
                        await message.channel.send(msg)

                return
                
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

# lmao no i'm not letting the bot token appear on github
client.run(key_discordtoken)


