#app.py

# Import all the relevant libraries and packages

from aux.imports import *


from aux.data_files import detector_data,signal_data, theoretical_bounds_data
from aux.aux_functions import load_and_categorize_data
from aux.aux_functions import interpolate_cosmic_strings
from aux.aux_functions import create_sliders
from aux.aux_functions import create_curves_dict
from aux.aux_functions import add_curves_to_plot

from aux.aux_functions import Tstar0
from aux.aux_functions import alpha0
from aux.aux_functions import betaOverH0
from aux.aux_functions import vw0
from aux.aux_functions import Gmu0
from aux.aux_functions import MPBH0
from aux.aux_functions import gstar0


from aux.signal_functions import hPT














# Suppress specific Bokeh warning
warnings.filterwarnings("ignore", message="ColumnDataSource's columns must be of the same length")





# Initialize app
app = Flask(__name__)




## Load detector curves

# Load data into Data class instances collected in the dictionary data_instances
# Create a dictionary category_dict containing the experiment labels divided into categories (Indirect bounds, Direct bounds, Projected bounds and others)


data_instances, category_dict, hc_cosmic_strings, hc_PBH = load_and_categorize_data(detector_data, signal_data, theoretical_bounds_data)

## Define app section

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/get_comments')
def get_comments():
    label = request.args.get('label')
    data_instance = data_instances.get(label, None)
    comment = data_instance.comment if data_instance and data_instance.comment not in [None, ''] else None
    
    return jsonify({'comment': comment})

# Flask route to serve the HTML template with the initial Bokeh plot
@app.route('/')
def index():
    script_bokeh_plot = server_document(url=f"http://localhost:5006/plot")


    return render_template(
        'index.html',
        script_bokeh_plot = script_bokeh_plot,
        bokeh_css=INLINE.render_css(),
        bokeh_js=INLINE.render_js(),
        category_dict=category_dict
    )



#Bokeh app for all
def bokeh_plot_app(doc):
    #Global variables that can be seen by all users, even if they are fed different plots
    global hc_cosmic_strings, data_instances, category_dict, curves_dict, curves_dict_Omega
    #Initial value of what to plot: 0 (plot h) as opposed to 1 (plot Omega)
    what_to_plot = 0

    #Phase transition, cosmic string and TCGMB variables only defined in app, not globally, matching initial values
    Tstar = Tstar0
    alpha = alpha0
    betaOverH = betaOverH0
    vw = vw0
    Gmu = Gmu0
    MPBH = MPBH0
    gstar = gstar0
    Mp = 2.43536E18 #Planck mass
    TCGMB = Mp #Initial CGMB temp plotted at Planck T





    # Global ColumnDataSource objects to manage plot data


    plot_source_areas = ColumnDataSource(data=dict(), name='plot_source_areas')
    plot_source_rectangles = ColumnDataSource(data=dict(), name='plot_source_rectangles')
    plot_source_curves = ColumnDataSource(data=dict(), name='plot_source_curves')
    plot_source_lines =  ColumnDataSource(data=dict(), name='plot_source_lines')
    # Annotations object
    annotation_source = ColumnDataSource(data=dict(), name='annotation_source')



    # Set up the figure

    #Global parameters for range, width and height
    hmin = 10.**-39.
    hmax = 10.**-10.

    Omegamin = 10.**-40.
    Omegamax = 10.**25.

    Shmin = 10.**-96.
    Shmax = 10.**-2.

    hrangechanged = 0
    Omegarangechanged = 0
    Shrangechanged = 0
    fmin = 10**-18.
    fmax = 10**20.
    frangechanged = 0
    plot_width = int(900)
    plot_width_changed = 0
    plot_height = 600
    plot_height_changed = 0
    xrange = (fmin, fmax)
    yrange = (hmin, hmax)

    fig = figure(background_fill_color='white',
    border_fill_color='black',
    border_fill_alpha=0.0,
    height= plot_height,
    width= plot_width,
    x_axis_label='frequency (Hz)',
    x_axis_type='log',
    x_axis_location='below',
    x_range=xrange,
    y_axis_label=r'$$h_c$$',
    y_axis_type='log',
    y_axis_location='left',
    y_range=yrange,
    title=r"Gravitational waves plotter",
    title_location='above',
    toolbar_location='below',
    tools='save',name = 'myplot')
    fig.output_backend = "svg"
    fig.xgrid.level = 'image'
    fig.ygrid.level = 'image'




    # Set up the sliders

    slider_x, slider_y, slider_y_Omega,  slider_y_Sh, slider_width,  slider_height, slider_pt_temp,  slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw, slider_cosmic_strings, slider_CGMB, slider_PBH, h_vs_Omega_buttons = create_sliders(fig, Omegamin, Omegamax, Shmin, Shmax)


    # Create dictionary of curves

    curves_dict, curves_dict_Omega, curves_dict_Sh = create_curves_dict(data_instances, category_dict, hmax)


    # Link curves to a chart
    fig, plot_source_areas, plot_source_rectangles,  plot_source_curves, plot_source_lines, annotation_source = add_curves_to_plot(fig, curves_dict, curves_dict_Omega, category_dict, what_to_plot, plot_source_areas, plot_source_rectangles,  plot_source_curves, plot_source_lines, annotation_source )


    #Main plot with range/size sliders
    layout = column(h_vs_Omega_buttons, fig)
    #Sliders for range/size
    layout_size = column(Div(text="<h1>Plot range and size</h1>"), slider_x, slider_y, slider_y_Omega, slider_y_Sh,  slider_width, slider_height)
    # #Sliders for phase transition parameters
    layout2 = column(Div(text="<h1>Phase transitions</h1>"), slider_pt_temp, slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw)
    #Slider for phase cosmic strings
    layout_cosmic_strings = column(Div(text="<h1>Global strings</h1>"),slider_cosmic_strings)
    #Slider for CGMB
    layout_CGMB = column(Div(text="<h1>CGMB</h1>"),slider_CGMB)
    #Slider for PBH
    layout_PBH = column(Div(text="<h1>PBHs (stochastic)</h1>"),slider_PBH)





    # Update plot data when changing between h and Omega and Sh-- ColumnDataSources and annotations
    def update_plot_data(curves_dict, curves_dict_Omega, curves_dict_Sh, category_dict, what_to_plot):


        nonlocal plot_source_areas
        nonlocal plot_source_rectangles
        nonlocal plot_source_curves
        nonlocal plot_source_lines
        nonlocal annotation_source
        nonlocal fig
        # To reduce individual changes (communications with server) update main variable only once, so we use first copy
        new_data_areas = {}
        new_data_rectangles = {}
        new_data_curves = {}
        new_data_lines = {}
        new_data_annotation = dict(annotation_source.data)

        # ColumnDataSource objects to manage plot data
        #plot_source = ColumnDataSource(data=dict(), name='plot_source')
        #plot_source_rectangles = ColumnDataSource(data=dict(), name='plot_source_rectangles')
        #plot_source_curves = ColumnDataSource(data=dict(), name='plot_source_curves')

        # Annotations object
        #plot_annotations = {}


        if what_to_plot == 0:
            curves_dict_to_use = curves_dict
        elif what_to_plot == 1:
            curves_dict_to_use = curves_dict_Omega
        elif what_to_plot == 2:
            curves_dict_to_use = curves_dict_Sh
        #Update plot_sources


        for label, data in curves_dict_to_use.items():
            # Determine the category of the curve
            category = None
            for cat, labels in category_dict.items():
                if label in labels:
                    category = cat
                    break

            # Generate keys for delta_x and delta_y dynamically based on the label
            annotation_x_key = f'annotation_x_{label}'  # Adjusted to use the dynamic key
            annotation_y_key = f'annotation_y_{label}'  # Adjusted to use the dynamic key
            label_angle_key  = f'label_angle_{label}'

            x_label = data.get(annotation_x_key, 0)
            y_label = data.get(annotation_y_key, 0)
            new_data_annotation[annotation_x_key] = [x_label]  # Change the x position
            new_data_annotation[annotation_y_key] = [y_label]  # Change the x position


            #Change label angles for selected curves when going from hc to Omega
            label_angle = data.get(label_angle_key, 0)
            if what_to_plot == 1 and  (label_angle) != 0:
                ratio = ((np.log10(Omegamax)-np.log10(Omegamin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height
                new_label_angle = np.arctan(1/ratio*(2.+2.*np.tan(label_angle)))
                new_data_annotation[label_angle_key] = [new_label_angle]
            if what_to_plot == 0 and  (label_angle) != 0:
                ratio = ((np.log10(hmax)-np.log10(hmin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height
                new_label_angle = np.arctan(0.9/ratio*(np.tan(label_angle)))
                new_data_annotation[label_angle_key] = [new_label_angle]
            if what_to_plot == 2 and  (label_angle) != 0:
                ratio = ((np.log10(Shmax)-np.log10(Shmin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height
                new_label_angle = np.arctan(1/ratio*(2.*np.tan(label_angle)-1))
                new_data_annotation[label_angle_key] = [new_label_angle]



            # If the category is found, apply the corresponding style
            if category:
                if (category == 'ProjBounds'):
                    #in this case line plot
                    #plotsource = plot_source_rectangles
                    x_key = f'x_{label}'
                    y_key = f'y_{label}'
                    # plot_source_rectangles.add(data[x_key], x_key)
                    # plot_source_rectangles.add(data[y_key], y_key)
                    new_data_rectangles[x_key] = data[x_key]
                    new_data_rectangles[y_key] = data[y_key]
                    #fig.line(x = x_key, y = y_key, source = plot_source_rectangles,  color = data[color_key], line_width = data[linewidth_key], line_dash = data[linestyle_key], line_alpha = data[opacity_key], level = data[depth_key], name = label, visible=False)#linewdith, linestyle, legend_label=label,
                elif (category == 'ProjBoundsCurves') or (category == 'SignalCurves') :
                    #also line plot but use different names
                    #plotsource = plot_source_curves
                    x_key = f'xCurve_{label}'
                    y_key = f'yCurve_{label}'
                    new_data_curves[x_key] = data[x_key]
                    if (y_key == 'yCurve_CGMB' ):
                        if (what_to_plot == 0):
                            #Plot h, rescales as Sqrt(T/MP) wrt to case with T=Mp stored in dict
                            new_data_curves[y_key] = np.array(np.sqrt(TCGMB/Mp)*data[y_key])
                        else:
                            #Plot Omega or Sh, both scale as (T/MP)  wrt to case with T=Mp stored in dict
                            new_data_curves[y_key] =  np.array((TCGMB/Mp)*data[y_key])
                    else:
                        #Not in CGMB, just regular substitution
                        new_data_curves[y_key] = data[y_key]
                    #fig.line(x = x_key, y = y_key, source= plot_source_curves,  color = data[color_key], line_width = data[linewidth_key], line_dash = data[linestyle_key], line_alpha = data[opacity_key], level = data[depth_key], name = label, visible=False)
                elif (category == 'SignalLines') or (category == 'TheoreticalBounds') :
                    #also line plot but use different names
                    x_key = f'x_{label}'
                    y_key = f'y_{label}'
                    new_data_lines[x_key] = data[x_key]
                    new_data_lines[y_key] = data[y_key]
                else:
                    #in this case current bounds area plot
                    #plotsource = plot_source
                    x_key = f'x_{label}'
                    y_key = f'y_{label}'
                    y2_key = f'y2_{label}'
                    new_data_areas[x_key] = data[x_key]
                    new_data_areas[y_key] = data[y_key]
                    new_data_areas[y2_key] = data[y2_key]

        plot_source_areas.data = new_data_areas
        plot_source_rectangles.data = new_data_rectangles
        plot_source_curves.data = new_data_curves
        plot_source_lines.data = new_data_lines
        annotation_source.data = new_data_annotation


    #Define a callback function for the what_to_plot_button
    def h_vs_Omega_button_handler(new, curves_dict, curves_dict_Omega, category_dict):
        nonlocal plot_source_areas
        nonlocal plot_source_rectangles
        nonlocal plot_source_curves
        nonlocal fig
        nonlocal what_to_plot
        #nonlocal hmin, hmax, Omegamin, Omegamax
        what_to_plot = new
        #print('what_to_plot = ',what_to_plot)
        #Update ranges
        if what_to_plot == 0:
             fig.y_range.start = hmin
             fig.y_range.end = hmax
             fig.yaxis.axis_label = r'$$h_c$$'
        elif what_to_plot == 1:
             fig.y_range.start = Omegamin
             fig.y_range.end = Omegamax
             fig.yaxis.axis_label = r'$$h^2 \Omega$$'
        elif what_to_plot == 2:
             fig.y_range.start = Shmin
             fig.y_range.end = Shmax
             fig.yaxis.axis_label = r'$$S_h\,\, [{\rm Hz}^{-1}]$$'
        # Call the update_plot_data function and update new_data
        update_plot_data(curves_dict, curves_dict_Omega, curves_dict_Sh, category_dict, what_to_plot)


    h_vs_Omega_buttons.on_change('active', lambda attr, old, new:  h_vs_Omega_button_handler(new, curves_dict, curves_dict_Omega, category_dict))

    #Function that updates annotation_angles and positions
    def update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax):

        # To reduce individual changes (communications with server) update main variable only once, so we use first copy
        new_data_annotation = dict(annotation_source.data)

        if what_to_plot == 0:
            curves_dict_to_use = curves_dict
        elif what_to_plot == 1:
            curves_dict_to_use = curves_dict_Omega
        elif what_to_plot == 2:
            curves_dict_to_use = curves_dict_Sh

        #Update plot_sources

        for label, data in curves_dict_to_use.items():
            # Generate keys for delta_x and delta_y dynamically based on the label
            annotation_x_key = f'annotation_x_{label}'  # Adjusted to use the dynamic key
            annotation_y_key = f'annotation_y_{label}'  # Adjusted to use the dynamic key
            label_angle_key  = f'label_angle_{label}'

            x_label = data.get(annotation_x_key, 0)
            y_label = data.get(annotation_y_key, 0)

            new_data_annotation[annotation_x_key] = [x_label]  # Change the x position
            new_data_annotation[annotation_y_key] = [y_label]  # Change the x position


            #Change label angles for selected curves when going from hc to Omega
            label_angle = data.get(label_angle_key, 0)

            if what_to_plot == 1 and  (label_angle) != 0:
                ratio = ((np.log10(Omegamax)-np.log10(Omegamin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height
                new_label_angle = np.arctan(1/ratio*(2.+2.*np.tan(label_angle)))
                new_data_annotation[label_angle_key] = [new_label_angle]

            if what_to_plot == 0 and  (label_angle) != 0:
                ratio = ((np.log10(hmax)-np.log10(hmin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height
                new_label_angle = np.arctan(0.9/ratio*(np.tan(label_angle)))
                new_data_annotation[label_angle_key] = [new_label_angle]

            if what_to_plot == 2 and  (label_angle) != 0:
                ratio = ((np.log10(Shmax)-np.log10(Shmin))/(np.log10(fmax)-np.log10(fmin)))*fig.width/fig.height
                new_label_angle = np.arctan(1/ratio*(2.*np.tan(label_angle)-1))
                new_data_annotation[label_angle_key] = [new_label_angle]



        return new_data_annotation


    #Define a callback function for plot size, and update annotation angles, for example after changing range which affects aspect ratio
    def update_frange(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot):

        nonlocal fig
        nonlocal annotation_source
        nonlocal fmin
        nonlocal fmax

        fmin = 10.**new[0]
        fmax = 10.**new[1]
        fig.x_range.start  = fmin
        fig.x_range.end = fmax

        annotation_source.data = update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)


    slider_x.on_change('value', lambda attr, old, new: update_frange(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot))

    def update_hrange(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot):

        nonlocal fig
        nonlocal annotation_source
        nonlocal hmin
        nonlocal hmax


        hmin = 10.**new[0]
        hmax = 10.**new[1]
        if what_to_plot == 0:
            fig.y_range.start = hmin
            fig.y_range.end = hmax

            annotation_source.data =  update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)


    slider_y.on_change('value', lambda attr, old, new: update_hrange(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot))

    def update_Omegarange(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot):

        nonlocal annotation_source
        nonlocal fig
        nonlocal Omegamin
        nonlocal Omegamax

        Omegamin = 10.**new[0]
        Omegamax = 10.**new[1]

        if what_to_plot == 1:
            fig.y_range.start = Omegamin
            fig.y_range.end = Omegamax

            annotation_source.data =  update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)

    slider_y_Omega.on_change('value', lambda attr, old, new: update_Omegarange(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot))

    def update_Shrange(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot):

        nonlocal annotation_source
        nonlocal fig
        nonlocal Shmin
        nonlocal Shmax

        Shmin = 10.**new[0]
        Shmax = 10.**new[1]

        if what_to_plot == 2:
            fig.y_range.start = Shmin
            fig.y_range.end = Shmax

            annotation_source.data =  update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)

    slider_y_Sh.on_change('value', lambda attr, old, new: update_Shrange(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot))


    def update_width(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot):

        nonlocal fig
        nonlocal annotation_source

        fig.width = slider_width.value;

        annotation_source.data =  update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)


    slider_width.on_change('value', lambda attr, old, new: update_width(new, curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot))


    def update_height(new, curves_dict, curves_dict_Omega, what_to_plot):

        nonlocal fig
        nonlocal annotation_source

        fig.height = slider_height.value;
        annotation_source.data =  update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)

    slider_height.on_change('value',  lambda attr, old, new: update_height(new, curves_dict, curves_dict_Omega, what_to_plot))




    #Handling changes in phase transition parameters: Simply change plot sources. Future: Do it only if active?
    def update_plot_phase_transition():

        nonlocal plot_source_curves
        nonlocal annotation_source



        x_coord = curves_dict['1st-order p.t.']['xCurve_1st-order p.t.']
        y_coord = np.array(hPT(Tstar, alpha, betaOverH, vw, gstar, x_coord))
        #For 1st-order p.t. we compute label position and angle near peak
        derivative = np.gradient(np.log10(y_coord), np.log10(x_coord))
        nan_mask = np.isnan(derivative)
        # Filter out NaN elements using the mask
        derivative = derivative[~nan_mask]
        if len(derivative)>0:
            position_min = np.argmin(abs(derivative))
            delta_x = 1/100000*x_coord[position_min]
            position_label = np.abs(x_coord - delta_x).argmin()
            delta_x = x_coord[position_label]
            delta_y = y_coord[position_label]
            label_angle = np.arctan(derivative[position_label])
        else:
            #If curve seems problematic, take delta_x delta_y out of plot, label angle 0
            delta_x = 1.e-5*fmin
            delta_y = 1.e-5*min(hmin,Omegamin)
            label_angle = 0.

        y_coord_h = y_coord
        delta_y_h = delta_y
        delta_x_h = delta_x

        curves_dict['1st-order p.t.']['yCurve_1st-order p.t.'] = y_coord
        curves_dict['1st-order p.t.']['annotation_x_1st-order p.t.'] = delta_x
        curves_dict['1st-order p.t.']['annotation_y_1st-order p.t.'] = delta_y
        curves_dict['1st-order p.t.']['label_angle_1st-order p.t.'] = label_angle

        #Coords for Omega
        y_coord = 2.737E36*(x_coord**2)*(y_coord**2)
        delta_y = 2.737E36*(delta_x**2)*(delta_y**2)

        curves_dict_Omega['1st-order p.t.']['yCurve_1st-order p.t.'] = y_coord
        curves_dict_Omega['1st-order p.t.']['annotation_x_1st-order p.t.'] = delta_x
        curves_dict_Omega['1st-order p.t.']['annotation_y_1st-order p.t.'] = delta_y
        curves_dict_Omega['1st-order p.t.']['label_angle_1st-order p.t.'] = label_angle

        #Coords for Sh
        y_coord = y_coord_h**2/x_coord
        delta_y = delta_y_h**2/delta_x_h

        curves_dict_Sh['1st-order p.t.']['yCurve_1st-order p.t.'] = y_coord
        curves_dict_Sh['1st-order p.t.']['annotation_x_1st-order p.t.'] = delta_x
        curves_dict_Sh['1st-order p.t.']['annotation_y_1st-order p.t.'] = delta_y
        curves_dict_Sh['1st-order p.t.']['label_angle_1st-order p.t.'] = label_angle

        if what_to_plot == 0:
            plot_source_curves.data['yCurve_1st-order p.t.'] = curves_dict['1st-order p.t.']['yCurve_1st-order p.t.']
        elif what_to_plot == 1:
            plot_source_curves.data['yCurve_1st-order p.t.'] = curves_dict_Omega['1st-order p.t.']['yCurve_1st-order p.t.']
        elif what_to_plot == 2:
            plot_source_curves.data['yCurve_1st-order p.t.'] = curves_dict_Sh['1st-order p.t.']['yCurve_1st-order p.t.']

        annotation_source.data = update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)



    # Define a callback function for the phase transition sliders
    def update_tstar(attr, old, new):
        nonlocal Tstar
        Tstar = 10**slider_pt_temp.value
        update_plot_phase_transition()
    def update_alpha(attr, old, new):
        nonlocal alpha
        alpha = 10**slider_pt_alpha.value
        update_plot_phase_transition()
    def update_betaOverH(attr, old, new):
        nonlocal betaOverH
        betaOverH = 10**slider_pt_betaOverH.value
        update_plot_phase_transition()
    def update_vw(attr, old, new):
        nonlocal vw
        vw = slider_pt_vw.value
        update_plot_phase_transition()

    # Attach the Python function to the 'value' change event of the slider
    slider_pt_temp.on_change('value', update_tstar)
    slider_pt_alpha.on_change('value', update_alpha)
    slider_pt_betaOverH.on_change('value', update_betaOverH)
    slider_pt_vw.on_change('value', update_vw)



    #Handling changes in cosmic string parameters
    def update_plot_cosmic_strings():
        global hc_cosmic_strings
        nonlocal plot_source_curves
        nonlocal annotation_source

        # Update the curves dict and plot based on the global variables of phase transitions
        x_coord = curves_dict['Global strings']['xCurve_Global strings']
        y_coord = np.array(hc_cosmic_strings((x_coord, Gmu)))
        #For cosmic st. we compute label position and angle near peak
        derivative = np.gradient(np.log10(y_coord), np.log10(x_coord))
        nan_mask = np.isnan(derivative)
        # Filter out NaN elements using the mask
        derivative = derivative[~nan_mask]
        if len(derivative)>0:
            position_min = np.argmin(abs(derivative))
            delta_x = 1/10*x_coord[position_min]
            position_label = np.abs(x_coord - delta_x).argmin()
            delta_x = x_coord[position_label]
            delta_y = y_coord[position_label]
            label_angle = np.arctan(derivative[position_label])
        else:
            #If curve seems problematic, take delta_x delta_y out of plot, label angle 0
            delta_x = 1.e-5*fmin
            delta_y = 1.e-5*min(hmin,Omegamin)
            label_angle = 0.

        y_coord_h = y_coord
        delta_y_h = delta_y
        delta_x_h = delta_x

        curves_dict['Global strings']['yCurve_Global strings'] = y_coord
        curves_dict['Global strings']['annotation_x_Global strings'] = delta_x
        curves_dict['Global strings']['annotation_y_Global strings'] = delta_y
        curves_dict['Global strings']['label_angle_Global strings'] = label_angle

        #Change values of Omega
        y_coord = 2.737E36*(x_coord**2)*(y_coord**2)
        delta_y = 2.737E36*(delta_x**2)*(delta_y**2)

        curves_dict_Omega['Global strings']['yCurve_Global strings'] = y_coord
        curves_dict_Omega['Global strings']['annotation_x_Global strings'] = delta_x
        curves_dict_Omega['Global strings']['annotation_y_Global strings'] = delta_y
        curves_dict_Omega['Global strings']['label_angle_Global strings'] = label_angle

        #Change values of Sh
        y_coord = y_coord_h**2/x_coord
        delta_y = delta_y_h**2/delta_x_h

        curves_dict_Sh['Global strings']['yCurve_Global strings'] = y_coord
        curves_dict_Sh['Global strings']['annotation_x_Global strings'] = delta_x
        curves_dict_Sh['Global strings']['annotation_y_Global strings'] = delta_y
        curves_dict_Sh['Global strings']['label_angle_Global strings'] = label_angle

        # Update the shared data source when the slider changes
        if what_to_plot == 0:
            plot_source_curves.data['yCurve_Global strings'] = curves_dict['Global strings']['yCurve_Global strings']
        elif what_to_plot == 1:
            plot_source_curves.data['yCurve_Global strings'] = curves_dict_Omega['Global strings']['yCurve_Global strings']
        elif what_to_plot == 2:
            plot_source_curves.data['yCurve_Global strings'] = curves_dict_Sh['Global strings']['yCurve_Global strings']

        annotation_source.data = update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)


    # Define a callback function for the phase transition sliders
    def update_Gmu(attr, old, new):
        nonlocal Gmu
        Gmu = 10**slider_cosmic_strings.value
        update_plot_cosmic_strings()


    # Attach the Python function to the 'value' change event of the slider
    slider_cosmic_strings.on_change('value', update_Gmu)



    #####################################
    #####################################
    #####################################
    #####################################
    #Handling changes in PBH mass


    def update_plot_PBH():
        global hc_PBH
        nonlocal plot_source_curves
        nonlocal annotation_source

        # Update the curves dict and plot based on the global variables of phase transitions
        x_coord = curves_dict['PBHs']['xCurve_PBHs']
        y_coord = np.array(hc_PBH((x_coord, MPBH)))
        #For PBHs we compute label position and angle near peak
        derivative = np.gradient(np.log10(y_coord), np.log10(x_coord))
        nan_mask = np.isnan(derivative)
        # Filter out NaN elements using the mask
        derivative = derivative[~nan_mask]
        if len(derivative)>0:
            position_min = np.argmax(abs(derivative))
            delta_x = 1/100000*x_coord[position_min]
            position_label = np.abs(x_coord - delta_x).argmin()
            delta_x = x_coord[position_label]
            delta_y = y_coord[position_label]
            label_angle = np.arctan(derivative[position_label])
        else:
            #If curve seems problematic, take delta_x delta_y out of plot, label angle 0
            delta_x = 1.e-5*fmin
            delta_y = 1.e-5*min(hmin,Omegamin)
            label_angle = 0.

        y_coord_h = y_coord
        delta_y_h = delta_y
        delta_x_h = delta_x

        curves_dict['PBHs']['yCurve_PBHs'] = y_coord
        curves_dict['PBHs']['annotation_x_PBHs'] = delta_x
        curves_dict['PBHs']['annotation_y_PBHs'] = delta_y
        curves_dict['PBHs']['label_angle_PBHs'] = label_angle

        #Change values of Omega
        y_coord = 2.737E36*(x_coord**2)*(y_coord**2)
        delta_y = 2.737E36*(delta_x**2)*(delta_y**2)

        curves_dict_Omega['PBHs']['yCurve_PBHs'] = y_coord
        curves_dict_Omega['PBHs']['annotation_x_PBHs'] = delta_x
        curves_dict_Omega['PBHs']['annotation_y_PBHs'] = delta_y
        curves_dict_Omega['PBHs']['label_angle_PBHs'] = label_angle

        #Change values of Sh
        y_coord = y_coord_h**2/x_coord
        delta_y = delta_y_h**2/delta_x_h

        curves_dict_Sh['PBHs']['yCurve_PBHs'] = y_coord
        curves_dict_Sh['PBHs']['annotation_x_PBHs'] = delta_x
        curves_dict_Sh['PBHs']['annotation_y_PBHs'] = delta_y
        curves_dict_Sh['PBHs']['label_angle_PBHs'] = label_angle

        # Update the shared data source when the slider changes
        if what_to_plot == 0:
            plot_source_curves.data['yCurve_PBHs'] = curves_dict['PBHs']['yCurve_PBHs']
        elif what_to_plot == 1:
            plot_source_curves.data['yCurve_PBHs'] = curves_dict_Omega['PBHs']['yCurve_PBHs']
        elif what_to_plot == 2:
            plot_source_curves.data['yCurve_PBHs'] = curves_dict_Sh['PBHs']['yCurve_PBHs']

        annotation_source.data = update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)


    # Define a callback function for the phase transition sliders
    def update_MPBH(attr, old, new):
        nonlocal MPBH
        MPBH = 10**slider_PBH.value
        update_plot_PBH()


    # Attach the Python function to the 'value' change event of the slider
    slider_PBH.on_change('value', update_MPBH)



    #####################################
    #####################################
    #####################################
    #Handling changes in CGMB temperature
    def update_plot_CGMB():
        nonlocal plot_source_curves
        nonlocal annotation_source

        # Update the curves dict and plot based on the global variables of phase transitions
        x_coord = curves_dict['CGMB']['xCurve_CGMB']
        y_coord = np.sqrt(TCGMB/Mp)*curves_dict['CGMB']['yCurve_CGMB']
        #For CGMB  we compute label position and angle near peak
        position_max = np.argmax(y_coord)
        delta_x = 5.*x_coord[position_max]
        position_label = np.abs(x_coord - delta_x).argmin()
        delta_x = x_coord[position_label]
        delta_y = y_coord[position_label]
        label_angle = 0

        #As we compute everything wrt to Planck spectrum, we keep it in curves dict so we don't update it to current TCGMB
        curves_dict['CGMB']['annotation_x_CGMB'] = delta_x
        curves_dict['CGMB']['annotation_y_CGMB'] = delta_y
        curves_dict['CGMB']['label_angle_CGMB'] = label_angle

        y_coord_h = y_coord
        delta_y_h = delta_y

        #Coords Omega
        delta_y = 2.737E36*(delta_x**2)*(delta_y**2)


        #curves_dict_Omega['CGMB']['yCurve_CGMB'] = y_coord
        curves_dict_Omega['CGMB']['annotation_x_CGMB'] = delta_x
        curves_dict_Omega['CGMB']['annotation_y_CGMB'] = delta_y
        curves_dict_Omega['CGMB']['label_angle_CGMB'] = label_angle


        #Coords Sh
        delta_y = delta_y_h**2/delta_x
        curves_dict_Sh['CGMB']['annotation_x_CGMB'] = delta_x
        curves_dict_Sh['CGMB']['annotation_y_CGMB'] = delta_y
        curves_dict_Sh['CGMB']['label_angle_CGMB'] = label_angle


        # Update the shared data source when the slider changes
        if what_to_plot == 0:
            plot_source_curves.data['yCurve_CGMB'] = y_coord
        elif  what_to_plot == 1:
            y_coord = 2.737E36*(x_coord**2)*(y_coord**2)
            plot_source_curves.data['yCurve_CGMB'] = y_coord
        elif  what_to_plot == 2:
            y_coord = y_coord_h**2/x_coord
            plot_source_curves.data['yCurve_CGMB'] = y_coord

        annotation_source.data = update_annotation_angles(curves_dict, curves_dict_Omega, curves_dict_Sh, what_to_plot, annotation_source, fig, fmin, fmax, hmin, hmax, Omegamin, Omegamax, Shmin, Shmax)


    # Define a callback function for the phase transition sliders
    def update_TCGMB(attr, old, new):
        nonlocal TCGMB
        TCGMB = 10.**slider_CGMB.value
        update_plot_CGMB()


    # Attach the Python function to the 'value' change event of the slider
    slider_CGMB.on_change('value', update_TCGMB)




    # Add the layout to the Bokeh document
    final_layout = column(layout,  Div(text="<div style='height: 10px; background-color: black; width: 100%;'></div>"), row(layout_size,Div(text="<div style='width: 10px; background-color: black; height: 100%;'></div>"), layout2, Div(text="<div style='width: 10px; background-color: black; height: 100%;'></div>"), column(layout_CGMB,layout_cosmic_strings, layout_PBH)), sizing_mode="scale_both")
    doc.add_root(final_layout)



plot_app = Application(FunctionHandler(bokeh_plot_app))


#Below, use either code to use with flask or tornado
###########################################
##CODE TO RUN WITH FLASK INTEGRATED SERVER
###########################################
# Start Flask app in a separate thread
flask_thread = Thread(target=lambda: app.run(debug=True, port=5003, use_reloader=False))
flask_thread.start()

# Create and start a single Bokeh server with the different apps with different urls
server = Server({'/plot': plot_app}, io_loop=IOLoop.current(), allow_websocket_origin=["localhost:5006","127.0.0.1:5006","localhost:5003","127.0.0.1:5003"], port=5006)
server.start()




if __name__ == '__main__':
    #print('Opening Bokeh application on http://localhost:5006/')
    #server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
    #print('Opening Bokeh application on http://localhost:5007/')
    #server2.io_loop.start()
    # Join threads
    flask_thread.join()

