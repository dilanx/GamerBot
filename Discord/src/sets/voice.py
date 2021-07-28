from message_groups import message_set
import utility
import youtube_dl

def join_vc(message):

    if message.author.voice == None:
        return [None, "ask me again when you join a vc!"]

    if utility.voice_channel != None:
        if utility.voice_channel.is_connected():
            return [None, "i'm already in a vc."]
        else:
            utility.voice_channel = None

    utility.planned_joinvc = True
    return [""]

def leave_vc(message):

    if utility.voice_channel == None:
        return [None, "i'm not in a vc."]

    if not utility.voice_channel.is_connected():
        utility.voice_channel = None
        return [None, "i'm not in a vc."]

    utility.planned_leavevc = True
    return [""]


msg_set = [
    message_set(join_vc,
                ["join vc",
                "join the vc",
                "join me in vc",
                "join the voice channel",
                "join voice",
                "join me in the voice channel",
                "join me in voice"],
                ["okay, i'll get on.",
                "be on in a second.",
                "sure, i'll be on in a sec."]),
    message_set(leave_vc,
                ["leave vc",
                "leave the vc",
                "disconnect",
                "leave the voice channel",
                "leave voice channel",
                "leave voice"],
                ["alrighty.",
                "okay i'll go.",
                "good bye!"])
]
