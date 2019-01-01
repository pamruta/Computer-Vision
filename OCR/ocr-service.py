
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
from flask import request, render_template

app = flask.Flask(__name__)

# render home-page
@app.route("/")
def home():
	return render_template('upload.html')

# save user uploaded file
@app.route("/upload", methods=['GET', 'POST'])
def upload():

	from datetime import datetime
	import requests
	import os

	# saving the uploaded file
	if request.method == 'POST' and request.files['file']:
		file = request.files['file']
		extn = file.filename.rsplit('.')[1]

		# assign a unique name to uploaded file
		fname = datetime.now().strftime("%d%m%Y-%H%M%S")
		filename = fname + "." + extn
		filepath = "static/" + filename

		file.save(filepath)

		# get choice of OCR service
		if request.form['choice']:
			choice = request.form['choice']
		else:
			choice = "google-vision"

		response = "<img src=/" + filepath + " width=400 height=300 > <br>"
		# calling ocr-service
		url = "http://127.0.0.1:5000/ocr?file=" + filename + "&choice=" + choice
		ocr_response = requests.get(url)

		response += ocr_response.text
		return response
	else:
		return "Error in processing the request."

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
	ocr_result = run_ocr(choice, filename)

	return ocr_result

app.run(debug=True)
