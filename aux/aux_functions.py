# aux_functions.py
import numpy as np
from bokeh.models import RangeSlider, CustomJSTickFormatter, CustomJS, Slider, LabelSet, ColumnDataSource

from aux.signal_functions import hPT

#Global phase transition variables
Tstar = 200.
alpha = 0.1
betaOverH = 10.
vw = 0.4
gstar = 106.75

#Global parameters to track changes in phase transition parameteters
Tstarchanged = 0
alphachanged = 0
betaOverHchanged = 0
vwchanged = 0

class Data:
    def __init__(self, x_coord, y_coord, color, linewidth, linestyle, opacity, depth, label, category=None, comment=None, delta_x=0, delta_y=0):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.color = color
        self.linewidth = linewidth
        self.linestyle = linestyle
        self.opacity = opacity
        self.depth = depth
        self.label = label
        self.category = category
        self.comment = comment
        self.delta_x = delta_x
        self.delta_y = delta_y

        if len(x_coord) != len(y_coord):
            raise Warning("x_coord and y_coord have different dimensions")

    def load_data(file_path, color, linewidth, linestyle, opacity, depth, label, category, comment, delta_x, delta_y):  # Update function signature to accept category
        if (category == 'Projected curve') or (category == 'Signal curve'):
            if (file_path) != " ":
                data = np.loadtxt(file_path, dtype=float)
                x_coord, y_coord = data[:, 0], data[:, 1]
            if label == '1st-order phase transition':
                #For PT, compute array for default parameters, T at weak scale 200 GeV, alpha = 0.1, beta = 10, v = 0.4, gstar = 106.75
                x_coord = 10**np.linspace(-18,21,200)
                x_coord = np.array(x_coord)
                y_coord = hPT(Tstar, alpha, betaOverH, vw, gstar, x_coord)
                y_coord = np.array(y_coord)
        else:
            if (file_path) != " ":
                data = np.loadtxt(file_path, delimiter=',', dtype=float)
                x_coord, y_coord = data[:, 0], data[:, 1]

        return Data(x_coord, y_coord, color, linewidth, linestyle, opacity, depth, label, category, comment, delta_x, delta_y)  # Pass the category to Data initialization

def load_and_categorize_data(detector_data, signal_data):
    data_instances = {}
    category_dict = {
        'IndBounds': [],
        'DirBounds': [],
        'ProjBounds': [],
        'ProjBoundsCurves': [],
        'SignalCurves': []
    }

    # Update the loop to handle the comment field
    for file_path, label, category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y in detector_data:
        data_instances[label] = Data.load_data(file_path, color, linewidth, linestyle, opacity, depth, label, category, comment, delta_x, delta_y)

        if category == 'Indirect bound':
            category_dict['IndBounds'].append(label)
        elif category == 'Direct bound':
            category_dict['DirBounds'].append(label)
        elif category == 'Projected bound':
            category_dict['ProjBounds'].append(label)
        elif category == 'Projected curve':
            category_dict['ProjBoundsCurves'].append(label)
        #elif category == 'Signal curve':
        #    category_dict['SignalCurves'].append(label)
            
    for file_path, label, category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y in signal_data:
        data_instances[label] = Data.load_data(file_path, color, linewidth, linestyle, opacity, depth, label, category, comment, delta_x, delta_y)

        if category == 'Signal curve':
            category_dict['SignalCurves'].append(label)

    return data_instances, category_dict


# Create plot sliders

def create_sliders(fig, Tstar):
    range_slider_x = RangeSlider(
        title=" Adjust frequency range",
        start=-18.,
        end=20.,
        step=1,
        value=(np.log10(float(fig.x_range.start)), np.log10(float(fig.x_range.end))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(0))")
    )
    #range_slider_x.js_on_change('value',
    #    CustomJS(args=dict(other=fig.x_range),
    #            code="other.start = 10**(this.value[0]);other.end = 10**(this.value[1]);"
    #   )
    #)
    range_slider_y = RangeSlider(
        title=" Adjust strain range",
        start=-35.,
        end=-10.,
        step=1,
        value=(np.log10(float(fig.y_range.start)), np.log10(float(fig.y_range.end))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10.,tick)).toExponential(0))")
    )
    #range_slider_y.js_on_change('value',
    #    CustomJS(args=dict(other=fig.y_range),
    #             code="other.start = 10**(this.value[0]);other.end = 10**(this.value[1]);"
    #    )
    #)

    slider_width = Slider(title="Adjust plot width", start=320, end=1920, step=10, value=int(1.61803398875*600))
    #callback_width = CustomJS(args=dict(plot=fig, slider=slider_width), code="plot.width = slider.value;")
    #slider_width.js_on_change('value', callback_width)

    slider_height = Slider(title="Adjust plot height", start=240, end=1080, step=10, value=600)
    #callback_height = CustomJS(args=dict(plot=fig, slider=slider_height), code="plot.height = slider.value;")
    #slider_height.js_on_change('value', callback_height)


    slider_pt_temp = Slider(
        title=" Phase transition temperature (GeV)",
        start=-3.,
        end=16.,
        step=0.05,
        value = np.log10(Tstar),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    slider_pt_alpha = Slider(
        title=" alpha",
        start=-5.,
        end=3.,
        step=0.05,
        value = np.log10(alpha),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    slider_pt_betaOverH = Slider(
        title=" beta/H",
        start=-5.,
        end=3.,
        step=0.05,
        value = np.log10(betaOverH),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    slider_pt_vw = Slider(
        title=" vw",
        start=0.05,
        end=0.99,
        step=0.04,
        value = vw
        #format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    return range_slider_x, range_slider_y, slider_width, slider_height,  slider_pt_temp, slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw   # return the sliders if needed

# Create dictionary of curves
def create_curves_dict(data_instances, category_dict, hmax):
    curves_dict = {}
    maxLengthProjBounds = 1
    #First identify max lengths
    for label, data_instance in data_instances.items():
        category = None
        for cat, labels in category_dict.items():
            if label in labels:
                category = cat
                break
        if (category == 'ProjBoundsCurves') or (category == 'SignalCurves'):
            maxLengthProjBounds = max(maxLengthProjBounds, len(data_instance.x_coord))
    for label, data_instance in data_instances.items():
        #Extract common keys for simplicity
        color_key = f'color_{label}'
        linewidth_key = f'linewidth_{label}'
        linestyle_key = f'linestyle_{label}'
        opacity_key = f'opacity_{label}'
        depth_key = f'depth_{label}'
        delta_x_key = f'delta_x_{label}'  # New key for delta_x
        delta_y_key = f'delta_y_{label}'  # New key for delta_y

        # Determine the category of the curve
        category = None
        for cat, labels in category_dict.items():
            if label in labels:
                category = cat
                break

        #If category is ProjBounds, want to plot polygon
        if (category == 'ProjBounds'):
            x_key = f'x_{label}'
            y_key = f'y_{label}'
            xaux = data_instance.x_coord
            yaux = data_instance.y_coord
            xaux = np.append(np.append( xaux, np.flip(xaux)), xaux[0])
            yaux =  np.append(np.append(yaux, [hmax,hmax]), yaux[0])
            curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity,  depth_key: data_instance.depth, delta_x_key: data_instance.delta_x, delta_y_key: data_instance.delta_y}
        elif (category == 'ProjBoundsCurves') or (category == 'SignalCurves'):
            x_key = f'xCurve_{label}'
            y_key = f'yCurve_{label}'
            xaux = data_instance.x_coord
            yaux = data_instance.y_coord
            xlength = len(xaux)
            nextra = maxLengthProjBounds - len(xaux)
            if nextra==0:
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, delta_x_key: data_instance.delta_x, delta_y_key: data_instance.delta_y}
            else:
                xextra = np.array([ xaux[xlength-1] for _ in range(nextra) ])
                yextra = np.array([ yaux[xlength-1] for _ in range(nextra) ])
                xaux = np.concatenate([xaux,xextra])
                yaux = np.concatenate([yaux,yextra])
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity, depth_key: data_instance.depth, delta_x_key: data_instance.delta_x, delta_y_key: data_instance.delta_y}
        else:
            x_key = f'x_{label}'
            y_key = f'y_{label}'
            y2_key = f'y2_{label}'
            curves_dict[label] = {x_key: data_instance.x_coord, y_key: data_instance.y_coord,  y2_key: np.array([10**-2 for _ in range(len(data_instance.y_coord))]), color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, delta_x_key: data_instance.delta_x, delta_y_key: data_instance.delta_y}
    return curves_dict



from bokeh.models import Line

def add_curves_to_plot(fig, curves_dict, category_dict, plot_source, plot_source_proj,  plot_source_proj_curves): # before it had argument plot_source
    """
    This function adds lines to the figure for each curve in curves_dict
    with different styles based on the category of each curve.
    """

    # Define styles for each category, deprecated
    # styles = {
    #     'IndBounds': {'line_color': 'blue', 'line_dash': 'solid'},
    #     'DirBounds': {'line_color': 'red', 'line_dash': 'dashed'},
    #     'ProjBounds': {'line_color': 'green', 'line_dash': 'dotdash'},
    #     'Detectors': {'line_color': 'black', 'line_dash': 'dotted'}
    # }

    for label, data in curves_dict.items():
        # Determine the category of the curve
        category = None
        for cat, labels in category_dict.items():
            if label in labels:
                category = cat
                break

        # Generate keys for delta_x and delta_y dynamically based on the label
        delta_x_key = f'delta_x_{label}'  # Adjusted to use the dynamic key
        delta_y_key = f'delta_y_{label}'  # Adjusted to use the dynamic key

        # Retrieve delta_x and delta_y using the dynamically generated keys
        delta_x = data.get(delta_x_key, 0)  # Defaulting to 0 if not present
        delta_y = data.get(delta_y_key, 0)  # Defaulting to 0 if not present


        #x_key = f'x_{label}'
        #y_key = f'y_{label}'
        color_key = f'color_{label}'
        linewidth_key = f'linewidth_{label}'
        linestyle_key = f'linestyle_{label}'
        opacity_key = f'opacity_{label}'
        depth_key = f'depth_{label}'
        

        # If the category is found, apply the corresponding style
        if category:
            if (category == 'ProjBounds'):
                #in this case line plot
                plotsource = plot_source_proj
                x_key = f'x_{label}'
                y_key = f'y_{label}'
                plotsource.add([], x_key)
                plotsource.add([], y_key)
                annotation_x = data[x_key][0] + delta_x
                annotation_y = data[y_key][0] + delta_y
                fig.line(x = x_key, y = y_key, source=plotsource,  color = data[color_key], line_width = data[linewidth_key], line_dash = data[linestyle_key], line_alpha = data[opacity_key], level = data[depth_key])#linewdith, linestyle, legend_label=label,
            elif (category == 'ProjBoundsCurves') or (category == 'SignalCurves') :
                #also line plot but use different names
                plotsource = plot_source_proj_curves
                x_key = f'xCurve_{label}'
                y_key = f'yCurve_{label}'
                plotsource.add([], x_key)
                plotsource.add([], y_key)
                annotation_x = data[x_key][0] + delta_x
                annotation_y = data[y_key][0] + delta_y
                fig.line(x = x_key, y = y_key, source=plotsource,  color = data[color_key], line_width = data[linewidth_key], line_dash = data[linestyle_key], line_alpha = data[opacity_key], level = data[depth_key])
            else:
                #in this case current bounds area plot
                plotsource = plot_source
                x_key = f'x_{label}'
                y_key = f'y_{label}'
                y2_key = f'y2_{label}'
                plotsource.add([], x_key)
                plotsource.add([], y_key)
                plotsource.add([], y2_key)
                annotation_x = data[x_key][0] + delta_x
                annotation_y = data[y_key][0] + delta_y
                fig.varea(x = x_key, y1 = y_key, y2=y2_key, source=plotsource,  color = data[color_key], alpha = data[opacity_key], level = data[depth_key])#legend_label=label,


        annotation_text = f"{label}"

        # Create a separate ColumnDataSource for each annotation
        annotation_source = ColumnDataSource({
            'x': [annotation_x],
            'y': [annotation_y],
            'text': [annotation_text]
        })

        # Create and add the LabelSet for the annotation
        annotation = LabelSet(x='x', y='y', text='text',
                              x_offset=0, y_offset=0, source=annotation_source,
                              text_font_size='10pt', visible=False,
                              name=f"annotation_{label}")  # Unique name
        fig.add_layout(annotation)



# Define update_plot function
def update_plot(button_label, curves_dict, on_buttons):
    #print("On buttons are: " + str(on_buttons))    

    # Check if button is in on_buttons, and add or remove it accordingly
    if button_label in on_buttons:
        on_buttons.remove(button_label)
    else:
        on_buttons.append(button_label)

    # Initialize an empty dictionary to hold the result
    result_dict = {}

    # Iterate through each button in on_buttons and add the corresponding data to result_dict
    for btn in on_buttons:
        curve_data = curves_dict.get(btn, {})
        for key, value in curve_data.items():
            if isinstance(value, str) or isinstance(value, int) or isinstance(value, float) :
                result_dict[key] = value
            else:
                result_dict[key] = value.tolist()

    #print("Result dict: " + str(result_dict))
    #print("On_buttons: ", on_buttons)

    return result_dict, on_buttons
