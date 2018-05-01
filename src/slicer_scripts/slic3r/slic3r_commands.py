'''
This script sends commands to slic3r algorithm to generate g-code.

http://manual.slic3r.org/advanced/command-line

slic3r --help # returns a list of references

slic3r my_model.stl --output /path/to/output.gcode # slice a model into G-code with specified output folder

slic3r my_model.stl --load my_config.ini --fill-pattern concentric # load a config file and override individual options

slic3r model1.stl model2.stl model3.stl 



slic3r data/stl/dino_body_sliced.stl \
	--load slicer_scripts/slic3r/taz-6/taz_configs/medium_ABS_no-support_pt35nzl_pt22layer.ini \
	--start-gcode slicer_scripts/slic3r/taz-6/start_code_abs.gcode \
	--end-gcode slicer_scripts/slic3r/taz-6/end_code_abs.gcode \
	--perimeter-speed 30 \
	--output data/gcode/dino_body_sliced_perimeter_speed_30.gcode
'''

# read in folder with stl files for slicing
folder_path = ""
stl_models = []
for model in folder_path:

	stl_models.append(model)




# read in config file
config_file = ""

speeds = [30, 60, 90, 120, 150]
min_cand_speeds = [60, 120]
heights = [0.1, 0.2, 0.3, 0.4]
candidate_param_settings = {"--perimeter-speed": min_cand_speeds, # default = 60
		"--infill-speed": speeds, # defualt = 80
		"--first-layer-speed": speeds, # default = 30
		"layer-height": heights # default = 0.3
		"solid-infill-every-layers": [0,2,4,6] # default = 0
		}

param_settings = candidate_param_settings["--perimeter-speed"]


# for each config (in this case two speeds)
	# run slicer command for everythingd
