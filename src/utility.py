import csv
import datetime
import random

import mysql.connector

keys = {}
mydb = None
mydb_cursor = None
client = None

voice_channel = None

planned_joinvc = False
planned_leavevc = False

changelog_msg = ""

def get_user_from_id(id):
    return client.fetch_user(id)

days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
                "mon", "tue", "wed", "thurs", "fri", "sat", "sun"]

def load_keys():

    with open(".keys.csv") as file:
        reader = csv.reader(file, delimiter="=")
        for line in reader:
            keys[line[0]] = line[1]

def load_changelog():

    with open("changelog.txt") as file:

        lines = file.readlines()

    global changelog_msg

    for l in lines:

        changelog_msg += l

load_changelog()

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

def time2hm(time_str):

    if " " in time_str:
        times = time_str.split(" ")
    else:
        times = [time_str]

    if len(times) < 2:

        for x in ["am", "pm"]:

            if times[0].endswith(x):
                times[0] = times[0][:-2]
                times.append(x)

    if len(times) < 2:
        return None

    hour = 0
    minute = 0

    if ":" in times[0]:

        time_sp = times[0].split(":")
        try:
            hour = int(time_sp[0])
            minute = int(time_sp[1])
        except:
            return None
    else:
        try:
            hour = int(times[0])
        except:
            return None

    if times[1] == "am":
        if hour == 12:
            hour = 0
    elif times[1] == "pm":
        if hour < 12:
            hour += 12
    else:
        return None

    return [hour, minute]



def date2ymd(date_str):

    if date_str == "today":

        next_date = datetime.datetime.now()

    elif date_str == "tomorrow":

        next_date = datetime.datetime.now() + datetime.timedelta(days=1)

    else:

        if " " in date_str:
            dates = date_str.split(" ")
        else:
            dates = [date_str]

        dow = None

        try:
            dow = days_of_week.index(dates[0])
            if dow > 6:
                dow -= 7

            today = datetime.date.today().weekday()

            dist = dow - today

            if dist <= 0:
                dist += 7

            next_date = datetime.datetime.now() + datetime.timedelta(days=dist)

        except:

            if len(dates) != 3:
                return None

            month = dates[0].capitalize()
            day = dates[1]
            year = dates[2]

            try:
                next_date = datetime.datetime.strptime(month + " " + day + " " + year, "%B %d %Y")
            except:
                return None

    return [next_date.date().year, next_date.date().month, next_date.date().day]


def dt2stamp(year, month, day, hour, minute):

    return datetime.datetime(year, month, day, hour, minute).timestamp()

def stamp2human(time):

    return datetime.datetime.fromtimestamp(time).strftime("%B %d %Y at %H:%M")

def get_ping_id(content):

    if "<@!" in content and ">" in content:

        return content.partition("<@!")[2].partition(">")[0]

    else:
        return None

def fp2sp(phrase):

    s = " " + phrase + " "

    return s.replace(" i ", " you ").replace(" me ", " you ").replace(" my ", " your ").strip()

def sp2fp(phrase):

    s = " " + phrase + " "

    return s.replace(" you ", " i ").replace(" you ", " me ").replace(" your ", " my ").strip()

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


load_keys()
connect_mysql()
