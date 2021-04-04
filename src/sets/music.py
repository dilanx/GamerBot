import urllib

import requests

from message_groups import message_set
import utility


key_geniustoken = utility.keys["GENIUS-TOKEN"]

def get_by_lyrics(message):
    
    msg = message.content.partition(" that goes ")[2]
    
    try:
        
        PARAMS = {'access_token':key_geniustoken}
    
        r = requests.get(url = "https://api.genius.com/search?q=" + urllib.parse.quote_plus(msg), params = PARAMS)
        data = r.json()
        
        hits = data["response"]["hits"]
        
        if (len(hits)) == 0:
            return [None, "i couldn't find anything, sorry!"]
        
        st = ""
        
        for hit in hits:
            st += "**" + hit["result"]["title"] + "** by " + hit["result"]["primary_artist"]["name"] + "\n"
            
        return [st]
        
    except:
        
        return [None, "oh noooo something went wrong i'm sorry :("]
    
msg_set = [
    message_set(get_by_lyrics,
                [" song that goes "],
                ["ooh okay maybe it's one of these?\n\n%0",
                 "i found these. hopefully it's one of them.\n\n%0",
                 "i think i found it?\n\n%0",
                 "hmm maybe it's one of these?\n\n%0",
                 "i think you might be talking about one of these.\n\n%0"])
    ]