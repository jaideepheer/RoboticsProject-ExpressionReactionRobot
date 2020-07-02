from config import resources
from extract_face import face_extractor_dnn, face_extractor_cascade
from extract_emotion import emotion_extractor_sarengil, emotion_extractor_oarriaga

# ================================================================
#                       DEFAULT DETECTORS
# ================================================================

def dnn_face_detector():
    return face_extractor_dnn(
        dnnConfigFile=resources['facedetect_dnnmodel_structure'],
        dnnModelFile=resources['facedetect_dnnmodel_weights'],
        confidenceThreshold=.4
        )
def cascade_face_detector():
    print("Cascade: ",resources['facedetect_haarcascade_frontalface'])
    return face_extractor_cascade(
        cascadeXMLFilePath=resources['facedetect_haarcascade_frontalface']
    )

def default_emotion_detector():
    return emotion_extractor_oarriaga(kerasModelPath=resources['emotiondetect_oarriaga_107'])
    #return emotion_extractor_sarengil(
    #    kerasModelPath=resources['emotiondetect_sarengil_structure'],
    #    kerasModelWeightsPath=resources['emotiondetect_sarengil_weights']
    #    )

# ================================================================

class image_to_emotion:
    def __init__(self, face_detector=dnn_face_detector(), emotion_detector=default_emotion_detector()):
        self.face_detector = face_detector
        self.emotion_detector = emotion_detector
    
    def image_to_emotion(self, imageArray):
        # define return tupple vars
        returnVals = () # (face_detected, {'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'})
        # check if image 3ch.
        height, width, channels = imageArray.shape[0:3]
        assert channels == 3 # image must be 3ch.
        # get face box
        (lx,ly,ux,uy) = self.face_detector.getFaceBoxLocation(imageArray)
        # check correct face box
        if(lx|ly|ux|uy > 0 and lx<ux and ly<uy):
            returnVals += (True,) # face_detected = True
            imageArray = imageArray[ly:uy, lx:ux] # crop image
            emotions = self.emotion_detector.getFaceEmotion(imageArray) # get emotions
            returnVals += (emotions,)
            returnVals += ((int(lx), int(ly), int(ux), int(uy)),) # add face pos. info
        else:
            # no face detected
            returnVals += (False,)
        return returnVals
