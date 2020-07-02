from image_to_emotion import image_to_emotion, cascade_face_detector, dnn_face_detector
from SocketHandler.socket_server import Server
from FPS_helper import time_marker
import cv2
import json
import numpy as np
import time

class emotion_server:
    emotion_predictor = None
    show_preview = True

    def add_eyeline(image, face_center, face_size, size=5, thickness=2):
        x, y = face_center
        # face center
        cv2.line(image, (x-size, y), (x+size, y), (0,255,0), thickness)
        cv2.line(image, (x, y-size), (x, y+size), (0,255,0), thickness)
        # eyeline
        eye_fromcenter_ratio = 0.2
        eye_height = int(y - (face_size[1]/2)*eye_fromcenter_ratio)
        cv2.line(image, (x-size, eye_height), (x+size, eye_height), (10,10,255), thickness+1)

    def add_overlay(image, fps, frame_time_ns, emotion, face_pos):
        height, width = image.shape[0:2]
        cv2.putText(image, "FPS: %f"%fps, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,30), 1)
        cv2.putText(image, "Frame Time: %fms"%(frame_time_ns/(10**6)), (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,30), 1)
        cv2.putText(image, emotion, (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,255), 1)
        cv2.rectangle(image,(face_pos[0],face_pos[1]),(face_pos[2],face_pos[3]),(0,255,0),2) # face border
        # face_center and eyeline
        face_center = (int(face_pos[0] + face_pos[2])//2, int(face_pos[1] + face_pos[3])//2)
        emotion_server.add_eyeline(image, face_center, (face_pos[2]-face_pos[0], face_pos[3]-face_pos[1])) # add cross

    def showImg(image, emotion, face_pos, frame_time_ns):
        emotion_server.add_overlay(image, (10**9/frame_time_ns), frame_time_ns, emotion, face_pos)
        cv2.imshow('preview',image)
        cv2.waitKey(1)

    async def __connection_handler__(self, websocket, path):
        try:
            print(time.asctime(), "Client connected: %s"%'localhost')
            compute_timer = time_marker()
            fps_timer = time_marker()
            packet_wait_timer = time_marker()
            while True:
                # ================== Wait =================
                data = await websocket.recv()
                # ================ Profiling ==============
                packet_wait_time = packet_wait_timer.ellapsed_ms()
                compute_timer.mark()
                # ================ Process ================
                image = np.frombuffer(data, np.uint8)
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                emotions = emotion_server.emotion_predictor.image_to_emotion(image)
                emotion_json = json.dumps(emotions)
                # =========================================

                # =============== Profiling ===============
                compute_time_ns = compute_timer.ellapsed_ns()
                print(time.asctime(), "Data recieved: %d bytes"%len(data))
                print(time.asctime(), "Sending Response: %s"%emotion_json)
                frame_time_ns = fps_timer.ellapsed_ns()
                print("FPS: %d"%(10**9/frame_time_ns))
                print("Compute Time: %d ms (%d ns)    [avg: %d ms]"%(compute_time_ns/(10**6), compute_time_ns, compute_timer.average_ellapsed_ms()))
                print("Packet Wait Time: %d ms    [avg: %d ms]"%(packet_wait_time, packet_wait_timer.average_ellapsed_ms()))
                fps_timer.mark()
                # =========================================

                # =============== Preview =================
                if(emotion_server.show_preview is True):  
                    if(emotions[0] is True):
                        best_emotion = max(emotions[1], key=emotions[1].get)
                        face_pos = emotions[2]
                    else:
                        best_emotion = "No Face Detected"
                        face_pos = (0,0,1,1)
                    emotion_server.showImg(image, best_emotion, face_pos, frame_time_ns) # preview image
                # =========================================
                await websocket.send(emotion_json) # send response
                # =============== Profiling ===============
                packet_wait_timer.mark()
                # =========================================
        finally:
            print(time.asctime(), "Client disconnected: %s"%'localhost')
    
    def __init__(self, hostname='', port=8765, emotion_predictor=image_to_emotion()):
        self.server = Server(host=hostname, port=port, connection_handler=self.__connection_handler__)
        emotion_server.emotion_predictor = emotion_predictor

    def startServerLoop(self):
        self.server.startServer()
        self.server.serverForeverBlockingTick()

emotion_predictor = image_to_emotion(face_detector=cascade_face_detector())
emoserve = emotion_server(emotion_predictor=emotion_predictor)
emoserve.startServerLoop()