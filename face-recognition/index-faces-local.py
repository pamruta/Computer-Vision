
# indexes faces from the images found in 'ref_faces' directory

from pprint import pprint

# adds reference image to image collection
def add_ref_image(image_file):
	import boto3
	client = boto3.client('rekognition')

	import re
	actor_name = re.sub(r'\.(jpeg|jpg|png)', r'', image_file)
	actor_name = re.sub(r'ref_faces\/', r'', actor_name)
	with open(image_file, "rb") as image:
		response = client.index_faces(CollectionId='friends', Image={'Bytes': image.read()}, DetectionAttributes=['ALL'], ExternalImageId=actor_name)
		pprint(response)

# traverse the 'ref_faces' directory and add images to the face-collection
import os
for dir, sub_dir, files in os.walk('ref_faces'):
	for fname in files:
		image_file = "ref_faces/" + fname
		add_ref_image(image_file)
