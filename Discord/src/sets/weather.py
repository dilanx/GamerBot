import json
import urllib

from message_groups import message_set
import utility

key_openweathermap = utility.keys["OPENWEATHERMAP-KEY"]

def get_weather_data(message):
    
    if " in " in message.content:
        msg = message.content.partition(" in ")[2]
    elif " at " in message.content:
        msg = message.content.partition(" at ")[2]
    else:
        msg = "evanston";
        
    if " " in msg:
        msg = msg.split(" ")[0]
        
    with urllib.request.urlopen("http://api.openweathermap.org/data/2.5/weather?q=" + msg + "&units=imperial&appid=" + key_openweathermap) as url:
        data = json.loads(url.read().decode())
    
    code = data["cod"]
    if code != 200:
        return [None, "aww i couldn't find weather data for that place."]
    
    desc_id = data["weather"][0]["id"]
    desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    city = data["name"]
    
    if desc_id < 300:
        weather = "there's a " + desc
    elif desc_id < 800:
        weather = "there's " + desc
    elif desc_id == 800:
        weather = "clear skies"
    else:
        weather = "there are " + desc
        
    return [weather, city, str(temp)]

msg_set = [
    message_set(get_weather_data,
                ["what is the weather",
                "weather in ",
                "weather at ",
                "weather like in ",
                "weather like at ",
                "temperature & in ",
                "temperature & at ",
                "temp & in ",
                "temp & at "],
                ["good question! it looks like %0 in %1. the temperature there is %2 °F rn.",
                "ahh yeah %0 in %1 rn at a temperature of %2 °F.",
                "ooh it looks like %0 in %1. it's %2 °F out right now.",
                "just checked and it looks like %0 in %1 at a temp of %2 °F."])
    ]