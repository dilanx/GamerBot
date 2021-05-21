import csv

from message_groups import message_set
import utility


reminders = {}

class Reminder:
    
    def __init__(self, time, sender, channel, message):
        
        self.time = time
        self.sender = sender
        self.channel = channel
        self.message = message
        
    def as_array(self):
        
        return [self.time, self.sender, self.channel, self.message]

def load():

    with open("data/reminders.csv") as file:
        reader = csv.reader(file, delimiter=",")
        for line in reader:
            reminders[line[0]] = Reminder(float(line[0]), int(line[1]), int(line[2]), line[3])
        
load()
    
def save():
    
    with open("data/reminders.csv", "w") as file:
        writer = csv.writer(file, delimiter=",")
        
        for r in reminders:
            
            writer.writerow(reminders[r].as_array())

def add_reminder(message):
    
    msg = message.content.partition(" to ")[2]
    
    if " at " not in msg:
        return [None, "hmm i'll need a date and time to remind you at."]
    
    if " today" in msg:
        
        on = "today"
        sp = msg.split(" at ")
        to = sp[0].replace(" today", "").strip()
        at = msg.split(" at ")[1].replace(" today", "").strip()
        
    elif " tomorrow" in msg:
        
        on = "tomorrow"
        sp = msg.split(" at ")
        to = sp[0].replace(" tomorrow", "").strip()
        at = sp[1].replace(" tomorrow", "").strip()
    
    else:
        
        if " on " not in msg:
            return [None, "hmm i'll need a date and time to remind you at."]
        
        on_at = msg.split(" on ")
        if " at " in on_at[0]:
            sp = on_at[0].split(" at ")
            to = sp[0]
            on = on_at[1]
            at = sp[1]
        elif " at " in on_at[1]:
            sp = on_at[1].split(" at ")
            to = on_at[0]
            on = sp[0]
            at = sp[1]
        else:
            return None
    
    ymd = utility.date2ymd(on)
    hm = utility.time2hm(at)
    
    if ymd == None:
        return [None, "i'm not sure what date you're talking about."]
    if hm == None:
        return [None, "i'm not sure what time you're talking about."]
        
    etime = utility.dt2stamp(ymd[0], ymd[1], ymd[2], hm[0], hm[1])
    
    to = utility.fp2sp(to)
    
    reminder = Reminder(etime, message.author.id, message.channel.id, to)
    
    reminders[str(etime)] = reminder
    save()
    
    return [utility.stamp2human(etime), to]

def delete_reminder(message):
    
    msg = message.content.partition(" to ")[2]
    
    r_list = []
    
    for r in reminders:
        
        if reminders[r].sender == message.author.id and reminders[r].message == utility.fp2sp(msg):
            
            r_list.append(r)
    
    if len(r_list) == 0:
        return [None, "you never told me to remind you about that in the first place lol."]
    
    for r in r_list:
        
        del reminders[r]
    
    save()
    
    return [""]
            

def my_reminders(message):
    
    r_list = []
    
    for r in reminders:
        
        if reminders[r].sender == message.author.id:
            r_list.append(reminders[r])
    
    if len(r_list) == 0:
        return [None, "you haven't told me to remind you about anything in the future."]
    
    st = ""    
    for i in range(len(r_list)):
        
        r = r_list[i]
        
        st += utility.stamp2human(float(r.time)) + ": " + r.message
        
        if i < len(r_list) - 1:
            st += "\n"
        
    return [st]
        

msg_set = [
    message_set(delete_reminder,
                ["do not remind me to ", " no longer remind me to ",
                 "delete & reminder to ", "remove & reminder to "],
                ["okay. i won't remind you about that anymore.",
                 "sure! i won't remind you about that.",
                 "okay sounds good."]),
    message_set(add_reminder,
                ["remind me to ", " set a reminder to"],
                ["okay! i'll remind you to %1 on %0.",
                 "sounds good. i'll remind you to %1 on %0.",
                 "sure thing. i'll remind you to %1 on %0."]),
    message_set(my_reminders,
                ["my reminders", "going to remind me about"],
                ["here are the things i'll remind you about:\n\n%0",
                 "here's what i'll remind you about:\n\n%0"])
    ]

reminder_msgs = [
    "%0! don't forget to %1!",
    "%0!! i'm reminding you to %1.",
    "here's your reminder to %1, %0.",
    "hi %0!! i'm reminding you to %1."
    ]
    