#!/usr/bin/python3

# https://pypi.python.org/pypi/websocket-client
import websocket

end_point = "ws://service.recommender-system.com/recsys2-course/engine"

voc = {

    'Author name' : "Andrea Galloni", 
    'Author email' : 'andreagalloni[92][at]gmail[dot]com',
    'Author id' : 'JGNBMW'

}

def handle_message(ws,message):
    
    val = voc[message]
    
    print ("Received message: " + message)

    if val != None :
        res = message + ":" + val
        print ("Sending: "+res)
        ws.send(res)
    else:
        print ("Unexpected Message: " + message)


def main():

    ws = websocket.WebSocket()
    ws.connect(end_point)
    print ("CONNECTED")
    i = 0 
    while (i<3):
        handle_message(ws,ws.recv())
        i+=1

    ws.close()
    print("WebSocket closed\nexit\n")


if __name__ == "__main__":
    main()
