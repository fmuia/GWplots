# aux_functions.py
import numpy as np
from bokeh.models import RangeSlider, CustomJSTickFormatter, CustomJS, Slider

class Data:
    def __init__(self, x_coord, y_coord, label, category=None):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.label = label
        self.category = category
        if len(x_coord) != len(y_coord):
            raise Warning("x_coord and y_coord have different dimensions")

    def load_data(file_path, label, category):  # Update function signature to accept category
        data = np.loadtxt(file_path, delimiter=',', dtype=float)
        x_coord, y_coord = data[:, 0], data[:, 1]
        return Data(x_coord, y_coord, label, category)  # Pass the category to Data initialization

def load_and_categorize_data(detector_data):
    data_instances = {}
    category_dict = {
        'IndBounds': [],
        'DirBounds': [],
        'ProjBounds': [],
        'Detectors': []
    }

    for file_path, label, category in detector_data:
        data_instances[label] = Data.load_data(file_path, label, category)

        if category == 'Indirect bound':
            category_dict['IndBounds'].append(label)
        elif category == 'Direct bound':
            category_dict['DirBounds'].append(label)
        elif category == 'Projected bound':
            category_dict['ProjBounds'].append(label)
        
        category_dict['Detectors'].append(label)
    
    return data_instances, category_dict

# Create plot sliders

def create_sliders(fig):
    range_slider_x = RangeSlider(
        title=" Adjust frequency range",
        start=-18.,
        end=20.,
        step=1,
        value=(np.log10(float(fig.x_range.start)), np.log10(float(fig.x_range.end))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(0))")
    )
    range_slider_x.js_on_change('value',
        CustomJS(args=dict(other=fig.x_range),
                 code="other.start = 10**(this.value[0]);other.end = 10**(this.value[1]);"
        )
    )
    range_slider_y = RangeSlider(
        title=" Adjust strain range",
        start=-35.,
        end=-10.,
        step=1,
        value=(np.log10(float(fig.y_range.start)), np.log10(float(fig.y_range.end))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10.,tick)).toExponential(0))")
    )
    range_slider_y.js_on_change('value',
        CustomJS(args=dict(other=fig.y_range),
                 code="other.start = 10**(this.value[0]);other.end = 10**(this.value[1]);"
        )
    )
    slider_width = Slider(title="Adjust plot width", start=320, end=1920, step=10, value=int(1.61803398875*600))
    callback_width = CustomJS(args=dict(plot=fig, slider=slider_width), code="plot.width = slider.value;")
    slider_width.js_on_change('value', callback_width)

    slider_height = Slider(title="Adjust plot height", start=240, end=1080, step=10, value=600)
    callback_height = CustomJS(args=dict(plot=fig, slider=slider_height), code="plot.height = slider.value;")
    slider_height.js_on_change('value', callback_height)

    return range_slider_x, range_slider_y, slider_width, slider_height  # return the sliders if needed

# Create dictionary of curves

def create_curves_dict(data_instances):
    curves_dict = {}
    for label, data_instance in data_instances.items():
        curves_dict[label] = {'x': data_instance.x_coord, 'y': data_instance.y_coord}
    return curves_dict
