#!/usr/local/bin/python
import numpy as np
from copy import deepcopy

filename = "../../data/gcode/dino_body_sliced_perimeter_speed_120.gcode"
#f = open(filename)
#x = f.readlines()



''''remove non-extruded g-code points'''

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

	limit only to valid extrusion commands e.g. contains_e = True

	TODO: limit to only G1 linear commands, contains_g1 = True
	'''
	cmd_to_feature = {'G': 0, 'X': 1, 'Y': 2, 'Z': 3, 'E': 4, 'F': 5}
	curr_values = [0,0,0,0,0,0]
	for row,line in enumerate(x):
		sep_line = line.split("\n")[0].split("\n")[0].split(" ")
		line_cmds = []
		# extrusion boolean
		isValid = True
		for cmd in sep_line:
			cmd_char = str(cmd[0])
			cmd_value = float(cmd[1:])
			# skip command if not contained in dict
			if cmd_char not in cmd_to_feature.keys():
				isValid = False
				break
			# valid extrusion command
			#if cmd_char == "E":# and cmd_value != 0.0:
			#	contains_e = True
			ind_col = cmd_to_feature[cmd_char]
			curr_values[ind_col] = cmd_value
		if isValid:
			training_data[row] = curr_values
		else:
			training_data[row] = np.nan

	# remove nan rows
	training_data = remove_nan_rows(training_data)

	# limit to xyz
	#training_data = training_data[:,1:4]
	# remove duplicates
	#training_data = remove_duplicates(training_data)

	return training_data

def remove_duplicates(x):
	'''helper function: remove duplicate rows'''
	import pandas as pd
	df = pd.DataFrame(x)
	return df.drop_duplicates().values


def remove_starting_outline_points(x):
	'''
		TODO: better heuristic. right now we remove first ~40 points
	'''
	return x[40:]

def remove_nan_rows(x):
	'''helper function: remove nan rows'''
	num_cols = x.shape[1]
	return x[~np.isnan(x)].reshape(-1, num_cols)

def normalize_training_data(x):
	# convert G1 to +1 and G92 to -1
	x[:, 0][x[:, 0] == 92] = -1

	# normalize columns 1 to end by dividing by max
	x[:, 1:] = x[:, 1:] / np.max(x[:, 1:],axis=0)
	return x

##### augment dataset with linearly interpolated points between commands#########


##### helper functions ######
def compute_linear_fit(x, y):
    '''
    given x and y compute linear fit
    return m (slope) and c (intercept)
    '''
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    return m, c

def f(x, m, c):
    '''linear function eval'''
    return m * x + c

def linear_interpolate(x, y, delta=0.1):
    '''
    interpolate points on a line with delta=.1
    preserves order and includes endpoints
    '''
    m, c = compute_linear_fit(x, y)
    x_interp = constant_interpolate(x, delta)  
    y_interp = f(x_interp, m, c)
    return x_interp, y_interp

def constant_interpolate(x, delta=0.1):
    start = np.min(x)
    end = np.max(x)
    x_interp = np.append(np.arange(start, end, delta), end)
    # reverse order
    if start != x[0]:
        x_interp = x_interp[::-1]
    return x_interp

def augment_training_data(coordinates, delta=0.1):
	'''
	augment training data (coordinates) with linearly interpolated points between
	pairwise coordinates using delta size

	- compute linear interpolation for each pair ((x1,y1), (x2,y2)) if both x and y changes
	- compute constant delta-interpolation for x or y if other coordinate does not change
	- always append starting coordinate plus interpolation (excluding final coordinate)
	- if z-axis switches between coordinate pair, simply append first coordinate

	TODO: properly interpolate extrusion position. current extrusion interpolation values are held constant which is WRONG!
		solution: compute amount of material extruded / mm using extruder diameter.

	'''

	interpolated_coordinates = []
	for i in range(1, coordinates.shape[0]):
		# is coordinate pair in same plane
	    isWithinPlane = coordinates[i-1,3] == coordinates[i, 3]
	    # does first coordinate have non-zero extrusion
	    isExtrude = coordinates[i-1,4] != 0.0
	    # if within same plane and non-zero extrusion -> interpolate
	    if isWithinPlane and isExtrude:
	        x, y = coordinates[i-1:i+1, 1], coordinates[i-1:i+1, 2]
	        isXUnique, isYUnique = len(np.unique(x)) == len(x), len(np.unique(y)) == len(y)
	        # interpolate via linear fit
	        if isXUnique and isYUnique: 
	            x_interp, y_interp = linear_interpolate(x, y, delta)
	        # interpolate with constant delta
	        else:
	            if isXUnique:
	                x_interp = constant_interpolate(x, delta)
	                y_interp = np.repeat(y[0], len(x_interp))
	            else:
	                y_interp = constant_interpolate(y, delta) 
	                x_interp = np.repeat(x[0], len(y_interp))
	        num_interps = len(x_interp)
	        # append interpolated coordinates to list
	        interp_array = np.tile(coordinates[i], (num_interps, 1))
	        interp_array[:, 1] = x_interp
	        interp_array[:, 2] = y_interp
	        interpolated_coordinates.append(interp_array)
	        #interpolated_coordinates.append(np.vstack([x_interp, y_interp, coordinates[i, 3] * np.ones(len(x_interp))]).T)
	    
	    #else:
	    #    # append last point on previous plane
	    #    interpolated_coordinates.append(coordinates[i-1])
	# add last point
	#interpolated_coordinates.append(coordinates[-1])
	interpolated_coordinates = np.vstack(interpolated_coordinates)
	return interpolated_coordinates

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

run(filename)