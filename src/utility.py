import csv
import random
import mysql.connector

keys = {}
mydb = None
mydb_cursor = None


def load_keys():
    
    with open(".keys.csv") as file:
        reader = csv.reader(file, delimiter="=")
        for line in reader:
            keys[line[0]] = line[1]
            
def connect_mysql():
    
    global mydb, mydb_cursor
    
    mydb = mysql.connector.connect(
        host=keys["SQL-HOST"],
        database=keys["SQL-DB"],
        user=keys["SQL-USER"],
        password=keys["SQL-PASS"]
        )
    
    mydb_cursor = mydb.cursor()
  
def run_sql(query):
    
    try:
        mydb_cursor.execute(query)
        if not query.startswith("select"):
            mydb.commit()
        return mydb_cursor
    except:
        return False

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