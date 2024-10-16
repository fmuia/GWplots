# aux_functions.py
import numpy as np
import pandas as pd
from bokeh.models import RangeSlider,  CustomJSTickFormatter, Slider, LabelSet, ColumnDataSource, Line
from bokeh.models.widgets import RadioButtonGroup
from scipy.interpolate import RegularGridInterpolator as RGI
from aux.signal_functions import hPT
from aux.data_files import signal_data


Tstar0 = 200.
alpha0 = 0.1
betaOverH0 = 10.
vw0 = 0.4
Gmu0 = 1.E-11
gstar0 = 106.75
MPBH0  = 1.E-6

#Define interpolating function from cosmic string data
def interpolate_cosmic_strings(signal_data):

    #We will collect data from cosmic strings in order to define an interpolating function
    data_strings = []
    coupling_strings = np.array([1.E-11, 1.E-12, 1.E-13, 1.E-14, 1.E-15, 1.E-16, 1.E-17])

    for file_path, label, category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y, label_angle, label_color, label_size in signal_data:
        if label == 'Global string Gmu=1E-11' and file_path !=' ':
            data = np.loadtxt(file_path, dtype=float)
            x_coord_strings =  data[:, 0]
            data_strings.append(np.array(data[:,1]))
        elif 'Global string' in label  and file_path !=' ':
            data = np.loadtxt(file_path, dtype=float)
            data_strings.append(np.array(data[:,1]))

    data_strings = np.array(data_strings)



    # Create interpolation function
    hc_cosmic_strings =  RGI((x_coord_strings, coupling_strings), data_strings.T, method='linear', bounds_error=False)


    return hc_cosmic_strings


#Define interpolating function
hc_cosmic_strings = interpolate_cosmic_strings(signal_data)




#Define interpolating function from PBH data
def interpolate_PBH(signal_data):

    #We will collect data from PBHs in order to define an interpolating function
    data_PBH = []
    mass_PBH = np.array([1.E-6, 1.E-7, 1.E-8, 1.E-9, 1.E-10, 1.E-11, 1.E-12, 1.E-13, 1.E-14, 1.E-15, 1.E-16])

    for file_path, label, category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y, label_angle, label_color, label_size in signal_data:
        if label == 'PBH_MPBH=1E-6' and file_path !=' ':
            data = np.loadtxt(file_path, dtype=float)
            x_coord_PBH =  data[:, 0]
            data_PBH.append(np.array(data[:,1]))
        elif 'PBH' in label  and file_path !=' ':
            data = np.loadtxt(file_path, dtype=float)
            data_PBH.append(np.array(data[:,1]))

    data_PBH = np.array(data_PBH)



    # Create interpolation function
    hc_PBH =  RGI((x_coord_PBH, mass_PBH), data_PBH.T, method='linear', bounds_error=False)


    return hc_PBH


#Define interpolating function
hc_PBH = interpolate_PBH(signal_data)



class Data:
    def __init__(self, x_coord, y_coord, color, linewidth, linestyle, opacity, depth, label, category=None, comment=None, delta_x=0, delta_y=0, label_angle = 0, label_color = 'black', label_size ='9pt'):
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
        self.label_angle = label_angle
        self.label_color = label_color
        self.label_size = label_size

        if len(x_coord) != len(y_coord):
            raise Warning("x_coord and y_coord have different dimensions")

    def load_data(file_path, color, linewidth, linestyle, opacity, depth, label, category, comment, delta_x, delta_y, label_angle, label_color, label_size):  # Update function signature to accept category
        if (category == 'Projected curve') or (category == 'Signal curve'):
            if (file_path) != " ":
                data = np.loadtxt(file_path, dtype=float)
                x_coord, y_coord = data[:, 0], data[:, 1]
                if label == 'CGMB':
                    x_coord = np.array(x_coord)
                    y_coord = np.array(y_coord)
                    #For CGMB we compute label position and angle near peak
                    position_max = np.argmax(y_coord)
                    delta_x = 5.*x_coord[position_max]
                    position_label = np.abs(x_coord - delta_x).argmin()
                    delta_x = x_coord[position_label]
                    delta_y = y_coord[position_label]
                    label_angle = 0

            #FilePath is now empty:
            if label == '1st-order p.t.':
                #For PT, compute array for default parameters, T at weak scale 200 GeV, alpha = 0.1, beta = 10, v = 0.4, gstar = 106.75
                x_coord = 10**np.linspace(-18,21,200)
                x_coord = np.array(x_coord)
                y_coord = hPT(Tstar0, alpha0, betaOverH0, vw0, gstar0, x_coord)
                y_coord = np.array(y_coord)
                #For 1st-order p.t. we compute label position and angle near peak
                derivative = np.gradient(np.log10(y_coord), np.log10(x_coord))
                nan_mask = np.isnan(derivative)
                # Filter out NaN elements using the mask
                derivative = derivative[~nan_mask]
                position_min = np.argmin(abs(derivative))
                delta_x = 1/100000*x_coord[position_min]
                position_label = np.abs(x_coord - delta_x).argmin()
                delta_x = x_coord[position_label]
                delta_y = y_coord[position_label]
                label_angle = np.arctan(derivative[position_label])

            if label == 'Global strings':
                #For global strings, compute array for default parameter Gmu=1E-11
                x_coord = 10**np.linspace(-18,21,200)
                x_coord = np.array(x_coord)
                y_coord = hc_cosmic_strings((x_coord, Gmu0))
                y_coord = np.array(y_coord)
                #For global string we compute label position and angle near max deriv.
                derivative = np.gradient(np.log10(y_coord), np.log10(x_coord))
                # Create a boolean mask for NaN elements
                nan_mask = np.isnan(derivative)
                # Filter out NaN elements using the mask
                derivative = derivative[~nan_mask]
                position_min = np.argmin(abs(derivative))
                delta_x = 1/10*x_coord[position_min]
                position_label = np.abs(x_coord - delta_x).argmin()
                delta_x = x_coord[position_label]
                delta_y = y_coord[position_label]
                label_angle = np.arctan(derivative[position_label])

            if label == 'PBHs':
                #For PBHs, compute array for default parameter M=1E-6
                x_coord = 10**np.linspace(-18,21,200)
                x_coord = np.array(x_coord)
                y_coord = hc_PBH((x_coord, MPBH0))
                y_coord = np.array(y_coord)
                #For PBH we compute label position and angle near max deriv.
                derivative = np.gradient(np.log10(y_coord), np.log10(x_coord))
                # Create a boolean mask for NaN elements
                nan_mask = np.isnan(derivative)
                # Filter out NaN elements using the mask
                derivative = derivative[~nan_mask]
                position_min = np.argmax(abs(derivative))
                delta_x = 1/100000*x_coord[position_min]
                position_label = np.abs(x_coord - delta_x).argmin()
                delta_x = x_coord[position_label]
                delta_y = y_coord[position_label]
                label_angle = np.arctan(derivative[position_label])

        else:
            if (file_path) != " ":
                data = np.loadtxt(file_path, delimiter=',', dtype=float)
                x_coord, y_coord = data[:, 0], data[:, 1]

        return Data(x_coord, y_coord, color, linewidth, linestyle, opacity, depth, label, category, comment, delta_x, delta_y, label_angle, label_color, label_size)  # Pass the category to Data initialization

def load_and_categorize_data(detector_data, signal_data, theoretical_bounds_data):
    #global hc_cosmic_strings
    #hc_cosmic_strings = interpolate_cosmic_strings(signal_data)
    data_instances = {}
    category_dict = {
        'IndBounds': [],
        'DirBounds': [],
        'ProjBounds': [],
        'ProjBoundsCurves': [],
        'SignalCurves': [],
        'SignalLines': [],
        'TheoreticalBounds': []
    }


    #For detector_data
    for file_path, label, category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y, label_angle, label_color, label_size in detector_data:
        data_instances[label] = Data.load_data(file_path, color, linewidth, linestyle, opacity, depth, label, category, comment, delta_x, delta_y, label_angle, label_color, label_size)

        if category == 'Indirect bound':
            category_dict['IndBounds'].append(label)
        elif category == 'Direct bound':
            category_dict['DirBounds'].append(label)
        elif category == 'Projected bound':
            category_dict['ProjBounds'].append(label)
        elif category == 'Projected curve':
            category_dict['ProjBoundsCurves'].append(label)

    #For signal_data
    for file_path, label, category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y, label_angle, label_color, label_size in signal_data:
        data_instances[label] = Data.load_data(file_path, color, linewidth, linestyle, opacity, depth, label, category, comment, delta_x, delta_y, label_angle, label_color, label_size)

        if category == 'Signal curve':
            category_dict['SignalCurves'].append(label)
        elif category == 'Signal line':
            category_dict['SignalLines'].append(label)

    #For theoretical_bounds_data
    for file_path, label, category, color, linewidth, linestyle, opacity, depth, comment, delta_x, delta_y, label_angle, label_color, label_size in theoretical_bounds_data:
        data_instances[label] = Data.load_data(file_path, color, linewidth, linestyle, opacity, depth, label, category, comment, delta_x, delta_y, label_angle, label_color, label_size)

        if category == 'Theoretical Bound':
            category_dict['TheoreticalBounds'].append(label)

    return data_instances, category_dict, hc_cosmic_strings, hc_PBH


# Create plot sliders, and button for h vs Omega

def create_sliders(fig, Omegamin, Omegamax, Shmin, Shmax):
    range_slider_x = RangeSlider(
        title=" Adjust frequency range",
        start=-18.,
        end=20.,
        step=1,
        value=(np.log10(float(fig.x_range.start)), np.log10(float(fig.x_range.end))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(0))")
    )



    range_slider_y = RangeSlider(
        title=r" Adjust $$h_c$$ range",
        start=-39.,
        end=-10.,
        step=1,
        value=(np.log10(float(fig.y_range.start)), np.log10(float(fig.y_range.end))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10.,tick)).toExponential(0))")
    )


    range_slider_y_Omega = RangeSlider(
        title=r" Adjust $$\Omega$$ range",
        start=-40.,
        end=40.,
        step=1,
        value=(np.log10(float(Omegamin)), np.log10(float(Omegamax))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10.,tick)).toExponential(0))")
    )


    range_slider_y_Sh = RangeSlider(
        title=r" Adjust $$S_h$$ range",
        start=-96.,
        end=-2.,
        step=1,
        value=(np.log10(float(Shmin)), np.log10(float(Shmax))),
        format=CustomJSTickFormatter(code="return ((Math.pow(10.,tick)).toExponential(0))")
    )


    slider_width = Slider(title="Adjust plot width", start=320, end=1920, step=10, value=int(1.61803398875*600))


    slider_height = Slider(title="Adjust plot height", start=240, end=1080, step=10, value=600)



    slider_pt_temp = Slider(
        title=" Phase transition temperature (GeV)",
        start=-3.,
        end=16.,
        step=0.05,
        value = np.log10(Tstar0),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    slider_pt_alpha = Slider(
        title=r" $$\alpha$$",
        start=-5.,
        end=3.,
        step=0.05,
        value = np.log10(alpha0),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    slider_pt_betaOverH = Slider(
        title=r" $$\beta/H$$",
        start=-5.,
        end=3.,
        step=0.05,
        value = np.log10(betaOverH0),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    slider_pt_vw = Slider(
        title=r" $$v_w$$",
        start=0.05,
        end=0.99,
        step=0.04,
        value = vw0
        #format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    # Slider for cosmic strings
    slider_cosmic_strings = Slider(
        title=r" String tension  $$G\mu$$",
        start=-17.,
        end=-11.,
        step=0.05,
        value = np.log10(Gmu0),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    #Slider for CGMB
    slider_CGMB = Slider(
        title=r" Temperature (GeV)",
        start=2,
        end=18.3866,
        step=0.05,
        value = 18.3866,
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    # Slider for PBHs
    slider_PBH = Slider(
        title=r" PBH mass  $$M_{PBH}/M_{\odot}$$",
        start=-16.,
        end=-6.,
        step=1,
        value = np.log10(MPBH0),
        format=CustomJSTickFormatter(code="return ((Math.pow(10,tick)).toExponential(2));")
    )

    # Code for h vs Omega button


    # Create a RadioButtonGroup widget
    h_vs_Omega_buttons = RadioButtonGroup(labels=[r"Plot characteristic strain h꜀", r"Plot energy fraction Ω",  r"Plot power spectral density Sh"], active=0)


    return range_slider_x, range_slider_y, range_slider_y_Omega, range_slider_y_Sh, slider_width, slider_height,  slider_pt_temp, slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw, slider_cosmic_strings, slider_CGMB, slider_PBH, h_vs_Omega_buttons   # return the sliders if needed

# Create dictionary of curves and annotations
def create_curves_dict(data_instances, category_dict, hmax):
    curves_dict = {}
    curves_dict_Omega = {}
    curves_dict_Sh = {}
    maxLengthCurves = 1
    maxLengthLines = 1
    #First identify max lengths
    for label, data_instance in data_instances.items():
        category = None
        for cat, labels in category_dict.items():
            if label in labels:
                category = cat
                break
        if (category == 'ProjBoundsCurves') or (category == 'SignalCurves'):
            maxLengthCurves = max(maxLengthCurves, len(data_instance.x_coord))
        if (category == 'SignalLines'):
            maxLengthLines = max(maxLengthLines, len(data_instance.x_coord))
    for label, data_instance in data_instances.items():
        #Extract common keys for simplicity
        color_key = f'color_{label}'
        linewidth_key = f'linewidth_{label}'
        linestyle_key = f'linestyle_{label}'
        opacity_key = f'opacity_{label}'
        depth_key = f'depth_{label}'
        annotation_x_key= f'annotation_x_{label}'  # New key for delta_x
        annotation_y_key = f'annotation_y_{label}'  # New key for delta_y
        label_angle_key = f'label_angle_{label}'
        label_color_key = f'label_color_{label}'
        label_size_key = f'label_size_{label}'

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
            yaux =  np.append(np.append(yaux, [10**10,10**10]), yaux[0])
            testcommentx = data_instance.delta_x
            if (testcommentx):
                annotation_x_aux =  data_instance.delta_x
                annotation_y_aux =  data_instance.delta_y
            else:
                annotation_x_aux =  xaux[0]
                annotation_y_aux =  yaux[0]
            yaux_h = yaux
            annotation_y_aux_h = annotation_y_aux
            curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity,  depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
            #
            #Data for Omega
            yaux = 2.737E36*(xaux**2)*(yaux_h**2)
            annotation_y_aux = 2.737E36*(annotation_x_aux**2)*(annotation_y_aux_h**2)
            curves_dict_Omega[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity,  depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle,  label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
            #
            #Data for Sh
            yaux = yaux_h**2/xaux
            annotation_y_aux = (annotation_y_aux_h**2)/(annotation_x_aux)
            curves_dict_Sh[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity,  depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle,  label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}

        #If ProjBoundsCurves or SignalCurves, we plot line segments
        elif (category == 'ProjBoundsCurves') or (category == 'SignalCurves'):
            x_key = f'xCurve_{label}'
            y_key = f'yCurve_{label}'
            xaux = data_instance.x_coord
            yaux = data_instance.y_coord
            testcommentx = data_instance.delta_x
            if (testcommentx):
                annotation_x_aux =  data_instance.delta_x
                annotation_y_aux =  data_instance.delta_y
            else:
                annotation_x_aux =  xaux[0]
                annotation_y_aux =  yaux[0]
            xlength = len(xaux)
            nextra = maxLengthCurves - len(xaux)
            if nextra==0:
                yaux_h = yaux
                annotation_y_aux_h = annotation_y_aux
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
                #Data for Omega
                yaux = 2.737E36*(xaux**2)*(yaux**2)
                annotation_y_aux = 2.737E36*(annotation_x_aux**2)*(annotation_y_aux**2)
                curves_dict_Omega[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
                #Data for Sh
                yaux = yaux_h**2/xaux
                annotation_y_aux = (annotation_y_aux_h**2)/(annotation_x_aux)
                curves_dict_Sh[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
            else:
                xextra = np.array([ xaux[xlength-1] for _ in range(nextra) ])
                yextra = np.array([ yaux[xlength-1] for _ in range(nextra) ])
                xaux = np.concatenate([xaux,xextra])
                yaux = np.concatenate([yaux,yextra])
                yaux_h = yaux
                annotation_y_aux_h = annotation_y_aux
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
                #Data for Omega
                yaux = 2.737E36*(xaux**2)*(yaux**2)
                annotation_y_aux = 2.737E36*(annotation_x_aux**2)*(annotation_y_aux**2)
                curves_dict_Omega[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
                #Data for Sh
                yaux = yaux_h**2/xaux
                annotation_y_aux = (annotation_y_aux_h**2)/(annotation_x_aux)
                curves_dict_Sh[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
        #If SignalLines, we plot line segments
        elif (category == 'SignalLines') or (category == 'TheoreticalBounds'):
            x_key = f'x_{label}'
            y_key = f'y_{label}'
            xaux = data_instance.x_coord
            yaux = data_instance.y_coord
            testcommentx = data_instance.delta_x
            if (testcommentx):
                annotation_x_aux =  data_instance.delta_x
                annotation_y_aux =  data_instance.delta_y
            else:
                annotation_x_aux =  xaux[0]
                annotation_y_aux =  yaux[0]
            xlength = len(xaux)
            nextra = maxLengthLines- len(xaux)
            if nextra==0:
                yaux_h = yaux
                annotation_y_aux_h = annotation_y_aux
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
                #Data for Omega
                yaux = 2.737E36*(xaux**2)*(yaux**2)
                annotation_y_aux = 2.737E36*(annotation_x_aux**2)*(annotation_y_aux**2)
                curves_dict_Omega[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
                #Data for Sh
                yaux = yaux_h**2/xaux
                annotation_y_aux = (annotation_y_aux_h**2)/(annotation_x_aux)
                curves_dict_Sh[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
            else:
                xextra = np.array([ xaux[xlength-1] for _ in range(nextra) ])
                yextra = np.array([ yaux[xlength-1] for _ in range(nextra) ])
                xaux = np.concatenate([xaux,xextra])
                yaux = np.concatenate([yaux,yextra])
                yaux_h = yaux
                annotation_y_aux_h = annotation_y_aux
                curves_dict[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
                #Data for Omega
                yaux = 2.737E36*(xaux**2)*(yaux**2)
                annotation_y_aux = 2.737E36*(annotation_x_aux**2)*(annotation_y_aux**2)
                curves_dict_Omega[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle,  opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
                #Data for Sh
                yaux = yaux_h**2/xaux
                annotation_y_aux = (annotation_y_aux_h**2)/(annotation_x_aux)
                curves_dict_Sh[label] = {x_key: xaux, y_key: yaux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
        else:
            #Here we plot current bounds, shaded areas
            x_key = f'x_{label}'
            y_key = f'y_{label}'
            y2_key = f'y2_{label}'
            xaux = data_instance.x_coord
            yaux = data_instance.y_coord
            y2aux = np.array([10**10 for _ in range(len(data_instance.y_coord))])
            testcommentx = data_instance.delta_x
            if (testcommentx):
                annotation_x_aux =  data_instance.delta_x
                annotation_y_aux =  data_instance.delta_y
            else:
                annotation_x_aux =  xaux[0]
                annotation_y_aux =  yaux[0]
            yaux_h = yaux
            y2aux_h = y2aux
            annotation_y_aux_h = annotation_y_aux
            curves_dict[label] = {x_key: xaux, y_key: yaux,  y2_key: y2aux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
            #Data for Omega
            yaux = 2.737E36*(xaux**2)*(yaux**2)
            y2aux = 2.737E36*(xaux**2)*(y2aux**2)
            annotation_y_aux = 2.737E36*(annotation_x_aux**2)*(annotation_y_aux**2)
            curves_dict_Omega[label] = {x_key: xaux, y_key: yaux,  y2_key: y2aux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
            #Data for Sh
            yaux = yaux_h**2/xaux
            y2aux = y2aux_h**2/xaux
            annotation_y_aux = (annotation_y_aux_h**2)/(annotation_x_aux)
            curves_dict_Sh[label] = {x_key: xaux, y_key: yaux,  y2_key: y2aux, color_key: data_instance.color, linewidth_key: data_instance.linewidth, linestyle_key: data_instance.linestyle, opacity_key: data_instance.opacity, depth_key: data_instance.depth, annotation_x_key:  annotation_x_aux, annotation_y_key: annotation_y_aux, label_angle_key : data_instance.label_angle, label_color_key : data_instance.label_color, label_size_key : data_instance.label_size}
    return curves_dict, curves_dict_Omega, curves_dict_Sh



# Defines plot data with curves and annotations, plots them invisibly
def add_curves_to_plot(fig, curves_dict, curves_dict_Omega, category_dict, what_to_plot, plot_source_areas, plot_source_rectangles, plot_source_curves, plot_source_lines, annotation_source):

    """"
    Always starts assuming one is plotting strain hc, and so uses curves_dict
    """



    #Ratio to convert angles
    fmin = fig.x_range.start
    fmax = fig.x_range.end
    hmin = fig.y_range.start
    hmax = fig.y_range.end
    ratio = ((np.log10(hmax)-np.log10(hmin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height


    if what_to_plot == 0:
        curves_dict_to_use = curves_dict
        angle_factor = 0.9
    else:
        curves_dict_to_use = curves_dict_Omega
        angle_factor = 1


    for label, data in curves_dict_to_use.items():
        # Determine the category of the curve
        category = None
        for cat, labels in category_dict.items():
            if label in labels:
                category = cat
                break

        color_key = f'color_{label}'
        linewidth_key = f'linewidth_{label}'
        linestyle_key = f'linestyle_{label}'
        opacity_key = f'opacity_{label}'
        depth_key = f'depth_{label}'

        # Generate keys for delta_x and delta_y dynamically based on the label
        annotation_x_key = f'annotation_x_{label}'  # Adjusted to use the dynamic key
        annotation_y_key = f'annotation_y_{label}'  # Adjusted to use the dynamic key
        label_text_key = f'annotation_text_{label}'
        label_angle_key = f'label_angle_{label}'
        label_color_key = f'label_color_{label}'
        label_size_key = f'label_size_{label}'








        label_text = f"{label}"

        #Correct label angle with aspect ratios

        label_angle = np.arctan(angle_factor/ratio*np.tan(data.get(label_angle_key, 0)))# Defaulting to 0 if not present
        # Retrieve delta_x and delta_y using the dynamically generated keys
        annotation_x = data.get(annotation_x_key, 0)  # Defaulting to 0 if not present
        annotation_y = data.get(annotation_y_key, 0)  # Defaulting to 0 if not present
        label_color = data.get(label_color_key, 'black')# Defaulting to black if not present
        label_size = data.get(label_size_key, '9pt')# Defaulting to 9 if not present

        annotation_source.add([annotation_x], annotation_x_key)
        annotation_source.add([annotation_y], annotation_y_key)
        annotation_source.add([label_angle], label_angle_key)
        annotation_source.add([label_text], label_text_key)
        annotation_source.add([label_color], label_color_key)
        annotation_source.add([label_size], label_size_key)

        

        # If the category is found, apply the corresponding style
        if category:
            if (category == 'ProjBounds'):
                #in this case line plot (4-point polygon)
                x_key = f'x_{label}'
                y_key = f'y_{label}'
                plot_source_rectangles.add(data[x_key], x_key)
                plot_source_rectangles.add(data[y_key], y_key)
                fig.line(x = x_key, y = y_key, source = plot_source_rectangles,  color = data[color_key], line_width = data[linewidth_key], line_dash = data[linestyle_key], line_alpha = data[opacity_key], level = data[depth_key], name = label, visible=False)#linewdith, linestyle, legend_label=label,
            elif (category == 'ProjBoundsCurves') or (category == 'SignalCurves') :
                #also line plot but use different names
                x_key = f'xCurve_{label}'
                y_key = f'yCurve_{label}'
                data_x = data[x_key]
                data_y = data[y_key]
                plot_source_curves.add(data_x, x_key)
                plot_source_curves.add(data_y, y_key)
                fig.line(x = x_key, y = y_key, source= plot_source_curves,  color = data[color_key], line_width = data[linewidth_key], line_dash = data[linestyle_key], line_alpha = data[opacity_key], level = data[depth_key], name = label, visible=False)



            elif (category == 'SignalLines') or (category == 'TheoreticalBounds'):
                #also line plot but use different names
                x_key = f'x_{label}'
                y_key = f'y_{label}'
                plot_source_lines.add(data[x_key], x_key)
                plot_source_lines.add(data[y_key], y_key)
                fig.line(x = x_key, y = y_key, source= plot_source_lines,  color = data[color_key], line_width = data[linewidth_key], line_dash = data[linestyle_key], line_alpha = data[opacity_key], level = data[depth_key], name = label, visible=False)
            else:
                #in this case current bounds area plot
                x_key = f'x_{label}'
                y_key = f'y_{label}'
                y2_key = f'y2_{label}'
                plot_source_areas.add(data[x_key], x_key)
                plot_source_areas.add(data[y_key], y_key)
                plot_source_areas.add(data[y2_key], y2_key)
                fig.varea(x = x_key, y1 = y_key, y2=y2_key, source= plot_source_areas,  color = data[color_key], alpha = data[opacity_key], level = data[depth_key], name = label, visible=False)#legend_label=label,



        # Create and add the LabelSet for the annotation
        annotation = LabelSet(x= annotation_x_key, y= annotation_y_key, text=label_text_key, x_offset=0, y_offset=0, source=annotation_source,text_font_size= label_size_key, visible=False, name=f"annotation_{label}", text_color = label_color_key, angle = label_angle_key)  # Unique name
        fig.add_layout(annotation)



    return  fig, plot_source_areas, plot_source_rectangles,  plot_source_curves, plot_source_lines, annotation_source







