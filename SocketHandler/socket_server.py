import asyncio
import functools
import websockets
import cv2
import numpy as np
import time
import FPS_helper
class Server:
    async def __default_connection_handler__(websocket, path):
        try:
            print(time.asctime(), "Client connected: %s"%'localhost')
            while True:
                image = await websocket.recv()
                await websocket.send("next")
                print(time.asctime(), "Data recieved: %d bytes"%len(image))
                image = np.frombuffer(image, np.uint8)
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        finally:
            print(time.asctime(), "Client disconnected: %s"%'localhost')
    
    def setConnectionHandler(self, connection_handler):
        self.__connection_handler__ = connection_handler
    
    def startServer(self):
        if(self.isRunning):
            raise RuntimeError("Server already running...!")
            return
        self.isRunning = True
        self.server = websockets.serve(self.__connection_handler__, self.host, self.port, max_size=None)
        self.loop.run_until_complete(self.server)
        print(time.asctime(), "Server started: ws://%s:%d"%(self.host, self.port))
    
    def serverTick(self):
        if(not self.isRunning):
            raise RuntimeError("Server not running...!")
            return
        self.loop.run_until_complete(self.server)
    
    def serverForeverBlockingTick(self):
        if(not self.isRunning):
            raise RuntimeError("Server not running...!")
            return
        self.loop.run_forever()
    
    
    def __init__(self, host='0.0.0.0', port=8765, connection_handler=__default_connection_handler__):
        self.isRunning = False
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()
        self.__connection_handler__ = connection_handler
        self.message_timer = FPS_helper.time_marker()