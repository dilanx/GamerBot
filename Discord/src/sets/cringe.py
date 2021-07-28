from message_groups import message_set
import utility

def add_cringe(message):

    if "<@" not in message.content:
        return [None, "hmm you need to tag someone so i know who you're talking about."]
    to = message.content.split("<@")[1].split(">")[0]
    if to.startswith("!"): to = to.replace("!", "")

    utility.connect_mysql()

    current = utility.run_sql("select cringe from cringe_points where user = '" + to + "'").fetchall()

    if len(current) == 0:

        utility.run_sql("insert into cringe_points (user, cringe) values ('" + to + "', 1)")
        return [to, "1"]

    else:

        cur_count = current[0][0] + 1
        utility.run_sql("update cringe_points set cringe = " + str(cur_count) + " where user = '" + to + "'")
        return [get_name_from_id(to), str(cur_count)]

def view_cringe(message):

    if "<@" not in message.content:
        return [None, "hmm you need to tag someone so i know who you're talking about."]
    to = message.content.split("<@")[1].split(">")[0]
    if to.startswith("!"): to = to.replace("!", "")

    utility.connect_mysql()

    current = utility.run_sql("select cringe from cringe_points where user = '" + to + "'").fetchall()

    if len(current) == 0:
        return [None, "they have no cringe points!"]

    else:
        num = current[0][0]

        if num == 0:
            return [None, "they have no cringe points!"]

        return [get_name_from_id(to), str(current[0][0])]

def cringe_leaderboard(message):
    return ["coming soon"]

def get_name_from_id(id):
    # TEMPORARY UNTIL I FIGURE OUT A BETTER WAY

    return "<@" + id + ">"

    #result = utility.run_sql("select name from cringe_points where user = '" + id + "'").fetchall()
    #return result[0]

msg_set = [
    message_set(add_cringe,
        ["give a cringe point to ",
        "give a cp to ",
        "add a cringe point to ",
        "add a cp to "],
        ["okay! %0 now has %1 cringe points.",
        "lmao cringee now %0 has %1 cringe points.",
        "%0 now has %1 cringe points."]
    ),
    message_set(view_cringe,
        ["how many cringe points does & have",
        "how cringe is "],
        ["looks like %0 has %1 cringe points.",
        "%0 has %1 cringe points. what a shame.",
        "%0 has %1 cringe points."]
    ),
    message_set(cringe_leaderboard,
        ["cringe leaderboard"],
        ["here's the cringe leaderboard:\n\n%0",
        "check out the cringe leaderboard:\n\n%0",
        "ooh check it out:\n\n%0",
        "here's the leaderboard of cringe:\n\n%0"])
]
