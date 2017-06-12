# implements optical character recognition (OCR)
# to extract text from images 
# using Google's Cloud Vision API

# Usage: ocr.py IMAGE-FILE

# importing libraries
import io
import sys

# importing google cloud-vision library
from google.cloud import vision

vision_client = vision.Client()

# read image file
with io.open(sys.argv[1], 'rb') as image_file:
	content = image_file.read()

image = vision_client.image(content = content)

texts = image.detect_text()

for text in texts:
	label = text.description
	break

print label
