from datetime import datetime, timedelta
import json
import urllib

from message_groups import message_set
import utility


key_polygonkey = utility.keys["POLYGON-KEY"]

def get_data(message):
    
    if "of " in message.content: spl = "of "
    else: spl = "for "
    
    msg = message.content.partition(spl)[2].replace("?", "")
    
    yesterday = datetime.now() - timedelta(1)
    try:
        with urllib.request.urlopen("https://api.polygon.io/v1/open-close/" + msg.upper() + "/" + datetime.strftime(yesterday, "%Y-%m-%d") + "?unadjusted=true&apiKey=" + key_polygonkey) as url:
            data = json.loads(url.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            return [None, "i can't afford to do more than around 5 requests per minute LMAO how sad."]
        else:
            return [None, "hmm i couldn't find any stock data for that."]
        
    if data["status"] == "NOT_FOUND":
        return [None, "hmm i couldn't find any stock data for that."]
    
    if data["status"] == "ERROR":
        return [None, "i can't afford to do more than 5 requests per minute LMAO how sad."]
    
    return [msg, str(data["open"]), str(data["high"]), str(data["low"]), str(data["close"])]

msg_set = [
    message_set(get_data,
                ["stock data for ",
                 "stock price of ",
                 "stonk data for ",
                 "stonk price of "],
                ["yeah i can do that. here's what i found for %0 (i can't get today's so here's yesterday's):\n\nOpen: %1\tClose: %4\nHigh: %2\tLow: %3",
                 "sure! here's stock data for %0 (i can't get today's so here's yesterday's):\n\nOpen: %1\tClose: %4\nHigh: %2\tLow: %3",
                 "got it. here's data for %0 (i can't get today's so here's yesterday's):\n\nOpen: %1\tClose: %4\nHigh: %2\tLow: %3"])
    ]