#!/usr/local/bin/python
import numpy as np
from copy import deepcopy

#filename = "../../data/gcode/dino_body_sliced_perimeter_speed_120.gcode"
#f = open(filename)
#x = f.readlines()

def cut_header(x):
	'''
	Returns starting index for linear commands.
	NOTE: this applies to slic3r + taz6 boilerplate format. linear commands start with 3rd "G92 E0".
	'''
	counter = 0
	for i,line in enumerate(x):
		split_line = line.split("\n")
		if str.startswith(split_line[0], "G92 E0"):
			counter = counter + 1
			if counter == 3: # if third instance
				return i

def cut_footer(x):
	'''
	Return index for end of linear commands.
	NOTE: this applies to slic3r + taz6 boilerplate format. heuristic: find index for second M400 command.
	'''
	counter = 0
	for i,line in enumerate(x):
		split_line = line.split("\n")
		if str.startswith(split_line[0], "M400"):
			counter = counter + 1
			if counter == 2: # if second instance
				return i-1

def gcode_to_training_data(x, training_data):
	'''
	Convert gcode to training data format:
	
	G1/G92 X Y Z E F
	1/0 float float float float float

	if line does not specify a value for variable X, use X's last seen value.
	'''
	cmd_to_feature = {'G': 0, 'X': 1, 'Y': 2, 'Z': 3, 'E': 4, 'F': 5}
	curr_values = [0,0,0,0,0,0]
	for row,line in enumerate(x):
		sep_line = line.split("\n")[0].split("\n")[0].split(" ")
		line_cmds = []
		for cmd in sep_line:
			col = cmd_to_feature[cmd[0]]
			value = cmd[1:]
			curr_values[col] = value
		training_data[row] = curr_values
	return training_data


def normalize_training_data(x):
	# convert G1 to +1 and G92 to -1
	x[:, 0][x[:, 0] == 92] = -1

	# normalize columns 1 to end by dividing by max
	x[:, 1:] = x[:, 1:] / np.max(x[:, 1:],axis=0)
	return x

def run(filename):
	f = open(filename)
	x = f.readlines()

	start_ind = cut_header(x)
	end_ind = cut_footer(x)
	num_commands = end_ind - start_ind

	training_data = np.zeros((num_commands, 6))
	x_trimmed = x[start_ind: end_ind]

	train_raw = gcode_to_training_data(x_trimmed, training_data)

	train = normalize_training_data(deepcopy(train_raw))

	return train, train_raw