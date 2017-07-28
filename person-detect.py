# import opencv library
import cv2

# real-time person detection with hog-cascade
hog_cascade = cv2.CascadeClassifier('/Users/pamruta/opencv/data/hogcascades/hogcascade_pedestrians.xml')

# check if video file is provided as command-line argument
import sys
if len(sys.argv) == 2:
	cam = cv2.VideoCapture(sys.argv[1])
# capture video from live webcam
else:
	cam = cv2.VideoCapture(0)

while 1:
    # capture frame from video
    frame = cam.read()[1]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # apply person detection algorithm
    people = hog_cascade.detectMultiScale(gray, 1.3, 5)

    # draw rectangle around each person detected in the video frame
    for (x, y, w, h) in people:
	cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 255, 0), 2)

    # show output
    cv2.imshow('webcam', frame)

    # halt on keypress
    if cv2.waitKey(1)&0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
