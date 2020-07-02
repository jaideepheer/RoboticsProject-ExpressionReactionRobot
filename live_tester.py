# ============================================================
# TFgpu workaround
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
# ============================================================
from image_to_emotion import image_to_emotion, cascade_face_detector, dnn_face_detector
from FPS_helper import time_marker
import cv2
import time

def handle_keyboard_input(quit_key='q', pause_key=' '):
    keyPress = cv2.waitKey(1) & 0xFF
    if keyPress == ord(quit_key): #press quit_key to quit
        return True
    elif keyPress == ord(pause_key):
        print("Paused...")
        keyPress = 0
        while(keyPress != ord(pause_key)):
            keyPress = cv2.waitKey(0) & 0xFF
            if(keyPress == ord(quit_key)):
                print("Exiting...!")
                exit()
        print("Resumed...")
    return False

def add_eyeline(image, face_center, face_size, size=5, thickness=2):
    print("face_size: ",face_size)
    x, y = face_center
    # face center
    cv2.line(image, (x-size, y), (x+size, y), (0,255,0), thickness)
    cv2.line(image, (x, y-size), (x, y+size), (0,255,0), thickness)
    # eyeline
    eye_fromcenter_ratio = 0.2
    eye_height = int(y - (face_size[1]/2)*eye_fromcenter_ratio)
    print("y:",y,", eyeheight:",eye_height)
    cv2.line(image, (x-size, eye_height), (x+size, eye_height), (10,10,255), thickness+1)

def add_overlay(image, face_detected, face_pos, best_emotion, fps, frame_time):
    height, width = image.shape[0:2]
    if(face_detected):
        cv2.putText(image, best_emotion, (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,255), 1)
        cv2.rectangle(image,(face_pos[0],face_pos[1]),(face_pos[2],face_pos[3]),(0,255,0),2) # face border
        face_center = (int(face_pos[0] + face_pos[2])//2, int(face_pos[1] + face_pos[3])//2)
        add_eyeline(image, face_center, (face_pos[2]-face_pos[0], face_pos[3]-face_pos[1])) # add cross
    else:
        cv2.putText(image, "No Face detected. %d %d"%(width,height), (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,255), 1)
    cv2.putText(image, "FPS: %f"%fps, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,30), 1)
    cv2.putText(image, "Frame Time: %fms"%frame_time, (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,30), 1)


def live_tester(feedback_handler):
    fps = time_marker()
    stream = cv2.VideoCapture(0)
    im2emo = image_to_emotion(face_detector=cascade_face_detector())
    while(True):
        ret, img = stream.read()
        height, width = img.shape[0:2]
        fps.mark()
        retVal = im2emo.image_to_emotion(img)
        bestEmo = 'none'
        emotions = 'none'
        if(retVal[0]==True):
            # face detected
            emotions = retVal[1]
            bestEmo = max(emotions, key=emotions.get)
            print("\nFace pos.:", retVal[2])
            #print("Emotions:",emotions)
            #print("Best Emotion:", bestEmo)
        else:
            retVal += (0,0,)

        feedback_handler.emo_tick(emotions) # feedback

        add_overlay(img, retVal[0], retVal[2], bestEmo, (1/fps.ellapsed_sec()), fps.ellapsed_ms())
        cv2.imshow('img',img)
        if(handle_keyboard_input()):
            break

import Client.FeedbackHandler.feedback_handler as FeedBack
live_tester(FeedBack.feedback_provider())