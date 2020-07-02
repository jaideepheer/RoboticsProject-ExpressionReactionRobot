import threading
import time
import pyttsx3
import random
from FeedbackHandler.sentence import sentences
class feedback_provider:
        def __init__(self, feedback_interval_sec=3):
                self.feedback_interval_sec = feedback_interval_sec
                self.emotions = []
                self.emoTickCount = 0
                # setup feedback thread
                self.feedback_thread = threading.Thread(target=self.feedback_tick)
                self.feedback_thread.setDaemon(True)
                self.feedback_thread.setName("feedback_provider_thread")
                # Run feedback tick loop
                self.isRunning = True
                self.feedback_thread.start()
        def emo_tick(self, emotion):
                if(isinstance(emotion, dict)):
                        self.emotions.append(emotion)
                self.emoTickCount += 1
        def get_appropriate_sentence(self, emotion):
                return random.choice(sentences[emotion])
        def get_feedback_sentence(self):
                feedback = "None"
                if(len(self.emotions)<=self.emoTickCount*0.5):
                        feedback = self.get_appropriate_sentence('no_face')
                else:
                        l = len(self.emotions)
                        ans = {}
                        for emo in self.emotions:
                                for (key,val) in emo.items():
                                        ans[key] = ans.get(key,0)+val/l
                        ans['neutral'] /= 2 # normalize
                        feedback = max(ans, key=ans.get)
                        feedback = self.get_appropriate_sentence(feedback)
                # clear emotions
                self.emotions.clear()
                self.emoTickCount = 0
                return feedback
        def feedback_tick(self):
                tts = pyttsx3.init()
                tts.setProperty('rate', 110)
                while self.isRunning:
                        # wait for defined interval
                        time.sleep(self.feedback_interval_sec)
                        # compute sentence
                        speech = self.get_feedback_sentence()
                        print("=========================================================================")
                        print(time.asctime(), "| Feedback:",speech)
                        print("=========================================================================")
                        # speak feedback
                        if(speech is ""):
                                speech = "Empty, sentence... error!"
                        tts.say(speech)
                        tts.runAndWait()
        def __del__(self):
                self.isRunning = False
                self.feedback_thread.join() # wait for thread to stop before delete
