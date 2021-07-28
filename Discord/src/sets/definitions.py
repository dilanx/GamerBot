import json
import urllib

from message_groups import message_set
import utility

key_merriamwebsterdictkey = utility.keys["MW-DICT-KEY"]
key_merriamwebstertheskey = utility.keys["MW-THES-KEY"]

def get_synonyms(message):
    
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
    
def get_antonyms(message):
    
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
    
def get_definition(message):
    
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

msg_set = [
    message_set(get_definition,
                ["what does & mean"],
                ["here's what i found for %0 (%1):\n%2"]),
    message_set(get_synonyms,
                ["a synonym for ",
                 "another word for "],
                ["ooh here are some synonyms for %0:\n%1",
                 "i found some other words for %0:\n%1"]),
    message_set(get_antonyms,
                ["the opposite of "],
                ["here are some antonyms for %0:\n%1",
                 "i found these antonyms for %0:\n%1"])
    ]