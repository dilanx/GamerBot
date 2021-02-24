import random

class message_set:
    
    def __init__(self, function, sig_array, message_array):
        self.function = function
        self.sig_array = sig_array
        self.message_array = message_array
        
    def call_function(self, message):
        self.args = self.function(message)
        return self.args
        
    def should_activate(self, message):
        
        for x in self.sig_array:
            
            if x in message:
                
                return True
            
        return False    
    
    def random_message(self):
        
        message = self.message_array[random.randrange(len(self.message_array))]
        for i in range(len(self.args)):
      
            message = message.replace("%" + str(i), self.args[i])
      
        return message
    
class profile_set:
    
    def __init__(self, name, number, pronouns):
        
        self.name = name
        self.number = number
        self.pronouns = pronouns
        self.data = [None]
        
    def _convert(self, data):
        
        msg = " " + data + " "
        
        if " i " in msg:
            msg = msg.replace(" i ", " %0 ")
            
        if " me " in msg:
            msg = msg.replace(" me ", " %1 ")
            
        if " my " in msg:
            msg = msg.replace(" my ", " %2 ")
            
        if " am " in msg:
            msg = msg.replace(" am ", " %3 ")
            
        return msg
        
    def add_new_data(self, data):
        
        msg = self._convert(data).strip()
        
        if msg in self.data: return False
        
        if self.data[0] is None: self.data[0] = msg.strip()
        else: self.data.append(msg.strip())
        
        self.save()
        
        return True
        
    def load_data(self, data):
        
        if self.data[0] is None: self.data[0] = data.replace("\n", "")
        else: self.data.append(data.replace("\n", ""))
        
    def del_data(self, data):
        
        msg = self._convert(data)
        
        if msg in self.data:
            self.data.remove(msg)
            self.save()
            return True
        return False
    
    def set_pronouns(self, pron_str):
        
        if "/" not in pron_str: return False
        
        msg = pron_str.split("/")
        
        if len(msg) != 3: return False
        
        fourth = "is"
        
        if msg[0] == "they":
            fourth = "are"
        
        self.pronouns = [msg[0], msg[1], msg[2], fourth]
        self.save()
        return True
        
    def get_all_raw(self):
        
        return self.data
    
    def find(self, data, use_you):
        
        if self.data[0] is None: return None
        
        for point in self.data:
            
            if data in point:
                
                point = self._format(point, use_you)
                return point
            
        return None
    
    def _format(self, msg, use_you):
        
        if use_you: msg = msg.replace("%0", "you").replace("%1", "you").replace("%2", "your").replace("%3", "are")
        else: msg = msg.replace("%0", self.pronouns[0]).replace("%1", self.pronouns[1]).replace("%2", self.pronouns[2]).replace("%3", self.pronouns[3])
        return msg
        
    
    def get_all_format(self, use_you):
        
        if self.data[0] is None: return None
        
        msg = [self._format(self.data[0], use_you)]
        
        for p in range(1, len(self.data)):
            
            point = self._format(self.data[p], use_you)
            msg.append(point)
            
        return msg
    
    def get_name(self):
        
        return self.name
    
    def get_pronouns(self):
        
        return self.pronouns
    
    def save(self):
        
        with open("profiles/" + self.number + ".txt", "w") as writer:
            writer.write(self.name + "\n")
            writer.write(str(self.pronouns) + "\n")
            if self.data[0] is not None:
                for l in self.data:
                    writer.write(l + "\n")