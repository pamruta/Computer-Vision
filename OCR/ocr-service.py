
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
				result = result + "\n" + text['DetectedText'] 
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
		result = ""
		for text in ocr_output.full_text_annotation.text.split("\n"):
			# skipping foreign language text for now
			if all(ord(char) < 128 for char in text):
				result += text + "\n"

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
			result = result + "\n" + text 

	return result

# create flask app

import flask
from flask import request, render_template

app = flask.Flask(__name__)

@app.route("/")
def home():
	# nothing to show here..
	return "To run OCR, use: 127.0.0.1/ocr?file=FILE_NAME"

# runs OCR service with given parameters
@app.route("/ocr", methods=['GET'])
def ocr():
	# there are many options to run OCR, here are few choices
	available_choices = ['aws', 'google-vision', 'tesseract', 'datacap', 'iris']

	# if no choice is given, using google-vision by default
	if 'choice' not in request.args:
		choice = "google-vision"
	else:
		choice = request.args['choice']

		# check if the choice is valid
		if choice not in available_choices:
			response = "Please select choice from: " + str(available_choices)
			return response

	# input file
	if 'file' not in request.args:
		response = "Please provide the input file to run OCR."
		return response

	filename = "static/" + request.args['file']
	ocr_result = run_ocr(choice, filename)

	# return output in plain-text format
	if 'json' not in request.args:
		return ocr_result
	else:
		# extract key-value pairs from text
		regex_file = request.args['json']

		# write OCR output to text-file
		from datetime import datetime
                fname = "ocr-output-" + datetime.now().strftime("%d%m%Y-%H%M%S") + ".txt"
		open(fname, "w").write(ocr_result)

		import requests
		url = "http://127.0.0.1:3000/extract?text=" + fname + "&regex=" + regex_file
		json_output = requests.get(url)
		return json_output.text

app.run(debug=True)
