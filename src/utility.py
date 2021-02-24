

def get_ping_id(content):
    
    if "<@!" in content and ">" in content:
        
        return content.partition("<@!")[2].partition(">")[0]
        
    else:
        return None
    