
# indexes faces from the images stored in s3 photo-bucket

from pprint import pprint

# adds reference image to image collection
def add_ref_image(image_file):
	import boto3
	client = boto3.client('rekognition')

	import re
	actor_name = re.sub(r'\.(jpeg|jpg|png)', r'', image_file)
	response = client.index_faces(CollectionId='friends-s3', Image={'S3Object': {'Bucket': 'pamruta-photo-bucket', 'Name': image_file}}, DetectionAttributes=['ALL'], ExternalImageId=actor_name)
	pprint(response)

for fname in ["jennifer_aniston", "courtney_cox", 'lisa_kudrow', 'matthew_perry', 'matt_leblanc', 'david_schwimmer']:
	image_file = fname + ".jpg"
	add_ref_image(image_file)
