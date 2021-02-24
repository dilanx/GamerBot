import discord
import sys
import os
from message_groups import message_set, profile_set
from utility import get_ping_id
from dotenv import load_dotenv

VERSION = "1.1"

load_dotenv()
client = discord.Client()



name = "gamer bot"

sets = []
    
    #add_message_set(basics.init())
#    add_message_set(ignore.init())
class Basics:
    
    def __init__(self):
        
        self.set = [
            message_set(self.hello,
                    ["hello", "hi", "sup", "hey", "say hi to "],
                    ["hello %0. i am %1.",
                     "umm hi %0",
                     "what's up %0. %1 here.",
                     "what's going on %0, %1 here.",
                     "oh hello there %0"]),
    
            message_set(self.tell_other,
                    ["tell "],
                    ["%0, here's a new message from %1: %2"]),
    
            message_set(self.change_name,
                     ["call you "],
                     ["ok you can call me %0 now",
                      "lmao alright you can call me %0 now"]),
            
            message_set(self.i_love_you,
                        ["i love you", "ily", "uwu"],
                        [":)"])]
        
    def get_msgs(self):
        return self.set
        
    def hello(self, message):
        
        to = message.author.display_name
        if "say hi to " in message.content:
            to = message.content.partition("say hi to ")[2]
        return [to, name]

    def change_name(self, message):
        
        new_name = message.content.partition("you ")[2]
        
        global name
        
        name = new_name
        
        return [name]
    
    def tell_other(self, message):
        
        split = message.content.partition(":")
        
        person = split[0].partition("tell ")[2]
        
        return [person, message.author.display_name, split[2]]
    
    def i_love_you(self, message):
        
        s = " " + message.content + " "
        
        if " ily " not in s and " i love you " not in s and " uwu " not in s:
            return None
        
        return [message.author.display_name]

class Ignore:
    
    def __init__(self):
        
        self.ignore = []
        self._load()
        
        self.set = [
            message_set(self.who_are_you_ignoring,
                    ["who are you ignoring"],
                    ["i'm ignoring these ppl rn: %0",
                     "i don't want to listen to these ppl: %0"]),
    
            message_set(self.ignore_start,
                    ["forever ignore "],
                    ["i'm now ignoring %0"]),
    
            message_set(self.ignore_end,
                    ["stop ignoring "],
                    ["if i was ignoring %0 before, i'm not anymore"])]
        
    def get_msgs(self):
        return self.set
        

    def who_are_you_ignoring(self, message):
        
        if (len(self.ignore) == 0): return [None, "i'm not ignoring anyone atm"]
        
        l = "<@" + self.ignore[0] + ">"
        
        for i in range(1, len(self.ignore)):
            
            l += ", <@" + self.ignore[i] + ">"
        
        return [l]
            
    
        
    def ignore_start(self, message):
        
        person = get_ping_id(message.content)
    
        if person is None:
            return [None, "idk who you want me to ignore :("]
        
        if (person == "203483343281455104"):
            return [None, "no i don't wanna ignore Dilan"]
        
        self.add_ignore(person)
        
        return ["<@" + person + ">"]
    
    def ignore_end(self, message):
            
        person = get_ping_id(message.content)
        
        if person is None:
            return [None, "idk who you want me to stop ignoring :("]
        
        if (person == "203483343281455104"):
            return [None, "i'd never ignore Dilan in the first place"]
        
        self.del_ignore(person)
        
        return ["<@" + person + ">"]
        
        
    
    def is_ignored(self, id):
        return id in self.ignore
    
    def add_ignore(self, id):
        self.ignore.append(id)
        self._save()
        
    def del_ignore(self, id):
        if id in self.ignore:
            self.ignore.remove(id)
            self._save()
            
    def _save(self):
        with open("data/ignore.txt", "w") as writer:
            for l in self.data:
                writer.write(l + "\n")
            
    def _load(self):
        with open("data/ignore.txt", "r") as reader:
            self.ignore = reader.readlines()
        
        for i in range(len(self.ignore)):
            
            self.ignore[i] = self.ignore[i].replace("\n", "")
    

class Remember:
    
    def __init__(self):
        
        self._data = {}
        self._load()
        
        self.set = [
            message_set(self.all_remember,
                        ["who all do you remember", "who do you remember", "who all do you know"],
                        ["here are the names of everyone i remember: %0 i'd love to meet more people (just tell me to remember your name)!",
                         "i remember these people: %0 i'd love to meet more people though (just tell me to remember your name)!",
                         "here are all the people i know: %0 i'd love to meet more people (just tell me to remember your name)!"]),
            message_set(self.new,
                        ["remember my name is ", "remember that my name is "],
                        ["okay %0! i'll remember you.",
                         "nice to meet you %0! i'll remember you now."]),
            message_set(self.pronouns,
                        ["remember my pronouns are ", "remember that my pronouns are "],
                        ["thanks! i know how to refer to you now.",
                         "okay got it."]),
            message_set(self.talk_about_all,
                        ["tell me about everyone"],
                        ["%0"]),
            message_set(self.talk_about_me,
                        ["tell me about myself"],
                        ["ofc! here's what i know about you, %0: %1"]),
            message_set(self.talk_about_me,
                        ["do you remember me"],
                        ["ofc i do! here's what i know about you, %0: %1",
                         "how could i forget! here's what i know about you, %0: %1"]),
            message_set(self.talk_about_other,
                        ["tell me about "],
                        ["ooh okay. here's what i know about %0: %1",
                         "oh I remember %2! here's what i know about %0: %1",
                         "how could i forget about %0! here's what i know about %2: %1"]),
            message_set(self.remember,
                        ["remember ", "remember that "],
                        ["okay %0, i'll remember that now.",
                         "cool! i'll remember that.",
                         "okay. i won't forget"]),
            message_set(self.what_is_my,
                        ["what is my ", "what are my "],
                        ["oh i know! %0",
                         "here's what i know: %0"]),
            message_set(self.what_do_i,
                        ["what do i "],
                        ["oh i know! %0",
                         "here's what i know: %0"]),
            message_set(self.what_is_other,
                        ["what is ", "what are "],
                        ["ooh i know this about %0: %1",
                         "%0 told me this earlier: %1",
                         "this is what i know about %0: %1"]),
            message_set(self.what_does_other,
                        ["what does "],
                        ["ooh i know this about %0: %1",
                         "%0 told me this earlier: %1",
                         "this is what i know about %0: %1"]),
            ]
        
    def _load(self):
        
        _, _, files = next(os.walk("data/profiles"))
        
        for f in files:
            
            if not f.endswith(".txt"): continue
            
            number = f[0:len(f) - 4]
            
            with open("data/profiles/" + f, "r") as reader:
                
                lines = reader.readlines()
                
            name = lines[0].replace("\n", "")
            
            pronouns = eval(lines[1].replace("\n", ""))
            
            prof = profile_set(name, number, pronouns)
            
            for i in range(2, len(lines)):
                prof.load_data(lines[i])
                
            self._data[number] = prof
            
    
            
    def get_msgs(self):
        return self.set
    
    def new(self, message):
        
        if str(message.author.id) in self._data:
            
            name = self._data[str(message.author.id)].get_name()
            
            return [None, "i already remember you as " + name]
        
        name = message.content.partition("my name is ")[2].strip()
        
        if " " in name: name = name.split(" ")[0]
        
        
        ps = profile_set(name, str(message.author.id), ["they", "them", "their", "are"])
        ps.save()
        self._data[str(message.author.id)] = ps 
        
        return [name]
    
    def pronouns(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "oh no i don't know your name. you'll have to let me remember that before i can remember other stuff about you."]
        
        msg = message.content.partition("my pronouns are ")[2].strip()
        
        if " " in msg: msg = msg.split(" ")[0]
        
        ans = self._data[str(message.author.id)].set_pronouns(msg)
        
        if not ans:
            return [None, "sorry, but i don't know what you mean. your pronouns need to be typed like subject/object/possession. for example: they/them/their, she/her/her, he/him/his"]
        
        return [""]
        
    def remember(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "oh no i don't know your name. you'll have to let me remember that before i can remember other stuff about you."]
            
        msg = message.content.partition("remember ")[2]
        
        if msg.startswith("that"): msg = msg.partition("that")[2].strip()
        
        msg = msg.replace(".", "").replace("!", "")
            
        ans = self._data[str(message.author.id)].add_new_data(msg)
        
        if not ans:
            
            return [None, "hmm i already know that."]
        
        return [self._data[str(message.author.id)].get_name()]
    
    
    def what_is_my(self, message):
        
        return self._what_i(message, " my ")
    
    def what_do_i(self, message):
        
        return self._what_i(message, " i ")
    
    def _what_i(self, message, split_type):
        
        if str(message.author.id) not in self._data:
            
            return [None, "i'm afraid that i don't know who you are. you'll have to let me remember your name first."]
        
        st = message.content.partition(split_type)[2]
        if (st.strip() == "name"): return ["your name is " + self._data[str(message.author.id)].get_name()]
        else: info = self._data[str(message.author.id)].find(message.content.partition(split_type)[2], True)
        
        if info is None:
            
            return [None, "i don't know :( but you should tell me."]
        
        return [info]
    
    def what_is_other(self, message):
        
        if "what is " in message.content:
            ind = "what is "
        else:
            ind = "what are "
            
        first_part = message.content.split(ind)[1]
        if "'s " not in message.content: return None
        who = first_part.split("'s ")[0]
        msg = first_part.split("'s ")[1].replace("?", "")
        
        return self._what_other(who, msg)

    def what_does_other(self, message):
        
        first_part = message.content.split("what does ")[1]
        if " " not in message.content: return None
        who = first_part.split(" ")[0]
        msg = first_part.split(" ")[1].replace("?", "")
        
        return self._what_other(who, msg)
        
    def _what_other(self, who, msg):
        
        for d in self._data.values():
            
            if d.get_name() == who:
                
                ans = d.find(msg, False)
                if ans is None:
                    return [None, "i know " + d.get_name() + " but i don't know " + d.get_pronouns()[2] + " " + msg + " :("]
                
                return [d.get_name(), ans]
                
        return [None, "i don't know who you're talking about :("]
    
    def talk_about_me(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "aww i don't remember you, sorry! i'd love to hear about you though :)"]
        
        info = self._data[str(message.author.id)]
        lines = info.get_all_format(True)
        
        if lines is None:
            
            return [None, "i remember you but i don't know much about you."]
        
        st = lines[0]
        
        for i in range(1, len(lines)):
            
            if i == len(lines) - 1:
                
                st += ", and " + lines[i] + "."
            
            else:
                
                st += ", " + lines[i]
        
        return [info.get_name(), st]
    
    def talk_about_other(self, message):
        
        who = message.content.split("tell me about ")[1]
        
        for d in self._data.values():
            
            if d.get_name() == who:
                
                lines = d.get_all_format(False)
                
                if lines is None:
                    
                    return [None, "i know " + d.get_name() + " but i don't know anything about " + d.get_pronouns()[1] + " :("]
                
                st = lines[0]
                
                for i in range(1, len(lines)):
                    
                    if i == len(lines) - 1:
                        
                        st += ", and " + lines[i] + "."
                    
                    else:
                        
                        st += ", " + lines[i]
                
                return [d.get_name(), st, d.get_pronouns()[1]]
                
        return [None, "i don't know who you're talking about :("]
    
    def talk_about_all(self, message):
        
        st = "here's everyone ik:"
        
        nws = []
        
        for d in self._data.values():
            
            lines = d.get_all_format(False)
            
            if lines is None:
                
                nws.append(d.get_name())
                continue
            
            st2 = lines[0]
                
            for i in range(1, len(lines)):
                
                if i == len(lines) - 1:
                    
                    st2 += ", and " + lines[i] + "."
                
                else:
                    
                    st2 += ", " + lines[i]
                    
            pron = d.get_pronouns()
            st += "\n\n**" + d.get_name() + "** *" + "(" + pron[0] + "/" + pron[1] + "/" + pron[2] + ")*\n" + st2
            
        if (len(nws) > 0):
            
            st3 = nws[0]
            
            if len(nws) == 2:
                st3 += " and " + nws[1]
            else:
                for i in range(2, len(nws)):
                    
                    if i == len(nws) - 1:
                        st3 += ", and " + nws[i]
                    else:
                        st3 += ", " + nws[i]
                
        st += "\n\ni also know " + st3 + " but i don't really know anything about them."
        
        return [st]
            
    
    def all_remember(self, message):
        
        if len(self._data.values()) == 0:
            return [None, "i don't know anyone :'("]
        
        val = list(self._data.values())
        
        st = val[0].get_name()
        
        for i in range(1, len(val)):
            
            if i == len(val) - 1:
                
                st += ", and " + val[i].get_name() + "."
                
            else:
                
                st += ", " + val[i].get_name()
                
        return [st]

def add_message_set(init):
    
    for i in init:
        sets.append(i)

basics = Basics()
ignore = Ignore()
remember = Remember()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if ignore.is_ignored(str(message.author.id)): return
    
    message.content = message.content.lower()
    
    if name in message.content:
        
        if str(message.author) == "Blockhead7360#5000":
            
            if message.content.startswith(name + " /"):
                
                cmd = message.content.partition(name + " /")[2]
                
                if cmd == "version":
                    await message.channel.send(VERSION)
                    return
                    
                if cmd == "stop":
                    await message.channel.send("already? well i guess i'll see you another time o7. shutting down now.")
                    sys.exit(0)
                    return
                
                if cmd.startswith("forceregister"):
                    await message.channel.send("you'll have to do it in the files atm :(")
                    return
        
        for s in sets:
            
            if s.should_activate(message.content):
                val = s.call_function(message)
                if val is not None:
                    
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
    

add_message_set(ignore.get_msgs())
add_message_set(remember.get_msgs())
add_message_set(basics.get_msgs())         

# lmao no i'm not letting the bot token appear on github
client.run(os.getenv("DISCORD-TOKEN"))


