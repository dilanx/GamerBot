import csv

from message_groups import message_set


learn_sets = {}
main_sets = []

def learn(message):

    msg = message.content.partition("learn that ")[2]
        
    if msg.startswith("saying "):
        msg = msg.partition("saying ")[2]
        
    if " is like saying " in msg:
        msg = msg.split(" is like saying ")
                
    understood = False
    
    for al in learn_sets.keys():
        
        if msg[1] == al:
            
            understood = True
    
    for s in main_sets:
        if s.should_activate(msg[1]):
            
            understood = True
            
    
    if not understood: return [None, "wait i don't know what \"" + msg[1] + "\" means"]
    
    learn_sets[msg[0]] = msg[1]
    _save()
    
    return [""]

def _load():

    with open("data/learn.csv") as file:
        reader = csv.reader(file, delimiter=",")
        for line in reader:
            learn_sets[line[0]] = line[1]
            
            
def _save():
    
    with open("data/learn.csv", "w") as file:
        writer = csv.writer(file, delimiter=",")
        
        for s in learn_sets:
            writer.writerow([s, learn_sets[s]])


_load()

msg_set = [
    message_set(learn,
                ["learn that & is like saying "],
                ["ooh okay thanks for teaching me!",
                 "ahh okay i'll remember that.",
                 "okay got it now thanks!",
                 "ohh so that's what that means. thanks!"])
            
        ]