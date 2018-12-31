
# import required libraries

import pytesseract
from PIL import Image

# input file
import sys
filename = sys.argv[1]

result = pytesseract.image_to_string(Image.open(filename))
for text in result.split("\n"):
	if text.strip():
		print text

