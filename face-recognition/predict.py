# import opencv library
import cv2
import numpy as np

# loading the trained model 
recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load("trained-model.yml")

# face detection with haarcascades
face_cascade = cv2.CascadeClassifier('/Users/pamruta/opencv/data/haarcascades/haarcascade_frontalface_default.xml')

# check if the video file is provided as command-line argument
import sys
if len(sys.argv) == 2:
	cam = cv2.VideoCapture(sys.argv[1])
# otherwise, capture video from live webcam
else:
	cam = cv2.VideoCapture(0)

# array of names to be identified
face_ids = ['amruta', 'pooja', 'shirin', 'swathi', 'sunpriya']

while 1:

    # capture frame
    frame = cam.read()[1]

    # convert to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # apply face detection
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # identify the person
    for (x, y, w, h) in faces:
	id, conf = recognizer.predict(gray[y:y+h,x:x+w])
	label = face_ids[id]
	text = label + " [conf = " + str(conf) + "]"
	cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)
	cv2.putText(frame, text, (x, y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # show output
    cv2.imshow('webcam', frame)

    # halt on keypress 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
