#!/usr/bin/python3

import asyncio
import websockets

questions = ['Author name','Author email','Author id']

async def handler(websocket,path):
    try:
        for q in questions:
            await websocket.send(q)
            data = await websocket.recv()
            print (q + " : " + data)

    except websockets.exceptions.ConnectionClosed :
        print( "Connection Unexpectedly Closed by the Client" )


start_server = websockets.serve(handler, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

