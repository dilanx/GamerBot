import urllib

from bs4 import BeautifulSoup

from message_groups import message_set

def get_covid_info(message):
    
    try:
        
        page = urllib.request.urlopen("https://www.northwestern.edu/coronavirus-covid-19-updates/university-status/dashboard/index.html")
        soup = BeautifulSoup(page, 'html.parser')
        
        blocks = soup.find_all("div", {"class": "stats-callout"})[0].find_all("div")
        
        info = []
        
        for block in blocks:
            
            data = block.find_all("div", {"class": "big"})
            
            if len(data) == 0: continue
            
            info.append(data[0].text)
        
        pos = float(info[0].replace("%", ""))
        
        if pos <= 1:
            msg = "not too bad"
        elif pos <= 5 and pos > 1:
            msg = "not good"
        else:
            msg = "pretty bad"
            
        info.insert(0, msg)
        
        return info
        
    except:
        return [None, "for some reason i can't get the covid-19 info, sorry :("]
    

def get_course_desc(message):
    
    if "course: " in message.content:
        msg = message.content.partition("course: ")[2]
    else:
        msg = message.content.partition("the ")[2].partition(" course")[0]
    data = msg.split(" ")
    
    if len(data) < 2:
        return [None, "hmm i don't understand your request. make sure you specify the course subject and number"]
    
    sq = msg.partition(" ")[2]
            
    data = _convert(data[0], data[1])
    
    found = []
    
    exact = False
    
    try:
        int(data[1].replace("-", ""))
        exact = True
        if "-" not in data[1]: data[1] += "-0"
    except:
        exact = False
    
    try:
        page = urllib.request.urlopen("https://catalogs.northwestern.edu/undergraduate/courses-az/" + data[0] + "/index.html")
        soup = BeautifulSoup(page, 'html.parser')
        
        blocks = soup.find_all("div", {"class": "courseblock"})
        
        for block in blocks:
        
            title = block.find_all("strong")
            if title is None: continue
            
            title = title[0].text.replace("\xa0", " ")
            
            if exact:
                
                number = title.split(" ")[1]
                
                if number == data[1]:
                
                    name = title.partition(number + " ")[2].replace("\xa0", "")
                    
                    desc = "*Unable to find the course description*"
                    desc_find = block.find_all("p", {"class": "courseblockdesc"})
                    
                    if len(desc_find) > 0:
                        desc = desc_find[0].text
                    else:
                        desc_find = block.find_all("span", {"class": "courseblockdesc"})
                        if len(desc_find) > 0:
                            desc = desc_find[0].text
                    
                    extra = ""
                    extra_find = block.find_all("p", {"class": "courseblockextra"})
                    
                    if (len(extra_find) > 0):
                        extra = extra_find[0].text
                    else:
                        extra_find = block.find_all("span", {"class": "courseblockextra"})
                        if (len(extra_find) > 0):
                            extra = extra_find[0].text
                        
                    desc = desc.replace("\xa0", " ").replace("\n", "")
                    extra = " \n*" + extra.replace("\xa0", " ").replace("\n", "") + "*"
                        
                    desc += extra
                    
                    return [data[0], number, name, desc]
         
            else:
                
                if sq in title.lower():
                    
                    title_split = title.split(" ")
                    subj_number = title_split[0] + " " + title_split[1]
                    name = title.partition(subj_number + " ")[2]
                    
                    found.append("**" + subj_number.lower() + "** " + name)
                    
                
                        
        if len(found) == 0: return [None, "i couldn't find the class you're looking for :("]
        
        st = "you didn't give me an exact course number to work with, but here's everything i found close to what you asked for:\n"
        
        for l in found:
            st += "\n" + l
            
        st += "\n\nlet me know if you want a description for any of them by providing me with the course number when you search."
        return [None, st]
        
    except:
        return [None, "hmm, i couldn't find what you're looking for."]
    
def _convert(name, number):
    
    if name == "cs":
        return ["comp_sci", number]
    
    if name == "ea":
        return ["gen_eng", "205-" + str(number)]
    
    if name == "dtc":
        return ["dsgn", "106-" + str(number)]
    
    return [name, number]

msg_set = [
    message_set(get_course_desc,
                [" course: ", " the & course"],
                ["ooh okay got it. here's a bit about %0 %1:\n\n**%2**\n%3",
                 "i found the course description for %0 %1:\n\n**%2**\n%3",
                 "here's info on %0 %1:\n\n**%2**\n%3"]),
    message_set(get_covid_info,
                ["covid like",
                 "covid is like",
                 "covid cases",
                 "covid-19 like",
                 "covid-19 is like",
                 "covid-19 cases",
                 "covid positivity rate",
                 "coronavirus like",
                 "coronavirus is like",
                 "coronavirus cases",
                 "coronavirus positivity rate"],
                ["hmm, it's %0. the positivity rate atm is %1, with %2 positive cases out of %3 in the past 7 days. " + 
                    "since august 20, there have been %5 tests, %6 of which were positive.",
                "ooh good question. just checked and it's %0 rn. the positivity rate is %1, with %2 positive cases out of %3 in the past week. " +
                    "since august 20, there have been %5 tests, %6 of which were positive.",
                "well, it's %0. the positivity rate is %1, with %2 positive cases out of %3 in the past 7 days. " +
                    "since august 20, there have been %5 tests, %6 of which were positive."])
    ]