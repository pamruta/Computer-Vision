
# recognizes face in the given input image
# by comparing it against a face collection 

import sys
if len(sys.argv) < 3:
	print "Usage: recognize-face.py IMAGE COLLECTION"
	exit(1)

image_file = sys.argv[1]
collection = sys.argv[2]

import boto3
client = boto3.client('rekognition')
with open(image_file, 'rb') as image:
	result = client.search_faces_by_image(CollectionId=collection, Image={'Bytes': image.read()}, MaxFaces = 1, FaceMatchThreshold = 70)
	if len(result['FaceMatches']) == 0:
		print "NULL"
	else:
		print result['FaceMatches'][0]['Face']['ExternalImageId']
