#!/usr/bin/env python

from argparse import ArgumentParser
def getFileArgs():
    parser = ArgumentParser(description='Socket client.')
    parser.add_argument('-a', dest='addr',metavar='ServerAddress', help="server address with port")
    parser.add_argument('--forceRPi', dest='forceRPi',action='store_true', help="force running in raspberry pi camera mode.")
    return parser.parse_args()
args = getFileArgs()
serverAddr = args.addr or "ws://localhost:8765"
if(not serverAddr.startswith("ws://")):
    serverAddr = "ws://"+serverAddr
print("Server Address:", serverAddr)


# detect os
"""
import os
print("OS:",os.name)
if(os.name.startswith("arm") or args.forceRPi):
    # if on RPi
    import subprocess
    subprocess.call(["sudo", "modprobe", "bcm2835-v4l2"])

"""

import time
import asyncio
import websockets
import picamera
import json
import numpy as np
from FPS_helper import time_marker
import FeedbackHandler.feedback_handler as FeedBack
from MotionHandler.motion_handler import *

loop = asyncio.get_event_loop()

async def hello():
    print(time.asctime(), "Attempting to connect: ", serverAddr)
    async with websockets.connect(serverAddr) as websocket:
        print(time.asctime(), "Connected: %s"%serverAddr)
        camera_timer = time_marker()
        packet_wait_timer = time_marker()
        feedback = FeedBack.feedback_provider()
        motion = motion_handler()
        while True:
            img = np.empty((640, 480, 3), dtype=np.uint8)
            # ================ Profiling ==============
            camera_timer.mark()
            # =============== CaptureImg ==============
            camera.capture(img, format='jpeg', use_video_port=True)
            # ================ Profiling ==============
            capture_time_ms = camera_timer.ellapsed_ms()
            print("\n\nCapture Time: %d ms    [avg: %d ms]"%(capture_time_ms, camera_timer.average_ellapsed_ms()))
            # =========================================

            # =============== Processing ==============
            img = bytes(img)
            # =========================================

            await websocket.send(img)

            # ================ Profiling ==============
            packet_wait_timer.mark()
            reply = await websocket.recv()
            packet_wait_ms = packet_wait_timer.average_ellapsed_ms()
            print("Response Time: %d ms    [avg: %d ms]"%(packet_wait_ms, packet_wait_timer.average_ellapsed_ms()))
            # ============== Speech ===================
            reply = json.loads(reply)
            print(reply)
            if(reply[0] == True):
                feedback.emo_tick(reply[1])
            else:
                feedback.emo_tick('none')
            # ============== Motion ===================
            if(reply[0] == True):
                # eyeline
                eye_fromcenter_ratio = 0.2
                face_pos = reply[2]
                x, y = (int(face_pos[0] + face_pos[2])//2, int(face_pos[1] + face_pos[3])//2)
                face_size = (face_pos[2]-face_pos[0], face_pos[3]-face_pos[1])
                eye_height = int(y - (face_size[1]/2)*eye_fromcenter_ratio)
                motion.set_motion_delta(False, (eye_height - 480/2)/240)
            else:
                motion.set_motion_delta(True, 0)
            # =========================================

with picamera.PiCamera() as camera:
    print("Camera starting...")
    camera.resolution = (640, 480)
    camera.framerate = 60
    #camera.start_preview()
    time.sleep(2)
    print("Camera up")
    loop.run_until_complete(hello())
