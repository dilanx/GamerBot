from datetime import datetime

from message_groups import message_set
import sets.remember as remember

awake_time = 0
link_help = "<http://docs.blockhead7360.com/GamerBot>"

def empty(message):
        
    return [""]

def awake(message):
    
    diff = datetime.now() - awake_time
    
    return [str(diff.total_seconds()) + " seconds"]
    

def what_do_you(message):
    
    msg = message.content.replace("gamer bot", "").replace("what do you", "").strip()
    
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
        
    
def why_do_you(message):
    
    msg = message.content.replace("gamer bot", "").replace("why do you", "").strip()
    
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

msg_set = [
    message_set(empty,
                ["are you awake"],
                ["yeah", "yeah i'm awake!",
                 "i am indeed awake", "yup",
                 "yes"]),
    message_set(empty,
                ["can you see this", "can you read this", "you there?"],
                ["yup", "yeah i'm here!",
                 "haha yeah i'm here",
                 "ya i'm here",
                 "yeah"]),
    message_set(awake,
                ["how long have you been awake"],
                ["i've been up for like %0.",
                 "it's been %0 since i woke up.",
                 "currently around %0.",
                 "%0 lol."]),
    message_set(empty,
                ["tell me a joke"],
                ["if only i was funny :(",
                 "aww i don't know any good ones."]),
    message_set(empty,
                ["are you gay"],
                ["no i like girl bots."]),
    message_set(empty,
                ["do my & homework",
                 "do my & hw",
                 "what about my & hw",
                 "what about my & homework"],
                ["code me to and i will.",
                 "i will if you program me to.",
                 "i would if i could.",
                 "wish i could but i can't, sorry!"]),
    message_set(empty,
                ["love you", "proud of you", "you are the best", "you are awesome",
                "you are cute"],
                ["aww thank you :blush:",
                 "that means a lot :blush:",
                 "yay :blush:",
                 "how pog of you to say that :)"]),
    message_set(empty,
                ["hate you", "screw you"],
                ["wow. :pensive:",
                 "that isn't nice :pensive:",
                 "i'm trying my best :cry:"]),
    message_set(empty,
                ["how are you made", "how were you made", "are you open source", "show me your code"],
                ["check it out! <https://github.com/dilanx/gamerbot>"]),
    message_set(empty,
                ["who made you", "who created you",
                 "who is your creator", "who's your creator",
                 "whos your creator"],
                ["dilan did :)"
                 "dilan made me!"]),
    message_set(empty,
                ["how are you"],
                ["i'm doing alright, thanks!",
                 "i'm doing well, thanks!",
                 "i'm good, thanks!",
                 "i'm doing alright.",
                 "i'm doing well.",
                 "i'm good."]),
    message_set(empty,
                [" your pronouns"],
                ["you can refer to me as he/him/it :)",
                 "i like he/him/it :)",
                 "i'm he/him/it :)"]),
    message_set(empty,
                ["how is your day", "how is ur day"],
                ["i'd say it's going pretty well.",
                 "it's going pretty well, thanks for asking!",
                 "it's not too bad rn, thanks for asking!",
                 "it's pretty good."]),
    message_set(empty,
                ["pog"],
                ["PogChamp"]),
    message_set(empty,
                ["omegalul&i guess", "omegalul&ig ", "omegalul& ig",
                 "omegaluliguess"],
                ["<:omegaluliguess:814979442820382730>"]),
    message_set(empty,
                ["omegalul"],
                ["<:omegalul:757655985488789607>"]),
    message_set(empty,
                ["pagman"],
                ["<:pagman:811972091909898261>"]),
    message_set(empty,
                ["sadge"],
                ["<:sadge:798245062721929216>"]),
    message_set(empty,
                ["drop an l"],
                ["L"]),
    message_set(empty,
                ["help", "what can you do"],
                ["i can finally help you: " + link_help,
                 "here's a link: " + link_help,
                 "take this: " + link_help,
                 "here you go: " + link_help]),
    message_set(why_do_you,
                ["why do you "],
                ["%0", "%1", "%2"]),
    message_set(what_do_you,
                ["what do you "],
                ["%0", "%1", "%2"])
    
    ]