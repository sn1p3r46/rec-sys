#!/usr/bin/python3

INVALID_KBASE = "Received Invalid Knowledge Base"
END_POINT = "ws://service.recommender-system.com/recsys2-course/engine"

AUTH_DIC = {

    'Author name' : 'Andrea Galloni', 
    'Author email' : 'andreagalloni[92][at]gmail[dot]com',
    'Author id' : 'JGNBMW',
    'Token' : '4lvos7hd1a',
}


def send(ws,msg):
    print ("Sending: \"" + msg + "\"")
    ws.send(msg)

def format_set_to_arr_str(myset):
    return "[\""+'","'.join([x for x in myset ])+"\"]"
