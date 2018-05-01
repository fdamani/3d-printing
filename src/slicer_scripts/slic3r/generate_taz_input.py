'''
This script takes as input slic3r g-code, start and end boilerplate taz 6 g-code
Performs following ops:
1. Parses taz 6 boilerplate code and specifies proper temperature settings depending on filament.
'''


# args parse
# arg 1 is slic3r g-code
# read in boilerplate start and end-gcode
# given extrusion and bed temperature specified 