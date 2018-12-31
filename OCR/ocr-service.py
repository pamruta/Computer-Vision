

# function to run OCR on a given input file
# using the selected choice of service
def run_ocr(choice, filename):

	if choice == "aws":
		result = run_aws(filename)

	elif choice == "google-vision":
		result = run_google(filename)

	elif choice == "tesseract":
		result = run_tesseract(filename)
	else:
		result = "Choice " + choice + " not supported."

	return result

# run OCR using aws
def run_aws(filename):

	# import AWS boto3 SDK
	import boto3
	client = boto3.client('rekognition')

	result = ""
	with open(filename, "rb") as image:
		ocr_output = client.detect_text(Image = {'Bytes': image.read()})
		for text in ocr_output['TextDetections']:
			if text['Type'] == "LINE":
				result = result + "<br>" + text['DetectedText']
	return result

# run OCR using google-vision
def run_google(filename):

	# import google vision sdk

	from google.cloud import vision
	client = vision.ImageAnnotatorClient()

	result = ""
	with open(filename, "rb") as image:
		image_object = vision.types.Image(content=image.read())
		ocr_output = client.document_text_detection(image=image_object)
		import re
		result = re.sub(r'\n', r'<br>', ocr_output.full_text_annotation.text)

	return result

# run OCR using tesseract
def run_tesseract(filename):

	# import required packages
	import pytesseract
	from PIL import Image

	result = ""

	ocr_output = pytesseract.image_to_string(Image.open(filename))
	for text in ocr_output.split("\n"):
		# omit blank lines
		if text.strip():
			result = result + "<br>" + text

	return result

# importing flask

import flask
from flask import request

app = flask.Flask(__name__)
@app.route("/")

def home():
	return "Nothing to show here. Try /ocr "

@app.route("/ocr", methods=['GET'])
def ocr():
	# there are many options to run OCR, here are few choices
	available_choices = ['aws', 'google-vision', 'tesseract', 'datacap', 'iris']

	if 'choice' not in request.args:
		response = "Please select your choice from: " + str(available_choices)
                return response

	choice = request.args['choice']
	if choice not in available_choices:
		response = "Please select your choice from: " + str(available_choices)
		return response

	# input file
	if 'file' not in request.args:
		response = "Please provide the input file to run OCR."
		return response

	filename = "static/" + request.args['file']
	response = "Running OCR using " + choice + " service on input file " + filename + "<br><br>"

	response += "<img src=/" + filename + " width=400 height=300> <br>"
	result = run_ocr(choice, filename)
	response += result

	return response

app.run(debug=True)
