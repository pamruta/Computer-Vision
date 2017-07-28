# Usage: python train.py DIR_PATH

# importing required packages
import os
import re
import cv2
import sys
import numpy as np
from PIL import Image

# loading face recognizer
recognizer = cv2.createLBPHFaceRecognizer()
# loading face detector
detector = cv2.CascadeClassifier("/Users/pamruta/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

# path to training directory
path = sys.argv[1]

face_samples = []
face_labels = []

# assigning ids to each person
face_ids = {'amruta' : 0, 'pooja': 1, 'shirin': 2, 'swathi': 3, 'sunpriya': 4}

# processing each image in the training directory
for image_file in os.listdir(path):
	# extract person name from filename
	label, ext = re.split(r'\-', image_file)

	# loading the image
	pilImage = Image.open(os.path.join(path, image_file)).convert('L')
	image = np.array(pilImage, 'uint8')

	# marking boundary around each face detected
	faces = detector.detectMultiScale(image)
	for (x,y,w,h) in faces:
		face_samples.append(image[y:y+h, x:x+w])
		face_labels.append(face_ids[label])

# building a model from sample images
recognizer.train(face_samples, np.array(face_labels))

# saving the model file
recognizer.save('trained-model.yml')
