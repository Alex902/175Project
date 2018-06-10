# This file contains functions for preprocessesing the data
# obtained from Assignments 1 and 3.

from collections import defaultdict
from PIL import Image
import random
import json
import os

def split_into_training_and_test():
	'''
	This function returns a dictionary. The keys in the dictionary
	will be the filenames of the images, and their associated values
	will be either a 0 (meaning that this particular image will be in the
	training set) or 1 (meaning that this particular image will be in
	the test set). 75% of the 57,207 images will be used for training, and 
	the remaining 25% will be used as test data. In order to split the images
	up into training and test sets, 1 out of every 4 images will be put into
	the test set while the other 3 will be put into the training set.
	'''
	to_return = {}
	iteration = 1
	num = random.randint(1, 4)
	for filename in os.listdir('Color'):
		if filename.endswith('.jpg'):
			if iteration == num:
				to_return[filename] = 1
			else:
				to_return[filename] = 0
			if iteration == 4:
				iteration = 1
				num = random.randint(1, 4)
			else:
				iteration += 1
	return to_return

def crop_images_and_place_into_train_and_test(train_and_test_split):
	'''
	This function crops the images in the 'Color' folder
	of the dataset that we downloaded from Canvas. 650
	pixels are chopped off from the left, 550 pixels are
	chopped off from the right, and 250 pixels are chopped
	off from the top (none chopped off from bottom). Each
	original 1920 by 1080 image is cropped to create a new
	720 by 830 image. The cropped image is then saved in
	either the 'Training_Set' directory or the 'Test_Set'
	directory (depending on which set that particular image
	was chosen to be placed into).
	'''
	os.makedirs('Training_Set')
	os.makedirs('Test_Set')
	for filename in os.listdir('Color'):
		if filename.endswith('.jpg'):
			image_obj = Image.open('Color/{}'.format(filename))
			cropped_image = image_obj.crop((650, 250, 1370, 1080))
			if train_and_test_split[filename] == 0:
				cropped_image.save('Training_Set/{}'.format(filename))
			elif train_and_test_split[filename] == 1:
				cropped_image.save('Test_Set/{}'.format(filename))

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

def update_annotations(train_and_test_split):
	'''
	This function creates brand new (updated) annotations files.
	Because we crop the images in the dataset, the dimensions of
	the images will be different. So we need to update the annotations
	to reflect the new dimensions of the images. This function also
	places the annotations for the training images in a separate file
	from the annotations for the test images.
	'''
	# open and load the original annotation file
	with open('annotation.json', 'r') as original_annotation_file:
		original_annotation = json.load(original_annotation_file)

	training_file = open('training_annotations.json', 'w')
	train_annotations = defaultdict(list)
	test_file = open('test_annotations.json', 'w')
	test_annotations = defaultdict(list)
	for annot in original_annotation:
		original_box = compute_bounding_box(original_annotation[annot])
		new_box = new_box = [original_box[0] - 250, original_box[1] - 650, original_box[2] - 250, original_box[3] - 650]
		key = '{}.jpg'.format(annot[:-2])
		if train_and_test_split[key] == 0:
			train_annotations[key].append(new_box)
		elif train_and_test_split[key] == 1:
			test_annotations[key].append(new_box)

	json.dump(train_annotations, training_file)
	json.dump(test_annotations, test_file)
	training_file.close()
	test_file.close()

if __name__ == '__main__':
	train_and_test_split = split_into_training_and_test()
	crop_images_and_place_into_train_and_test(train_and_test_split)
	update_annotations(train_and_test_split)
