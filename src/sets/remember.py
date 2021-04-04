from message_groups import message_set, profile_set
import os
import sets.mathematics as mathematics

_data = {}

def hello(message):
    
    if str(message.author.id) not in _data:
        
        return [None, "oh hello there! i'm gamer bot! i'm not sure who you are but you should tell me your name so i remember."]
    
    your_name = _data[str(message.author.id)].get_name()
    
    return [your_name]

def new(message):
        
    if str(message.author.id) in _data:
        
        name = _data[str(message.author.id)].get_name()
        
        return [None, "i already remember you as " + name]
    
    name = message.content.partition("my name is ")[2].strip()
    
    if " " in name: name = name.split(" ")[0]
    
    
    ps = profile_set(name, str(message.author.id), ["they", "them", "their", "are"])
    ps.save()
    _data[str(message.author.id)] = ps 
    
    return [name]

def pronouns(message):
        
    if str(message.author.id) not in _data:
        
        return [None, "oh no i don't know your name. you'll have to let me remember that before i can remember other stuff about you."]
    
    msg = message.content.partition("my pronouns are ")[2].strip()
    
    if " " in msg: msg = msg.split(" ")[0]
    
    ans = _data[str(message.author.id)].set_pronouns(msg)
    
    if not ans:
        return [None, "sorry, but i don't know what you mean. your pronouns need to be typed like subject/object/possession. for example: they/them/their, she/her/her, he/him/his"]
    
    return [""]

def remember(message):
        
    if str(message.author.id) not in _data:
        
        return [None, "oh no i don't know your name. you'll have to let me remember that before i can remember other stuff about you."]
        
    msg = message.content.partition("remember ")[2]
    
    if msg.startswith("that"): msg = msg.partition("that")[2].strip()
    
    msg = msg.replace(".", "").replace("!", "")
        
    ans = _data[str(message.author.id)].add_new_data(msg)
    
    if not ans:
        
        return [None, "hmm i already know that."]
    
    return [_data[str(message.author.id)].get_name()]

def forget(message):
        
        if str(message.author.id) not in _data:
            
            return [None, "oh no i don't know your name. you'll have to let me remember that before i can remember other stuff about you."]
            
        msg = message.content.partition("forget ")[2]
        
        if msg.startswith("that"): msg = msg.partition("that")[2].strip()
        
        msg = msg.replace(".", "").replace("!", "")
            
        ans = _data[str(message.author.id)].del_data(msg)
        
        if not ans:
            
            return [None, "i can't forget something about you that i didn't know"]
        
        return [_data[str(message.author.id)].get_name()]
    
def what_is_my(message):
        
    return _what_i(message, " my ")
    
def what_do_i(message):
        
    return _what_i(message, " i ")
    
def _what_i(message, split_type):
        
    if str(message.author.id) not in _data:
        
        return [None, "i'm afraid that i don't know who you are. you'll have to let me remember your name first."]
    
    if "who am i" in message.content.strip():
        return ["your name is " + _data[str(message.author.id)].get_name()]
    
    st = message.content.partition(split_type)[2]
    if (st.strip() in ["name", "name?"]): return ["your name is " + _data[str(message.author.id)].get_name()]
    else: info = _data[str(message.author.id)].find(message.content.partition(split_type)[2], True)
    
    if info is None:
        
        return [None, "i don't know :( but you should tell me."]
    
    return [info]

def what_is_other(message):
        
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
    
    return _what_other(who, msg)

def what_does_other(message):
    
    first_part = message.content.split("what does ")[1]
    if " " not in message.content: return None
    who = first_part.split(" ")[0]
    msg = first_part.split(" ")[1].replace("?", "")
    
    return _what_other(who, msg)
        
def _what_other(who, msg):
    
    who = who.strip()
    
    for d in _data.values():
        if d.get_name() == who:
            
            ans = d.find(msg, False)
            if ans is None:
                return [None, "i know " + d.get_name() + " but i don't know " + d.get_pronouns()[2] + " " + msg + " :("]
            
            return [d.get_name(), ans]
            
    return [None, "i don't know who you're talking about :("]

def talk_about_me(message):
    
    if str(message.author.id) not in _data:
        
        return [None, "aww i don't remember you, sorry! i'd love to hear about you though :)"]
    
    info = _data[str(message.author.id)]
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
    
def talk_about_you(message):
    
    if str(message.author.id) not in _data:
        
        return [None, "you first! what's your name?"]
    
    your_name = _data[str(message.author.id)].get_name()
    
    return [your_name]
    
def talk_about_other(message):
    
    who = message.content.split("tell me about ")[1]
    
    for d in _data.values():
        
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
    
def talk_about_all(message):
    
    st = "here's everyone ik:"
    
    nws = []
    
    for d in _data.values():
        
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
            
    
def all_remember(message):
    
    if len(_data.values()) == 0:
        return [None, "i don't know anyone :'("]
    
    val = list(_data.values())
    
    st = val[0].get_name()
    
    for i in range(1, len(val)):
        
        if i == len(val) - 1:
            
            st += ", and " + val[i].get_name() + "."
            
        else:
            
            st += ", " + val[i].get_name()
            
    return [st]
    
def forget_about_me(message):
    
    if str(message.author.id) not in _data:
        
        return [None, "i can't forget about someone i don't know xD"]
    
    name = _data[str(message.author.id)].get_name()

    _data[str(message.author.id)].forget()
    
    del _data[str(message.author.id)]
    
    return [name]

def get_profile(sender_id):
    if str(sender_id) not in _data: return None
    else: return _data[str(sender_id)]

def _load():
        
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
            
        _data[number] = prof

_load()

msg_set = [
    message_set(all_remember,
                ["who all do you remember", "who do you remember", "who all do you know"],
                ["here are the names of everyone i remember: %0 i'd love to meet more people (just tell me to remember your name)!",
                 "i remember these people: %0 i'd love to meet more people though (just tell me to remember your name)!",
                 "here are all the people i know: %0 i'd love to meet more people (just tell me to remember your name)!"]),
    message_set(new,
                ["remember my name is ", "remember that my name is ", "my name is "],
                ["okay %0! i'll remember you.",
                 "nice to meet you %0! i'll remember you now."]),
    message_set(pronouns,
                ["remember my pronouns are ", "remember that my pronouns are ", "my pronouns are "],
                ["thanks! i know how to refer to you now.",
                 "okay got it."]),
    message_set(talk_about_all,
                ["tell me about everyone"],
                ["%0"]),
    message_set(talk_about_me,
                ["tell me about myself", "what do you know about me"],
                ["ofc! here's what i know about you, %0: %1"]),
    message_set(talk_about_you,
                ["tell me about yourself"],
                ["there isn't really to say much about me, %0. i'm a discord bot lmaoo. i do like talking to you though :)",
                 "hmm tbh idrk. i'm a discord bot who likes talking to people, especially you %0 :)",
                 "i like talking to ppl, like you, %0, as well as giving them helpful information. other than that i'm just a little discord bot :)"]),
    message_set(talk_about_me,
                ["do you remember me"],
                ["ofc i do! here's what i know about you, %0: %1",
                 "how could i forget! here's what i know about you, %0: %1"]),
    message_set(forget_about_me,
                ["forget everything about me"],
                ["it was nice knowing you, %0! i'll forget everything about you as you requested",
                 "well, ig all friendships come to an end. goodbye %0 :'(",
                 "as you request, %0."]),
    message_set(talk_about_other,
                ["tell me about "],
                ["ooh okay. here's what i know about %0: %1",
                 "oh I remember %2! here's what i know about %0: %1",
                 "how could i forget about %0! here's what i know about %2: %1"]),
    message_set(remember,
                ["remember ", "remember that "],
                ["okay %0, i'll remember that now.",
                 "cool! i'll remember that.",
                 "okay. i won't forget"]),
    message_set(forget,
                ["forget ", "forget that "],
                ["forget what :)",
                 "okay %0, i'll forget about that."]),
    message_set(what_is_my,
                ["what is my ", "what are my ", "whats my ", "what's my ", "who am i"],
                ["oh i know! %0",
                 "here's what i know: %0"]),
    message_set(what_do_i,
                ["what do i "],
                ["oh i know! %0",
                 "here's what i know: %0"]),
    message_set(what_is_other,
                ["what is ", "what are ", "whats ", "what's "],
                ["ooh i know this about %0: %1",
                 "%0 told me this earlier: %1",
                 "this is what i know about %0: %1"]),
    message_set(what_does_other,
                ["what does "],
                ["ooh i know this about %0: %1",
                 "%0 told me this earlier: %1",
                 "this is what i know about %0: %1"])
    ]

msg_set_LOW = [
    message_set(hello,
            ["hello", "hi", "sup", "hey", "good morning", "good afternoon", "good evening"],
            ["umm hi %0",
             "oh hello there %0",
             "hi %0!!",
             "hello %0!!",
             "hey %0! how are you?",
             "hi %0! how are you doing?",
             "hello %0. how are you?"])
    
    ]