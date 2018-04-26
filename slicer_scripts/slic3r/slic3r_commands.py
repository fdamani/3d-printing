'''
This script sends commands to slic3r algorithm to generate g-code.

http://manual.slic3r.org/advanced/command-line

slic3r --help # returns a list of references

slic3r my_model.stl --output /path/to/output.gcode # slice a model into G-code with specified output folder

slic3r my_model.stl --load my_config.ini --fill-pattern concentric # load a config file and override individual options

slic3r model1.stl model2.stl model3.stl 

'''



# read in folder with stl files for slicing
folder_path = ""
stl_models = []
for model in folder_path:

	stl_models.append(model)




# read in config file
config_file = ""

param_settings = {} # key is command line arg; value is a list of values that we want that command to take on
keys = {"--perimeter-speed": [30, 60, 90, 120, 150], 