
# import google vision

from google.cloud import vision

client = vision.ImageAnnotatorClient()

# input image to parse
import sys
image_file = sys.argv[1]

with open(image_file, "rb") as image:
	image_object = vision.types.Image(content=image.read())
	response = client.document_text_detection(image=image_object)

	#print response.full_text_annotation.text
	text = response.text_annotations[0].description
	print text
