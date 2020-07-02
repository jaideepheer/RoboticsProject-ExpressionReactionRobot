import numpy as np
import cv2
import time
#import dlib
#from keras.preprocessing import image

#-----------------------------
#opencv initialization

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
#face_detector = dlib.get_frontal_face_detector()
modelFile = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
configFile = "deploy.prototxt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
fps = 0

while(True):
	ret, img = cap.read()
	fps = time.time()-fps
	cv2.putText(img, "FPS: %f"%(1/fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,30), 1)
	cv2.putText(img, "Frame Time: %f"%fps, (0, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (30,60,30), 1)
	fps = time.time()
	#print(img.shape)
	#img = cv2.imread('C:/Users/IS96273/Desktop/hababam.jpg')

	dnntime = time.clock()
	blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), [104, 117, 123], False, False)
	net.setInput(blob)
	detections = net.forward()
	#print("DNN Time:",time.clock()-dnntime)

	dnntime = time.clock()
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	#print("Cascade time:",time.clock()-dnntime)
	#detected_faces = face_detector(img)
	#face_frames = [(x.left(), x.top(), x.right(), x.bottom()) for x in detected_faces]

	#print(faces) #locations of detected faces

	dnntime = time.clock()
	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2) #draw rectangle to main image
		cv2.putText(img, "CV2 Haar", (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
	#for (left,top,right,bottom) in face_frames:
	#	cv2.rectangle(img,(left,top),(right,bottom),(0,255,0),2) #draw rectangle to main image
	#	cv2.putText(img, "DLib", (int(left), int(top)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 1)
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with the
		# prediction
		confidence = detections[0, 0, i, 2]
		if(confidence<.5):
			continue
		# compute the (x, y)-coordinates of the bounding box for the
		# object
		w = img.shape[1]
		h = img.shape[0]
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		(startX, startY, endX, endY) = box.astype("int")
		# draw the bounding box of the face along with the associated
		# probability
		text = "{:.2f}%".format(confidence * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(img, (startX, startY), (endX, endY),
			(0, 0, 255), 2)
		cv2.putText(img, text, (startX, y),
			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
	#print("DNN Box Time:",time.clock()-dnntime)
	cv2.imshow('img',img)

	if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
		break

#kill open cv things		
cap.release()
cv2.destroyAllWindows()