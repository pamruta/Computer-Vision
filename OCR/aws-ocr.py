
# import AWS boto3 SDK

import boto3
client = boto3.client('rekognition')

# input file
import sys
image_file = sys.argv[1]

with open(image_file, "rb") as image:
	response = client.detect_text(Image = {'Bytes': image.read()})

# print OCR output
for text in response['TextDetections']:
	if text['Type'] == "LINE":
		print text['DetectedText']
