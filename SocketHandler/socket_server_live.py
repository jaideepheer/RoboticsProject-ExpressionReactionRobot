#!/usr/bin/env python

# WS server example

import asyncio
import functools
import websockets
import cv2
import numpy as np
import time
import FPS_helper

loop = asyncio.get_event_loop()
frame_timer = FPS_helper.time_marker()

def add_overlay(image, fps, frame_time):
    height, width = image.shape[0:2]
    cv2.putText(image, "FPS: %f"%fps, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,30), 1)
    cv2.putText(image, "Frame Time: %fms"%(frame_time/10**6), (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,30), 1)

def showImg(image):
    add_overlay(image, (1/frame_timer.ellapsed_sec()), frame_timer.ellapsed_ns())
    frame_timer.mark()
    cv2.imshow('preview',image)
    cv2.waitKey(1)

async def hello(websocket, path):
    try:
        print(time.asctime(), "Client connected: %s"%'localhost')
        #stream = cv2.VideoCapture(0)
        while True:
            image = await websocket.recv()
            await websocket.send("next")
            print(time.asctime(), "Data recieved: %d bytes"%len(image))
            image = np.frombuffer(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            showImg(image) # preview image
    finally:
        print(time.asctime(), "Client disconnected: %s"%'localhost')
        cv2.destroyAllWindows()
        #exit()


start_server = websockets.serve(hello, '', 8765, max_size=None)
print(time.asctime(), "Server started: ws://localhost:8765")
loop.run_until_complete(start_server)
loop.run_forever()