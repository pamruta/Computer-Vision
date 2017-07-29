# simple video streaming in opencv
# Usage: stream.py [VIDEO-FILE]
# if no input is given video streaming will use the connected webcam

# importing packages
import cv2
import sys

# check if the video-file is provided via command-line
if len(sys.argv) != 2:
	cam = cv2.VideoCapture(0)
else:
	cam = cv2.VideoCapture(sys.argv[1])

while 1:
    frame = cam.read()[1]
    cv2.imshow('webcam', frame)
    if cv2.waitKey(1)&0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
