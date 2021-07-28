import mendeleev

from message_groups import message_set

def get_data(el):
    
    try:
        el = el.capitalize()
        e = mendeleev.element(el)
    except:
        return None
    
    # name, symbol, number, weight, desc
    return [e.name, e.symbol, e.atomic_number, e.atomic_weight, e.description]
    
def get_all_data(message):
    
    msg = message.content.partition("element data for ")[2]
    
    data = get_data(msg)
    
    if data is None:
        return [None, "hmm i don't know."]
    
    return [data[0], data[1], str(data[2]), str(data[3]), str(data[4])]
    
def get_name(message):
    
    msg = message.content.partition(" name for ")[2]
    
    data = get_data(msg)
    
    if data is None:
        return [None, "hmm i don't know."]
    
    return [msg.capitalize(), data[0]]

def get_symbol(message):
    
    msg = message.content.partition(" symbol for ")[2]
    
    data = get_data(msg)
    
    if data is None:
        return [None, "hmm i don't know."]
    
    return [msg.capitalize(), data[1]]

def get_atomic_number(message):
    
    msg = message.content.partition(" atomic number of ")[2]
    
    data = get_data(msg)
    
    if data is None:
        return [None, "hmm i don't know."]
    
    return [data[0], str(data[2])]

def get_atomic_weight(message):
    
    msg = message.content.partition(" of ")[2]
    
    data = get_data(msg)
    
    if data is None:
        return [None, "hmm i don't know."]
    
    return [data[0], str(data[3])]

def get_description(message):
    
    msg = message.content.partition(" the element ")[2]
    
    data = get_data(msg)
    
    if data is None:
        return [None, "hmm i don't know."]
    
    if data[4] is None:
        return [None, "aww i don't have a description for that element."]

    
    return [data[0], data[1], data[4]]

msg_set = [
    message_set(get_all_data,
                ["element data for "],
                ["okay here's some data i found for %0 (%1):\n\n%4\n\nAtomic number: %2\nAtomic weight: %3"]),
    message_set(get_name,
                [" name for "],
                ["the name for %0? that's %1.",
                 "i believe the name for %0 is %1.",
                 "i think the name for %0 is %1."]),
    message_set(get_symbol,
                [" symbol for "],
                ["i think the symbol for %0 is %1."]),
    message_set(get_atomic_number,
                [" atomic number of "],
                ["i believe the atomic number of %0 is %1."]),
    message_set(get_atomic_weight,
                [" atomic weight of ",
                 " atomic mass of "],
                ["the atomic weight of %0 is %1."]),
    message_set(get_description,
                ["tell me about the element ",
                 "description of the element "],
                ["sure! here's what i know about %0 (%1):\n\n%2"])
    ]