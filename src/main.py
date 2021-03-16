import discord
import os
from message_groups import message_set, profile_set, spd
import utility
from dotenv import load_dotenv
import cexprtk
from bs4 import BeautifulSoup
import urllib
from datetime import datetime, timedelta
import json
import requests
import mendeleev

VERSION = "1.8 (extremely cracked)"
dev = False

load_dotenv()
client = discord.Client()

key_discordtoken = os.getenv("DISCORD-TOKEN")
key_merriamwebsterdictkey = os.getenv("MW-DICT-KEY")
key_merriamwebstertheskey = os.getenv("MW-THES-KEY")
key_polygonkey = os.getenv("POLYGON-KEY")
key_geniustoken = os.getenv("GENIUS-TOKEN")

link_help = "http://docs.blockhead7360.com/GamerBot"

name = "gamer bot"

sets = []

learn_sets = {}

awake_time = None
    
    #add_message_set(basics.init())
#    add_message_set(ignore.init())

class Learn:
    
    def __init__(self):
        
        self._load()
        self.set = [
            message_set(self.learn,
                        ["learn that & is like saying "],
                        ["ooh okay thanks for teaching me!",
                         "ahh okay i'll remember that.",
                         "okay got it now thanks!",
                         "ohh so that's what that means. thanks!"])
            
            ]
        
    def get_msgs(self):
        return self.set
    
    def learn(self, message):
        
        msg = message.content.partition("learn that ")[2]
        
        if msg.startswith("saying "):
            msg = msg.partition("saying ")[2]
            
        if " is like saying " in msg:
            msg = msg.split(" is like saying ")
                    
        understood = False
        
        for al in learn_sets.keys():
            
            if msg[1] == al:
                
                understood = True
        
        for s in sets:
            if s.should_activate(msg[1]):
                
                understood = True
                
        
        if not understood: return [None, "wait i don't know what \"" + msg[1] + "\" means"]
        
        learn_sets[msg[0]] = msg[1]
        self._save()
        
        return [""]
    
    def _load(self):
        
        with open("data/learn.txt", "r") as reader:
            learnmsgs = reader.readlines()
            
        for line in learnmsgs:
            
            both = line.split(" !LEARN_MSG! ")
            
            learn_sets[both[0]] = both[1]
        
    
    def _save(self):
            
        with open("data/learn.txt", "w") as writer:
            for line in learn_sets.keys():
                writer.write(line + " !LEARN_MSG! " + learn_sets[line] + "\n")
            

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
        
        person = utility.get_ping_id(message.content)
    
        if person is None:
            return [None, "idk who you want me to ignore :("]
        
        if (person == "203483343281455104"):
            return [None, "no i don't wanna ignore Dilan"]
        
        self.add_ignore(person)
        
        return ["<@" + person + ">"]
    
    def ignore_end(self, message):
            
        person = utility.get_ping_id(message.content)
        
        if person is None:
            return [None, "idk who you want me to stop ignoring :("]
        
        if (person == "203483343281455104"):
            return [None, "i'd never ignore Dilan in the first place"]
        
        self.del_ignore(person)
        
        return ["<@" + person + ">"]
        
        
    
    def is_ignored(self, user):
        return user in self.ignore
    
    def add_ignore(self, user):
        self.ignore.append(user)
        self._save()
        
    def del_ignore(self, user):
        if user in self.ignore:
            self.ignore.remove(user)
            self._save()
            
    def _save(self):
        with open("data/ignore.txt", "w") as writer:
            for l in self.ignore:
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
        
        self.set2 = [
            message_set(self.hello,
                    ["hello", "hi", "sup", "hey", "say hi to "],
                    ["umm hi %0",
                     "oh hello there %0",
                     "hi %0!!",
                     "hello %0!!",
                     "hey %0! how are you?",
                     "hi %0! how are you doing?",
                     "hello %0. how are you?"])
            
            ]
        
        self.set = [
            message_set(self.all_remember,
                        ["who all do you remember", "who do you remember", "who all do you know"],
                        ["here are the names of everyone i remember: %0 i'd love to meet more people (just tell me to remember your name)!",
                         "i remember these people: %0 i'd love to meet more people though (just tell me to remember your name)!",
                         "here are all the people i know: %0 i'd love to meet more people (just tell me to remember your name)!"]),
            message_set(self.new,
                        ["remember my name is ", "remember that my name is ", "my name is "],
                        ["okay %0! i'll remember you.",
                         "nice to meet you %0! i'll remember you now."]),
            message_set(self.pronouns,
                        ["remember my pronouns are ", "remember that my pronouns are ", "my pronouns are "],
                        ["thanks! i know how to refer to you now.",
                         "okay got it."]),
            message_set(self.talk_about_all,
                        ["tell me about everyone"],
                        ["%0"]),
            message_set(self.talk_about_me,
                        ["tell me about myself", "what do you know about me"],
                        ["ofc! here's what i know about you, %0: %1"]),
            message_set(self.talk_about_you,
                        ["tell me about yourself"],
                        ["there isn't really to say much about me, %0. i'm a discord bot lmaoo. i do like talking to you though :)",
                         "hmm tbh idrk. i'm a discord bot who likes talking to people, especially you %0 :)",
                         "i like talking to ppl, like you, %0, as well as giving them helpful information. other than that i'm just a little discord bot :)"]),
            message_set(self.talk_about_me,
                        ["do you remember me"],
                        ["ofc i do! here's what i know about you, %0: %1",
                         "how could i forget! here's what i know about you, %0: %1"]),
            message_set(self.forget_about_me,
                        ["forget everything about me"],
                        ["it was nice knowing you, %0! i'll forget everything about you as you requested",
                         "well, ig all friendships come to an end. goodbye %0 :'(",
                         "as you request, %0."]),
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
            message_set(self.forget,
                        ["forget ", "forget that "],
                        ["forget what :)",
                         "okay %0, i'll forget about that."]),
            message_set(self.what_is_my,
                        ["what is my ", "what are my ", "whats my ", "what's my ", "who am i"],
                        ["oh i know! %0",
                         "here's what i know: %0"]),
            message_set(self.what_do_i,
                        ["what do i "],
                        ["oh i know! %0",
                         "here's what i know: %0"]),
            message_set(self.what_is_other,
                        ["what is ", "what are ", "whats ", "what's "],
                        ["ooh i know this about %0: %1",
                         "%0 told me this earlier: %1",
                         "this is what i know about %0: %1"]),
            message_set(self.what_does_other,
                        ["what does "],
                        ["ooh i know this about %0: %1",
                         "%0 told me this earlier: %1",
                         "this is what i know about %0: %1"])
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
    
    def get_msgs2(self):
        return self.set2
    
    def get_profile(self, sender_id):
        
        if str(sender_id) not in self._data: return None
        else: return self._data[str(sender_id)]
    
    def hello(self, message):
        
        global name
        
        if str(message.author.id) not in self._data:
            
            return [None, "oh hello there! i'm " + name + "! i'm not sure who you are but you should tell me your name so i remember."]
        
        your_name = self._data[str(message.author.id)].get_name()
        
        return [your_name]
        
    
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
    
    def forget(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "oh no i don't know your name. you'll have to let me remember that before i can remember other stuff about you."]
            
        msg = message.content.partition("forget ")[2]
        
        if msg.startswith("that"): msg = msg.partition("that")[2].strip()
        
        msg = msg.replace(".", "").replace("!", "")
            
        ans = self._data[str(message.author.id)].del_data(msg)
        
        if not ans:
            
            return [None, "i can't forget something about you that i didn't know"]
        
        return [self._data[str(message.author.id)].get_name()]
    
    def what_is_my(self, message):
        
        return self._what_i(message, " my ")
    
    def what_do_i(self, message):
        
        return self._what_i(message, " i ")
    
    def _what_i(self, message, split_type):
        
        if str(message.author.id) not in self._data:
            
            return [None, "i'm afraid that i don't know who you are. you'll have to let me remember your name first."]
        
        if "who am i" in message.content.strip():
            return ["your name is " + self._data[str(message.author.id)].get_name()]
        
        st = message.content.partition(split_type)[2]
        if (st.strip() in ["name", "name?"]): return ["your name is " + self._data[str(message.author.id)].get_name()]
        else: info = self._data[str(message.author.id)].find(message.content.partition(split_type)[2], True)
        
        if info is None:
            
            return [None, "i don't know :( but you should tell me."]
        
        return [info]
    
    def what_is_other(self, message):
        
        content = message.content.replace("whats", "what is ").replace("what's", "what is ")
        
        if "what is " in content:
            ind = "what is "
            
            possible_math = mathematics.evaluate_math(content)
            
            if possible_math[0] is not None:
                return [None, "here's what i got: " + possible_math[0]]
            
        else:
            ind = "what are "
            
        first_part = content.split(ind)[1]
        if "'s " not in content: return None
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
        
        who = who.strip()
        
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
    
    def talk_about_you(self, message):
        
        
        if str(message.author.id) not in self._data:
            
            return [None, "you first! what's your name?"]
        
        your_name = self._data[str(message.author.id)].get_name()
        
        return [your_name]
    
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
    
    def forget_about_me(self, message):
        
        if str(message.author.id) not in self._data:
            
            return [None, "i can't forget about someone i don't know xD"]
        
        name = self._data[str(message.author.id)].get_name()

        self._data[str(message.author.id)].forget()
        
        del self._data[str(message.author.id)]
        
        return [name]

class Interactions:
    
    def __init__(self):
        
        self.set = [
            message_set(self.empty,
                        ["are you awake"],
                        ["yeah", "yeah i'm awake!",
                         "i am indeed awake", "yup",
                         "yes"]),
            message_set(self.awake,
                        ["how long have you been awake"],
                        ["i've been up for like %0.",
                         "it's been %0 since i woke up.",
                         "currently around %0.",
                         "%0 lol."]),
            message_set(self.empty,
                        ["tell me a joke"],
                        ["if only i was funny :(",
                         "aww i don't know any good ones."]),
            message_set(self.empty,
                        ["are you gay"],
                        ["no i like girl bots."]),
            message_set(self.empty,
                        ["do my & homework",
                         "do my & hw",
                         "what about my & hw",
                         "what about my & homework"],
                        ["code me to and i will.",
                         "i will if you program me to.",
                         "i would if i could.",
                         "wish i could but i can't, sorry!"]),
            message_set(self.empty,
                        ["love you", "proud of you", "youre the best", "you're the best",
                         "you're awesome", "youre awesome", "you're cute", "youre cute",
                         "like you"],
                        ["aww thank you :blush:",
                         "that means a lot :blush:",
                         "yay :blush:",
                         "how pog of you to say that :)"]),
            message_set(self.empty,
                        ["hate you", "screw you"],
                        ["wow. :pensive:",
                         "that isn't nice :pensive:",
                         "i'm trying my best :cry:"]),
            message_set(self.empty,
                        ["how are you made", "how were you made"],
                        ["check it out!\ncode: https://github.com/blockhead7360/gamerbot\nupdate log: http://docs.blockhead7360.com/changelogs/swwa-20010"]),
            message_set(self.empty,
                        ["who made you", "who created you",
                         "who is your creator", "who's your creator",
                         "whos your creator"],
                        ["why, master dilan himself.",
                         "dilan made me!"]),
            message_set(self.empty,
                        ["how are you"],
                        ["i'm doing alright, thanks!",
                         "i'm doing well, thanks!",
                         "i'm good, thanks!",
                         "i'm doing alright.",
                         "i'm doing well.",
                         "i'm good."]),
            message_set(self.empty,
                        ["pog"],
                        ["PogChamp"]),
            message_set(self.empty,
                        ["help", "what can you do"],
                        ["i can finally help you: " + link_help,
                         "here's a link: " + link_help,
                         "take this: " + link_help,
                         "here you go: " + link_help]),
            message_set(self.why_do_you,
                        ["why do you "],
                        ["%0", "%1", "%2"]),
            message_set(self.what_do_you,
                        ["what do you "],
                        ["%0", "%1", "%2"])
            
            ]
        
    def get_msgs(self):
        return self.set
    
    def empty(self, message):
        
        return [""]
    
    def awake(self, message):
        
        diff = datetime.now() - awake_time
        
        return [str(diff.total_seconds()) + " seconds"]
        
    
    def what_do_you(self, message):
        
        msg = message.content.replace(name, "").replace("what do you", "").strip()
        
        user = remember.get_profile(message.author.id)
        
        if "like to do" in msg:
            return ["i mean mainly just talk to people ig",
                    "i like to talk to you!",
                    "i like to do bot things."]
            
        if "like" in msg:
            return [None, "uhh idk"]
        
        if "think of me" in msg:
            
            if user is None:
                return [None, "i don't really have an opinion of you because i don't know you. you should tell me your name!"]
            
            return [None, "feature not complete"]
        
        return None
            
        
    def why_do_you(self, message):
        
        msg = message.content.replace(name, "").replace("why do you", "").strip()
        
        user = remember.get_profile(message.author.id)
        
        if user is None:
            return [None, "uhh i don't know you. i'd like to though, so you should tell me your name!"]
        
        if "hate me" in msg:
            return ["nooo i don't hate you, " + user.get_name() + "!",
                    "what makes you think i hate you, " + user.get_name() + "??",
                    "no no i don't hate you " + user.get_name() + "..."]
        
        if "love me" in msg or "like me" in msg:
            return ["because you're great, " + user.get_name() + "!",
                    "because you're pretty cool, " + user.get_name() + "!",
                    "you're just that cool, " + user.get_name() + "!"]
        
        return None
    
class Mathematics:
    
    def __init__(self):
        
        self.set = [
            message_set(self.evaluate_math,
                        [" math: ",
                         "evaluate the following mathematical expression: ",
                         "do my math hw: ",
                         "do my math homework: "],
                        ["good thing i'm a genius. here's what i got: %0",
                         "here's the answer: %0",
                         "i have evaluated a solution: %0",
                         "da math is done: %0"])
            
            ]
        
    def get_msgs(self):
        return self.set
    
    def evaluate_math(self, message):
        
        if type(message) == str:
            content = message
        else:
            content = message.content
        
        if "what is " in content:
            msg = content.partition("what is ")[2]
        else:
            msg = content.partition(": ")[2]
        
        try: ans = cexprtk.evaluate_expression(msg, {})
        except:
            return [None, "sorry i don't understand that math expression :("]
        

        return [str(ans)]

class Northwestern:
    
    def __init__(self):
        
        self.set = [
            message_set(self.get_course_desc,
                        [" course: ", " the & course"],
                        ["ooh okay got it. here's a bit about %0 %1:\n\n**%2**\n%3",
                         "i found the course description for %0 %1:\n\n**%2**\n%3",
                         "here's info on %0 %1:\n\n**%2**\n%3"]),
            message_set(self.get_covid_info,
                        ["covid like",
                         "covid is like",
                         "covid cases",
                         "covid-19 like",
                         "covid-19 is like",
                         "covid-19 cases",
                         "covid positivity rate",
                         "coronavirus like",
                         "coronavirus is like",
                         "coronavirus cases",
                         "coronavirus positivity rate"],
                        ["hmm, it's %0. the positivity rate atm is %1, with %2 positive cases out of %3 in the past 7 days. " + 
                            "since august 20, there have been %5 tests, %6 of which were positive.",
                        "ooh good question. just checked and it's %0 rn. the positivity rate is %1, with %2 positive cases out of %3 in the past week. " +
                            "since august 20, there have been %5 tests, %6 of which were positive.",
                        "well, it's %0. the positivity rate is %1, with %2 positive cases out of %3 in the past 7 days. " +
                            "since august 20, there have been %5 tests, %6 of which were positive."])
            ]
        
        pass
    
    def get_msgs(self):
        return self.set
    
    def get_covid_info(self, message):
        
        try:
            
            page = urllib.request.urlopen("https://www.northwestern.edu/coronavirus-covid-19-updates/university-status/dashboard/index.html")
            soup = BeautifulSoup(page, 'html.parser')
            
            blocks = soup.find_all("div", {"class": "stats-callout"})[0].find_all("div")
            
            info = []
            
            for block in blocks:
                
                data = block.find_all("div", {"class": "big"})
                
                if len(data) == 0: continue
                
                info.append(data[0].text)
            
            pos = float(info[0].replace("%", ""))
            
            if pos <= 1:
                msg = "not too bad"
            elif pos <= 5 and pos > 1:
                msg = "not good"
            else:
                msg = "pretty bad"
                
            info.insert(0, msg)
            
            return info
            
        except:
            return [None, "for some reason i can't get the covid-19 info, sorry :("]
        
    
    def get_course_desc(self, message):
        
        if "course: " in message.content:
            msg = message.content.partition("course: ")[2]
        else:
            msg = message.content.partition("the ")[2].partition(" course")[0]
        data = msg.split(" ")
        
        if len(data) < 2:
            return [None, "hmm i don't understand your request. make sure you specify the course subject and number"]
        
        sq = msg.partition(" ")[2]
                
        data = self._convert(data[0], data[1])
        
        found = []
        
        exact = False
        
        try:
            int(data[1].replace("-", ""))
            exact = True
            if "-" not in data[1]: data[1] += "-0"
        except:
            exact = False
        
        try:
            page = urllib.request.urlopen("https://catalogs.northwestern.edu/undergraduate/courses-az/" + data[0] + "/index.html")
            soup = BeautifulSoup(page, 'html.parser')
            
            blocks = soup.find_all("div", {"class": "courseblock"})
            
            for block in blocks:
            
                title = block.find_all("strong")
                if title is None: continue
                
                title = title[0].text.replace("\xa0", " ")
                
                if exact:
                    
                    number = title.split(" ")[1]
                    
                    if number == data[1]:
                    
                        name = title.partition(number + " ")[2].replace("\xa0", "")
                        
                        desc = "*Unable to find the course description*"
                        desc_find = block.find_all("p", {"class": "courseblockdesc"})
                        
                        if len(desc_find) > 0:
                            desc = desc_find[0].text
                        else:
                            desc_find = block.find_all("span", {"class": "courseblockdesc"})
                            if len(desc_find) > 0:
                                desc = desc_find[0].text
                        
                        extra = ""
                        extra_find = block.find_all("p", {"class": "courseblockextra"})
                        
                        if (len(extra_find) > 0):
                            extra = extra_find[0].text
                        else:
                            extra_find = block.find_all("span", {"class": "courseblockextra"})
                            if (len(extra_find) > 0):
                                extra = extra_find[0].text
                            
                        desc = desc.replace("\xa0", " ").replace("\n", "")
                        extra = " \n*" + extra.replace("\xa0", " ").replace("\n", "") + "*"
                            
                        desc += extra
                        
                        return [data[0], number, name, desc]
             
                else:
                    
                    if sq in title.lower():
                        
                        title_split = title.split(" ")
                        subj_number = title_split[0] + " " + title_split[1]
                        name = title.partition(subj_number + " ")[2]
                        
                        found.append("**" + subj_number.lower() + "** " + name)
                        
                    
                            
            if len(found) == 0: return [None, "i couldn't find the class you're looking for :("]
            
            st = "you didn't give me an exact course number to work with, but here's everything i found close to what you asked for:\n"
            
            for l in found:
                st += "\n" + l
                
            st += "\n\nlet me know if you want a description for any of them by providing me with the course number when you search."
            return [None, st]
            
        except:
            return [None, "hmm, i couldn't find what you're looking for."]
        
    def _convert(self, name, number):
        
        if name == "cs":
            return ["comp_sci", number]
        
        if name == "ea":
            return ["gen_eng", "205-" + str(number)]
        
        if name == "dtc":
            return ["dsgn", "106-" + str(number)]
        
        return [name, number]
    
class Definitions:
    
    def __init__(self):
        
        self.set = [
            message_set(self.get_definition,
                        ["what does & mean"],
                        ["here's what i found for %0 (%1):\n%2"]),
            message_set(self.get_synonyms,
                        ["a synonym for ",
                         "another word for "],
                        ["ooh here are some synonyms for %0:\n%1",
                         "i found some other words for %0:\n%1"]),
            message_set(self.get_antonyms,
                        ["the opposite of "],
                        ["here are some antonyms for %0:\n%1",
                         "i found these antonyms for %0:\n%1"])
            ]
        
    def get_msgs(self):
        return self.set
        
    
    def get_synonyms(self, message):
        
        text = message.content.partition(" for ")[2].replace("?", "")
        word = text.replace(" ", "%20")
        
        with urllib.request.urlopen("https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + key_merriamwebstertheskey) as url:
            data = json.loads(url.read().decode())
        
        if len(data) == 0:
            return [None, "i'm sorry, i couldn't find any synonyms for that word."]
        
        if type(data[0]) == dict:
            syns = data[0]["meta"]["syns"]
            
            if len(syns) == 0:
                return [None, "i couldn't find any synonyms for that word."]
            
            syn = ""
            
            if len(syns) == 1:
                
                syns = syns[0]
                
                syn = "\n" + syns[0]
                
                for i in range(len(syns)):
                
                    syn += ", " + syns[i]
                
            else:
                
                for x in range(len(syns)):
                    
                    syn += "\n" + str(x + 1) + ". " + syns[x][0]
                    
                    
                    for i in range(len(syns[x])):
                
                        syn += ", " + syns[x][i]
            
            return [text, syn]
        
        st = data[0]
        
        for i in range(1, len(data)):
            st += ", " + data[i]
        
        return [None, "i couldn't find that word specifically, but here are some words that are close: " + st]
        
    def get_antonyms(self, message):
        
        text = message.content.partition(" of ")[2].replace("?", "")
        word = text.replace(" ", "%20")
        
        with urllib.request.urlopen("https://www.dictionaryapi.com/api/v3/references/thesaurus/json/" + word + "?key=" + key_merriamwebstertheskey) as url:
            data = json.loads(url.read().decode())
        
        if len(data) == 0:
            return [None, "i'm sorry, i couldn't find any antonyms for that word."]
        
        if type(data[0]) == dict:
            ants = data[0]["meta"]["ants"]
            
            ant = ""
            
            if len(ants) == 1:
                
                ants = ants[0]
                
                ant = "\n" + ants[0]
                
                for i in range(len(ants)):
                
                    ant += ", " + ants[i]
                
            else:
                
                for x in range(len(ants)):
                    
                    ant += "\n" + str(x + 1) + ". " + ants[x][0]
                    
                    
                    for i in range(len(ants[x])):
                
                        ant += ", " + ants[x][i]
            
            return [text, ant]
        
        st = data[0]
        
        for i in range(1, len(data)):
            st += ", " + data[i]
        
        return [None, "i couldn't find that word specifically, but here are some words that are close: " + st]
        
    def get_definition(self, message):
        
        text = message.content.partition("does ")[2].partition(" mean")[0]
        word = text.replace(" ", "%20")
        
        with urllib.request.urlopen("https://www.dictionaryapi.com/api/v3/references/collegiate/json/" + word + "?key=" + key_merriamwebsterdictkey) as url:
            data = json.loads(url.read().decode())
        
        
        if len(data) == 0:
            return [None, "i'm sorry, i couldn't find what that word means!"]
        
        if type(data[0]) == dict:
            word_type = data[0]["fl"]
            word_defs = data[0]["shortdef"]
            
            if len(word_defs) == 0:
                return [None, "i couldn't find a good definition for that word."]
            
            word_def = ""
            
            if len(word_defs) == 1:
                word_def = "\n" + word_defs[0]
            else:
                
                for i in range(len(word_defs)):
                    
                    word_def += "\n" + str(i + 1) + ". " + word_defs[i]
            
            
            return [text, word_type, word_def]
        
        st = data[0]
        
        for i in range(1, len(data)):
            st += ", " + data[i]
        
        return [None, "i couldn't find that word specifically, but here are some words that are close: " + st]
            
            
class Stonks:
    
    def __init__(self):
        
        self.set = [
            message_set(self.get_data,
                        ["stock data for ",
                         "stock price of ",
                         "stonk data for ",
                         "stonk price of "],
                        ["yeah i can do that. here's what i found for %0 (i can't get today's so here's yesterday's):\n\nOpen: %1\tClose: %4\nHigh: %2\tLow: %3",
                         "sure! here's stock data for %0 (i can't get today's so here's yesterday's):\n\nOpen: %1\tClose: %4\nHigh: %2\tLow: %3",
                         "got it. here's data for %0 (i can't get today's so here's yesterday's):\n\nOpen: %1\tClose: %4\nHigh: %2\tLow: %3"])
            ]
        
    def get_msgs(self):
        return self.set
        
    def get_data(self, message):
        
        if "of " in message.content: spl = "of "
        else: spl = "for "
        
        msg = message.content.partition(spl)[2].replace("?", "")
        
        yesterday = datetime.now() - timedelta(1)
        try:
            with urllib.request.urlopen("https://api.polygon.io/v1/open-close/" + msg.upper() + "/" + datetime.strftime(yesterday, "%Y-%m-%d") + "?unadjusted=true&apiKey=" + key_polygonkey) as url:
                data = json.loads(url.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                return [None, "i can't afford to do more than around 5 requests per minute LMAO how sad."]
            else:
                return [None, "hmm i couldn't find any stock data for that."]
            
        if data["status"] == "NOT_FOUND":
            return [None, "hmm i couldn't find any stock data for that."]
        
        if data["status"] == "ERROR":
            return [None, "i can't afford to do more than 5 requests per minute LMAO how sad."]
        
        return [msg, str(data["open"]), str(data["high"]), str(data["low"]), str(data["close"])]
    
class Music:
    
    def __init__(self):
        
        self.set = [
            message_set(self.get_by_lyrics,
                        [" song that goes "],
                        ["ooh okay maybe it's one of these?\n\n%0",
                         "i found these. hopefully it's one of them.\n\n%0",
                         "i think i found it?\n\n%0",
                         "hmm maybe it's one of these?\n\n%0",
                         "i think you might be talking about one of these.\n\n%0"])
            ]
        
    def get_msgs(self):
        return self.set
    
    def get_by_lyrics(self, message):
        
        msg = message.content.partition(" that goes ")[2]
        
        try:
            
            PARAMS = {'access_token':key_geniustoken}
        
            r = requests.get(url = "https://api.genius.com/search?q=" + urllib.parse.quote_plus(msg), params = PARAMS)
            data = r.json()
            
            hits = data["response"]["hits"]
            
            if (len(hits)) == 0:
                return [None, "i couldn't find anything, sorry!"]
            
            st = ""
            
            for hit in hits:
                st += "**" + hit["result"]["title"] + "** by " + hit["result"]["primary_artist"]["name"] + "\n"
                
            return [st]
            
        except:
            
            return [None, "oh noooo something went wrong i'm sorry :("]
        
class Chemistry:
    
    def __init__(self):
        
        self.set = [
            message_set(self.get_all_data,
                        ["element data for "],
                        ["okay here's some data i found for %0 (%1):\n\n%4\n\nAtomic number: %2\nAtomic weight: %3"]),
            message_set(self.get_name,
                        [" name for "],
                        ["the name for %0? that's %1.",
                         "i believe the name for %0 is %1.",
                         "i think the name for %0 is %1."]),
            message_set(self.get_symbol,
                        [" symbol for "],
                        ["i think the symbol for %0 is %1."]),
            message_set(self.get_atomic_number,
                        [" atomic number of "],
                        ["i believe the atomic number of %0 is %1."]),
            message_set(self.get_atomic_weight,
                        [" atomic weight of ",
                         " atomic mass of "],
                        ["the atomic weight of %0 is %1."]),
            message_set(self.get_description,
                        ["tell me about the element ",
                         "description of the element "],
                        ["sure! here's what i know about %0 (%1):\n\n%2"])
            ]
        
    def get_msgs(self):
        return self.set
    
    def get_data(self, el):
        
        try:
            el = el.capitalize()
            e = mendeleev.element(el)
        except:
            return None
        
        # name, symbol, number, weight, desc
        return [e.name, e.symbol, e.atomic_number, e.atomic_weight, e.description]
        
    def get_all_data(self, message):
        
        msg = message.content.partition("element data for ")[2]
        
        data = self.get_data(msg)
        
        if data is None:
            return [None, "hmm i don't know."]
        
        return [data[0], data[1], str(data[2]), str(data[3]), str(data[4])]
        
    def get_name(self, message):
        
        msg = message.content.partition(" name for ")[2]
        
        data = self.get_data(msg)
        
        if data is None:
            return [None, "hmm i don't know."]
        
        return [msg.capitalize(), data[0]]
    
    def get_symbol(self, message):
        
        msg = message.content.partition(" symbol for ")[2]
        
        data = self.get_data(msg)
        
        if data is None:
            return [None, "hmm i don't know."]
        
        return [msg.capitalize(), data[1]]
    
    def get_atomic_number(self, message):
        
        msg = message.content.partition(" atomic number of ")[2]
        
        data = self.get_data(msg)
        
        if data is None:
            return [None, "hmm i don't know."]
        
        return [data[0], str(data[2])]
    
    def get_atomic_weight(self, message):
        
        msg = message.content.partition(" of ")[2]
        
        data = self.get_data(msg)
        
        if data is None:
            return [None, "hmm i don't know."]
        
        return [data[0], str(data[3])]
    
    def get_description(self, message):
        
        msg = message.content.partition(" the element ")[2]
        
        data = self.get_data(msg)
        
        if data is None:
            return [None, "hmm i don't know."]
        
        if data[4] is None:
            return [None, "aww i don't have a description for that element."]
    
        
        return [data[0], data[1], data[4]]
        
        

def add_message_set(init):
    
    for i in init:
        sets.append(i)

learn = Learn()
ignore = Ignore()
remember = Remember()
interactions = Interactions()
mathematics = Mathematics()
northwestern = Northwestern()
definitions = Definitions()
stonks = Stonks()
music = Music()
chemistry = Chemistry()

whitelist = ["Blockhead7360#5000"]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if ignore.is_ignored(str(message.author.id)): return
    
    message.content = message.content.lower()
    
    if name in message.content:
        
        if dev:
            
            if str(message.author) not in whitelist:
                await message.channel.send("aww sorry i can't respond rn. i'm in developer mode.")
                return
            
        history(message)
            
        if message.content.startswith(name + " /"):
            
            cmd = message.content.partition(name + " /")[2]
            
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
        
        for ls in learn_sets.keys():
        
            if ls in message.content:
            
                message.content = message.content.replace(ls, learn_sets[ls])
        
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
    
    global awake_time
    
    awake_time = datetime.now()
    
def history(message):
    
    with open("data/history/" + str(message.author.id) + ".txt", "a") as writer:
            writer.write("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") \
                         + "] [" + str(message.channel.id) + "] " + message.content + "\n")

add_message_set(learn.get_msgs())
add_message_set(music.get_msgs())
add_message_set(ignore.get_msgs())
add_message_set(definitions.get_msgs())
add_message_set(northwestern.get_msgs())
add_message_set(stonks.get_msgs())
add_message_set(chemistry.get_msgs())
add_message_set(remember.get_msgs())
add_message_set(mathematics.get_msgs())
add_message_set(interactions.get_msgs())
add_message_set(remember.get_msgs2())

# lmao no i'm not letting the bot token appear on github
client.run(key_discordtoken)


