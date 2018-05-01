;This profile is designed specifically for LulzBot TAZ 6 3D Printer
;Basic slice data:
;Sliced at: {day} {date} {time}
;Layer height: {layer_height}
;Walls: {wall_thickness}
;Fill: {fill_density}
;Estimated Print time: {print_time}
;Filament used: {filament_amount}m {filament_weight}g
;Filament cost: {filament_cost}
;Variables to replace: print_bed_temperature, print_temperature, clean_temperature
G26                          ; clear potential 'probe fail' condition
G21                          ; set units to Millimeters
M107                         ; disable fans
G90                          ; absolute positioning
M82                          ; set extruder to absolute mode
G92 E0                       ; set extruder position to 0
M140 S85					 ; get bed heating up
G28 XY                       ; home X and Y
G1 X-19 Y258 F1000           ; move to safe homing position
M109 S161    				 ; soften filament for z homing, 70% of extrusion temperature is fine. default=170. 
G28 Z                        ; home Z
M104 S161    				 ; wipe temp, 70% of extrusion temperature is fine. default=160
G1 E-30 F100                 ; suck up XXmm of filament
G1 X-15 Y100 F3000           ; move above wiper pad
G1 Z1                        ; push nozzle into wiper
G1 X-17 Y95 F1000            ; slow wipe
G1 X-17 Y90 F1000            ; slow wipe
G1 X-17 Y85 F1000            ; slow wipe
G1 X-15 Y90 F1000            ; slow wipe
G1 X-17 Y80 F1000            ; slow wipe
G1 X-15 Y95 F1000            ; slow wipe
G1 X-17 Y75 F2000            ; fast wipe
G1 X-15 Y65 F2000            ; fast wipe
G1 X-17 Y70 F2000            ; fast wipe
G1 X-15 Y60 F2000            ; fast wipe
G1 X-17 Y55 F2000            ; fast wipe
G1 X-15 Y50 F2000            ; fast wipe
G1 X-17 Y40 F2000            ; fast wipe
G1 X-15 Y45 F2000            ; fast wipe
G1 X-17 Y35 F2000            ; fast wipe
G1 X-15 Y40 F2000            ; fast wipe
G1 X-17 Y70 F2000            ; fast wipe
G1 X-15 Y30 Z2 F2000         ; fast wipe
G1 X-17 Y35 F2000            ; fast wipe
G1 X-15 Y25 F2000            ; fast wipe
G1 X-17 Y30 F2000            ; fast wipe
G1 X-15 Y25 Z1.5 F1000       ; slow wipe
G1 X-17 Y23 F1000            ; slow wipe
G1 Z10                       ; raise extruder
M109 S161				     ; heat to probe temp. probe temp is 70% of extrusion temperature (print_temperature). default=160
G1 X-9 Y-9                   ; move above probe
M204 S100                    ; set accel for probing
G29                          ; probe sequence (for auto-leveling)
M204 S500                    ; set accel back to normal
G1 X0 Y0 Z15 F5000           ; get out the way
M400                         ; clear buffer
G4 S1                        ; pause
M117 Heating...              ; LCD status message
M140 S85					 ; get bed heating up
M109 S230				     ; set extruder temp and wait
M190 S85					 ; get bed temping up during first layer
G1 Z2 E0 F75                 ; extrude filament back into nozzle
M117 TAZ Printing...         ; LCD status message