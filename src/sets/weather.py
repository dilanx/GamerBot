import json
import urllib

from message_groups import message_set
import utility


key_openweathermap = utility.keys["OPENWEATHERMAP-KEY"]

def get_weather_data(message):
    
    if " in " in message.content:
        msg = message.content.partition(" in ")[2]
    else:
        msg = message.content.partition(" at ")[2]
        
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
    low = data["main"]["temp_min"]
    high = data["main"]["temp_max"]
    city = data["name"]
    
    if desc_id < 300:
        weather = "there's a " + desc
    elif desc_id < 800:
        weather = "there's " + desc
    elif desc_id == 800:
        weather = "clear skies"
    else:
        weather = "there are " + desc
        
    return [weather, city, str(temp), str(high), str(low)]

msg_set = [
    message_set(get_weather_data,
                ["weather in ",
                "weather at ",
                "weather like in ",
                "weather like at ",
                "temperature & in ",
                "temperature & at ",
                "temp & in ",
                "temp & at "],
                ["good question! it looks like %0 in %1. the temperature there is %2 °F rn, with a %3 °F high and a %4 °F low.",
                "ahh yeah %0 in %1 rn at a temperature of %2 °F. the high is %3 °F and the low is %4 °F.",
                "ooh it looks like %0 in %1. it's %2 °F out right now, with a %3 °F high and a %4 °F low for today.",
                "just checked and it looks like %0 in %1 at a temp of %2 °F. the high is %3 °F and the low is %4 °F."])
    ]