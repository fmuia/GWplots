#app_dev.py

# Import all the relevant libraries and packages

from aux.imports import *
from aux.data_files import detector_data
from aux.aux_functions import load_data
from aux.aux_functions import create_sliders

# Load detector curves

for file_path, label in detector_data:
    globals()[label.replace(' ', '_')] = load_data(file_path, label)

print(BAW.x_coord)
print(LSD_weak)




# Load signal curves






# Set up the figure

hmin = 10.**-35.
hmax = 10.**-10.
xrange=(10**-18, 10**20)
fig = figure(background_fill_color='white',
             border_fill_color='black',
             border_fill_alpha=0.0,
             height=600,
             width=int(1.61803398875*600),
             x_axis_label='frequency (Hz)',
             x_axis_type='log',
             x_axis_location='below',
             x_range=xrange,
             y_axis_label='h',
             y_axis_type='log',
             y_axis_location='left',
             y_range=(hmin, hmax),
             title='Gravitational waves plotter',
             title_location='above',
             toolbar_location='below',
             tools='save')
fig.output_backend = "svg"

# Set up the sliders

slider_x, slider_y, slider_width, slider_height = create_sliders(fig)

print(slider_x)
