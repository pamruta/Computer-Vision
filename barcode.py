# Barcode Scanner using Python Zbar library
# Usage: barcode.py IMAGE-FILE
# Example: python ./barcode.py samples/barcode.png

# importing various libraries

import zbar
from PIL import Image
import sys
import requests
import json

# handling UTF-8 encoded characters
reload(sys)
sys.setdefaultencoding('UTF-8')

# loading the image-file
pil = Image.open(sys.argv[1]).convert('L')
width, height = pil.size
raw = pil.tobytes()
image = zbar.Image(width, height, 'Y800', raw)

# scanning image with zbar
scanner = zbar.ImageScanner()
scanner.parse_config('enable')
scanner.scan(image)

web_url = ""
for symbol in image:
	# print the barcode
	code_type = str(symbol.type)
	barcode = str(symbol.data)
	print '[Code_Type =', code_type, ', Code =', barcode, ']'

	# fetching the product name
	base_url = "https://www.upccodesearch.com/api/v1/"
	if(code_type == "UPCA" or code_type == "UPCE"):
		web_url = base_url + "upc/" + barcode
	elif(code_type == "EAN13" or code_type == "EAN8"):
		web_url = base_url + "ean/" + barcode
	else:
		print "ERROR: Can't process barcodes of type = ", code_type

	if web_url != "":
		response = requests.get(web_url)
		json_output = json.loads(response.content)
		# product found
		if 'item' in json_output:
			print "Title = ", json_output['item']['title']
		# print error message
		else:
			print "Error = ", json_output['message']
del(image)
