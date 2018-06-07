# This file contains functions for preprocessesing the data
# obtained from Assignments 1 and 3.

from collections import defaultdict
from PIL import Image
import json
import os

def crop_images():
	'''
	This function crops the images in the 'Color' folder
	of the dataset that we downloaded from Canvas. 650
	pixels are chopped off from the left, 550 pixels are
	chopped off from the right, and 250 pixels are chopped
	off from the top (none chopped off from bottom). Each
	original 1920 by 1080 image is cropped to create a new
	720 by 830 image. Each new (cropped) image will be placed
	in a directory named 'Cropped_Images'.
	'''	
	for filename in os.listdir('Color'):
		if filename.endswith('.jpg'):
			image_obj = Image.open('Color/{}'.format(filename))
			cropped_image = image_obj.crop((650, 250, 1370, 1080))
			cropped_image.save('Cropped_Images/{}'.format(filename))

def compute_bounding_box(list_of_joint_positions):
	'''
	This function takes a list_of_joint_positions as an argument
	and returns a 4 element list containing the coordinates for
	the bounding box around the hand. The list that is returned
	is of the following format: [ymin, xmin, ymax, xmax].
	'''
	min_x = list_of_joint_positions[0][0]
	max_x = list_of_joint_positions[0][0]
	min_y = list_of_joint_positions[0][1]
	max_y = list_of_joint_positions[0][1]

	for inner_list in list_of_joint_positions:
		if inner_list[0] < min_x:
			min_x = inner_list[0]
		if inner_list[0] > max_x:
			max_x = inner_list[0]
		if inner_list[1] < min_y:
			min_y = inner_list[1]
		if inner_list[1] > max_y:
			max_y = inner_list[1]

	return [min_y - 10, min_x - 10, max_y + 10, max_x + 10]

def update_annotations():
	'''
	This function creates a brand new (updated) annotations file.
	Because we will crop the images in the dataset, the dimensions of
	the images will be different. So we need to update the annotations
	to reflect the new dimensions of the images.
	'''
	# open and load the original annotation file
	with open('annotation.json', 'r') as original_annotation_file:
		original_annotation = json.load(original_annotation_file)

	new_annotation_file = open('updated_annotation.json', 'w')
	new_annotation = defaultdict(list)
	for annot in original_annotation:
		original_box = compute_bounding_box(original_annotation[annot])
		new_box = [original_box[0] - 250, original_box[1] - 650, original_box[2] - 250, original_box[3] - 650]
		key = '{}.jpg'.format(annot[:-2])
		new_annotation[key].append(new_box)

	json.dump(new_annotation, new_annotation_file)
	new_annotation_file.close()

if __name__ == '__main__':
	#crop_images() DONE
	#update_annotations() DONE
