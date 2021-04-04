import cexprtk

from message_groups import message_set

def evaluate_math(message):
        
    if type(message) == str:
        content = message
    else:
        content = message.content
    
    if "what is " in content:
        msg = content.partition("what is ")[2]
    else:
        msg = content.partition(": ")[2]
    
    try: ans = cexprtk.evaluate_expression(msg, {})
    except:
        return [None, "sorry i don't understand that math expression :("]
    

    return [str(ans)]
    
msg_set = [
        message_set(evaluate_math,
                    [" math: ",
                     "evaluate the following mathematical expression: ",
                     "do my math hw: ",
                     "do my math homework: "],
                    ["good thing i'm a genius. here's what i got: %0",
                     "here's the answer: %0",
                     "i have evaluated a solution: %0",
                     "da math is done: %0"])
        
        ]