from datetime import datetime
import time

import discord
from discord.ext import tasks

from message_groups import spd
from sets import learn, remember, interactions, \
    mathematics, northwestern, definitions, stonks, music, \
    chemistry, weather, wbstats, reminder, cringe, voice
import utility


VERSION = "1.13 (being cracked is an understatement)"
dev = False

client = discord.Client()

key_discordtoken = utility.keys["DISCORD-TOKEN"]

link_help = "http://docs.blockhead7360.com/GamerBot"

sets = []

## Message set function return guide
# None - exit out of current message set and continue searching
# [None, <msg>] - force send message rather than any message set strings
# [<embed>, <optional-msg>] - send the discord embed, optionally with a message


def add_message_set(init):

    for i in init:
        sets.append(i)

whitelist = [203483343281455104]

del_msgs = ["lmaoo looks like dilan just deleted something: %0",
            "welp looks like dilan deleted something: %0",
            "dilan just deleted: %0",
            "look at what dilan deleted: %0"]

@client.event
async def on_message_delete(message):
    if message.author.id == 203483343281455104 and message.guild.id == 706345833750069260:
        await message.channel.send(utility.r_msg(del_msgs).replace("%0", message.content))

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

            if message.author.id not in whitelist:
                await message.channel.send("aww sorry i can't respond rn. i'm in developer mode. dilan is updating me :)")
                return

        history(message)

        if message.content.startswith("gamer bot /"):

            cmd = message.content.partition("gamer bot /")[2]

            if cmd == "version":
                await message.channel.send(VERSION)
                return

            if cmd.startswith("acl "):

                if message.author.id in whitelist:

                    sp = cmd.partition("acl ")[2].split(" ")

                    if len(sp) != 1:
                        await message.channel.send("fail.")
                        return

                    try:

                        await client.get_channel(int(sp[0])).send(utility.changelog_msg)

                    except:
                        await message.channel.send("fail.")

                    return

                else:
                    await message.channel.send("you aren't whitelisted to use /acl.")
                    return

            if cmd.startswith("spd "):

                if message.author.id in whitelist:

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

                if message.author.id in whitelist:

                    utility.connect_mysql()

                    response = utility.run_sql(cmd.partition("sql ")[2])

                    if not response:
                        await message.channel.send("aww i couldn't send that query :(")
                        return

                    response = response.fetchall()

                    if (len(response) == 0): response = "success"
                    else: response = str(response)

                    await message.channel.send("i sent your query to the server (" + utility.keys["SQL-HOST"] + ")"
                                                + " and got the following response:\n" + response)
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

                    if utility.planned_joinvc:
                        utility.planned_joinvc = False
                        channel = message.author.voice.channel
                        utility.voice_channel = await channel.connect()

                    if utility.planned_leavevc:
                        utility.planned_leavevc = False
                        await utility.voice_channel.disconnect()
                        utility.voice_channel = None


                return

    # easter egg lmao
    if "s!bw " in message.content or "s!bedwars " in message.content:
        if message.author.id == 396422982857392139:
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

    remind.start()

def history(message):

    with open("data/history/" + str(message.author.id) + ".txt", "a") as writer:
            writer.write("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
                         + "] [" + str(message.channel.id) + "] " + message.content + "\n")

@tasks.loop(seconds=10.0)
async def remind():

    cur_time = datetime.now().timestamp()

    to_remove = []

    need_to_save = False

    for reminder_time in reminder.reminders:

        if float(reminder_time) < cur_time:

            r = reminder.reminders[reminder_time]

            await client.get_channel(r.channel).send(utility.r_msg(reminder.reminder_msgs)
                                                     .replace("%0", "<@" + str(r.sender) + ">").replace("%1", r.message))

            to_remove.append(reminder_time)
            need_to_save = True

    for r in to_remove:

        del reminder.reminders[r]

    if need_to_save:
        reminder.save()




add_message_set(learn.msg_set)
# add_message_set(cringe.msg_set)
add_message_set(music.msg_set)
add_message_set(wbstats.msg_set)
add_message_set(reminder.msg_set)
add_message_set(definitions.msg_set)
add_message_set(northwestern.msg_set)
add_message_set(stonks.msg_set)
add_message_set(weather.msg_set)
add_message_set(chemistry.msg_set)
add_message_set(remember.msg_set)
add_message_set(mathematics.msg_set)
add_message_set(interactions.msg_set)
add_message_set(voice.msg_set)
add_message_set(remember.msg_set_LOW)

learn.main_sets = sets
utility.client = client

client.run(key_discordtoken)
