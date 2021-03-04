import random

def r_msg(msgs):
    
    return msgs[random.randrange(len(msgs))]
    
def in_msg(msg, arr):
    
    for i in arr:
        if i in msg: return True
        
    return False
    
    

def get_ping_id(content):
    
    if "<@!" in content and ">" in content:
        
        return content.partition("<@!")[2].partition(">")[0]
        
    else:
        return None
    
class SubjectPronounDictionary:
    
    def __init__(self):
        self.map = {}
        self._load()
        
    def get_map(self):
        return self.map
    
    def _load(self): 
        with open("data/spd.txt", "r") as reader:
            lines = reader.readlines()
        
        for l in lines:
            
            split = l.replace("\n", "").split(" ")
            self.map[split[0]] = split[1]
    
    def add_to_map(self, old, new):
        
        self.map[old] = new
        self._save_upd(old + " " + new)
        
    def _save_upd(self, line):
        with open("data/spd.txt", "a") as writer:
            writer.write(line + "\n")