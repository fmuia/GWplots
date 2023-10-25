#app_dev.py

# Import all the relevant libraries and packages

from aux.imports import *
from aux.data_files import detector_data
from aux.aux_functions import load_data

# Load detector curves

for file_path, label in detector_data:
    globals()[label.replace(' ', '_')] = load_data(file_path, label)

print(BAW.x_coord)
print(LSD_weak)




# Load signal curves
