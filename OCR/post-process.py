
# python flask application to extract key-value pairs from plain-text output of OCR

# converts a given date-format into regular expression pattern
def make_date_regex(date_format):

	import re
	date_regex = date_format
	date_regex = re.sub(r'/', r'\/', date_regex)
	date_regex = re.sub(r'(dd|yy|mm)', r'\d\d', date_regex)
	return date_regex

# checks if the given date is valid
def valid_date(date_input, date_format):

	from datetime import datetime
	import re

	date_format = re.sub(r'dd', r'%d', date_format)
	date_format = re.sub(r'mm', r'%m', date_format)
	date_format = re.sub(r'yyyy', r'%Y', date_format)
	date_format = re.sub(r'yy', r'%y', date_format)

	try:
		date_ok = datetime.strptime(date_input, date_format)
		return 1
	except ValueError:
		return 0

# create flask app

import flask
from flask import request

app = flask.Flask(__name__)
@app.route("/extract", methods=['GET'])

# extracts key-value pairs from plain-text input 
# using the regex patterns defined in regex file

def post_process():

	# import packages
	import json
	import sys
	import re

	reload(sys)
	sys.setdefaultencoding('utf-8')

	# plain-text input
	if 'text' not in request.args:
		return "Please provide input text to parse."

	# regex file which defines key-value pairs to extract
	if 'regex' not in request.args:
		return "Please provide regex file to extract key-value pairs."

	# read text from input text file
	full_text = open(request.args['text'], "r").read()

	# load json file which defines the regex patterns
	regex_file = "regex/" + request.args['regex']
	regex_json = json.loads(open(regex_file, "r").read())

	# date format
	if 'global_date_format' in regex_json:
		global_date_format = regex_json['global_date_format']
	else:
		# use mm/dd/yyyy as default date format
		global_date_format = "mm/dd/yyyy"

	json_output = "{\n"

	for regex_entry in regex_json['regexes']:
		pattern = ""
		validate_date = 0
		# generate date regex based on the given date format
		if 'data_type' in regex_entry and regex_entry['data_type'] == "DATE":
			pattern = make_date_regex(global_date_format)
			validate_date = 1

		# regex pattern to match
		if 'match_regex' in regex_entry:
			pattern = regex_entry['match_regex']
	
		# field names that match this pattern
		if 'field_name' not in regex_entry:
			return "Field name is missing in regex file.."

		# text to strip from matching text patterns
		if 'strip_expr' in regex_entry:
			strip_expr = regex_entry['strip_expr']
		else:
			strip_expr = ""

		# find all matching texts
		for matching_text in re.findall(pattern, full_text):
			# skip the matched text if it appears in no_match list
			if 'no_match' in regex_entry and matching_text in regex_entry['no_match']:
				continue

			# create attribute-value pair
			if len(regex_entry['field_name']) <= 0:
				return "More matching patterns found than given field-names."

			attr_name = regex_entry['field_name'].pop(0)
			attr_value = re.sub(strip_expr, r'', matching_text)

			# if validate_date flag is 1 then attr_value must be a valid date string
			if validate_date == 1 and not valid_date(attr_value, global_date_format):
				response = "Date " + attr_value + " doesn't match the given date-format " + global_date_format + ".."
				return response

			json_output += "\t\"" + attr_name + "\": \"" + attr_value + "\",\n"

		# no matching patterns found for some fields
		while len(regex_entry['field_name']) > 0:
			attr_name = regex_entry['field_name'].pop(0)
			json_output += "\t\"" + attr_name + "\": \"NONE\",\n" 

	json_output += "\t\"Status\": \"OK\"\n"
	json_output += "}\n"

	return json_output

app.run(host='127.0.0.1', port='3000', debug=True)
