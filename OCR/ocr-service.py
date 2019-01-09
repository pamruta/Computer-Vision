
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
		result = ocr_output.full_text_annotation.text

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

# create python flask app

import flask
from flask import request

app = flask.Flask(__name__)

# runs OCR service on input files uploaded from local disk
@app.route("/upload", methods=['POST'])
def upload():

	# import required libraries
	from datetime import datetime
	import requests

	url = "http://127.0.0.1:5000/ocr?"

	# input image
	if 'image' not in request.files:
		response = "Please provide the input file to run OCR."
		return response

	file = request.files['image']

	# get file extension
	extn = file.filename.rsplit(".")[1]

	# create unique file name
	file_name = "image-" + datetime.now().strftime("%d%m%Y-%H%M%S") + "." + extn

	# save file in static directory for further processing
	file_path = "static/" + file_name
	file.save(file_path)

	# pass file as input parameter 
	url += "image=" + file_name

	# choice of OCR service
	if 'choice' in request.args:
		url += "&choice=" + request.args['choice']

	# json file to extract key-value pairs 
	if 'json' in request.files:
		regex_file = request.files['json']

		# create unique file name
		regex_name = "regex-" + datetime.now().strftime("%d%m%Y-%H%M%S") + ".json"
		regex_path = "regex/" + regex_name
		regex_file.save(regex_path)

		# pass regex file as input parameter
		url += "&json=" + regex_name

	# send API request
	response = requests.get(url)
	return response.text


# runs OCR service with given parameters
@app.route("/ocr", methods=['GET'])
def ocr():

	# handling utf-8 encodings
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')

	# there are many options to run OCR, here are few choices
	available_choices = ['aws', 'google-vision', 'tesseract', 'datacap', 'kofax']

	# if no choice is given, use google-vision by default
	if 'choice' not in request.args:
		choice = "google-vision"
	else:
		choice = request.args['choice']

		# check if the choice is valid
		if choice not in available_choices:
			response = "Please select choice from: " + str(available_choices)
			return response

	# input image
	if 'image' not in request.args:
		response = "Please provide the input file to run OCR."
		return response

	input_file = "static/" + request.args['image']
	ocr_result = run_ocr(choice, input_file)

	# return output in plain-text format
	if 'json' not in request.args:
		return ocr_result
	else:
		# extract key-value pairs from text
		regex_file = request.args['json']

		from datetime import datetime

		# write OCR output to text-file
                ocr_text = "ocr-text-" + datetime.now().strftime("%d%m%Y-%H%M%S") + ".txt"
		ocr_path = "output/" + ocr_text
		open(ocr_path, "w").write(ocr_result)

		import requests
		url = "http://127.0.0.1:3000/extract?text=" + ocr_text + "&regex=" + regex_file
		json_output = requests.get(url)
		return json_output.text

app.run(debug=True)
