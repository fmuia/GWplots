#app.py

# Import all the relevant libraries and packages

from aux.imports import *


from aux.data_files import detector_data,signal_data
from aux.aux_functions import load_and_categorize_data
from aux.aux_functions import create_sliders
from aux.aux_functions import create_curves_dict
from aux.aux_functions import add_curves_to_plot
from aux.aux_functions import update_plot
from aux.aux_functions import Tstar
from aux.aux_functions import alpha
from aux.aux_functions import betaOverH
from aux.aux_functions import vw
from aux.aux_functions import Tstarchanged
from aux.aux_functions import alphachanged
from aux.aux_functions import betaOverHchanged
from aux.aux_functions import vwchanged
from aux.aux_functions import gstar
from aux.signal_functions import hPT

from bokeh.models import SaveTool

# Initialize app
app = Flask(__name__)
# Define global variables
fig = None
slider_x = None
slider_y = None
slider_width = None
slider_height = None
slider_pt_temp = None
slider_pt_alpha = None
slider_pt_betaOverH = None
slider_pt_vw = None
category_dict = None
curves_dict = None


# Define the global variable
data_instances = {}

# Define the on_buttons variable
on_buttons = []



# Global ColumnDataSource to manage plot data
plot_source = ColumnDataSource(data=dict(), name='plot_source')
plot_source_proj = ColumnDataSource(data=dict(), name='plot_source_proj')
plot_source_proj_curves = ColumnDataSource(data=dict(), name='plot_source_proj_curves')


# Set up the figure


hmin = 10.**-35.
hmax = 10.**-10.
xrange=(10**-18, 10**20)
fig = figure(background_fill_color='white',
border_fill_color='black',
border_fill_alpha=0.0,
height=600,
width=int(900),
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
tools='save',name = 'myplot')
fig.output_backend = "svg"
fig.xgrid.level = 'image'
fig.ygrid.level = 'image'


def create_bokeh_plot():
    global fig, slider_x, slider_y, slider_width,  slider_height, slider_pt_temp, slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw, category_dict, data_instances, curves_dict, on_buttons, layout, layout2
    # Import all the relevant libraries and packages

## Load detector curves

    # Load data into Data class instances collected in the dictionary data_instances
    # Create a dictionary category_dict containing the experiment labels divided into categories (Indirect bounds, Direct bounds, Projected bounds)

    data_instances, category_dict = load_and_categorize_data(detector_data, signal_data)

    #print('This are the data instances:')
    #
    #print(data_instances['HOL'].comment)
    # print(data_instances['BAW'].y_coord)
    # print(data_instances['BAW'].color)
    # print(data_instances['BAW'].depth)

    #print('This is the category dictionary:')
    #print(category_dict)



    # Set up the sliders

    slider_x, slider_y, slider_width,  slider_height, slider_pt_temp,  slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw = create_sliders(fig, Tstar)


    # Create dictionary of curves

    curves_dict = create_curves_dict(data_instances, category_dict, hmax)
    #print('This is the curves dictionary:')
    #print(curves_dict)


    # Link curves to a chart
    add_curves_to_plot(fig, curves_dict, category_dict, plot_source, plot_source_proj, plot_source_proj_curves)

    #Main plot with range/size sliders
    layout = column(fig, slider_x, slider_y,  slider_width, slider_height)
    #Sliders for phase transition parameters
    layout2 = column(slider_pt_temp, slider_pt_alpha, slider_pt_betaOverH, slider_pt_vw)






create_bokeh_plot()


## Define app section

@app.route('/get_comments')
def get_comments():
    label = request.args.get('label')
    data_instance = data_instances.get(label, None)
    comment = data_instance.comment if data_instance and data_instance.comment not in [None, ''] else None
    
    return jsonify({'comment': comment})

# Flask route to serve the HTML template with the initial Bokeh plot
@app.route('/')
def index():
    # Generate script tags for Bokeh content
    # Get the session ID for the Bokeh server session

    #script main plot and range/size sliders
    script_bokeh_plot = server_document(url='http://127.0.0.1:5006/plot')
    #script phase transition sliders
    script_bokeh_phase_transition = server_document(url='http://127.0.0.1:5006/phase_transition')


    return render_template(
        'index.html',
        script_bokeh_plot = script_bokeh_plot,
        script_bokeh_phase_transition =  script_bokeh_phase_transition,
        #script=script,
        #div=div,
        #div_pt = div_pt,
        #script_pt = script_pt,
        bokeh_css=INLINE.render_css(),
        bokeh_js=INLINE.render_js(),
        category_dict=category_dict
    )


@app.route('/update_plot', methods=['GET'])
def update_plot_route():
    global on_buttons
    button_label = request.args.get('button_label')
    new_data, on_buttons = update_plot(button_label, curves_dict, on_buttons)  # Call the update_plot function and update new_data
    #print(f'New Data: {new_data}')  # Debugging line
    return jsonify(new_data)  # Return new_data to the client



#Bokeh app for main plot with range, size sliders
def bokeh_plot_app(doc):

    def update_plot_phase_transition():
        global Tstar
        global Tstarchanged, alphachanged, betaOverHchanged, vwchanged
        global plot_source_proj_curves
        global curves_dict
        # Update the curves dict and plot based on the global variables of phase transitions
        if (Tstarchanged == 1) or (alphachanged == 1) or (betaOverHchanged == 1) or (vwchanged == 1):
            Tstarchanged = 0
            alphachanged = 0
            betaOverHchanged = 0
            vwchanged = 0
            x_coord =curves_dict['1st-order phase transition']['xCurve_1st-order phase transition']
            y_coord = np.array(hPT(Tstar, alpha, betaOverH, vw, gstar, x_coord))
            curves_dict['1st-order phase transition']['yCurve_1st-order phase transition'] = y_coord
            if '1st-order phase transition' in on_buttons:
                # Update the shared data source when the slider changes
                plot_source_proj_curves.data['yCurve_1st-order phase transition'] = y_coord

    # Schedule periodic updates (every 100 milliseconds)
    doc.add_periodic_callback(update_plot_phase_transition, 100)

    # Add the layout to the Bokeh document
    doc.add_root(layout)



#Bokeh app with sliders for phase transitions
def bokeh_phase_transition_app(doc):
    # Define a callback function for the phase transition sliders
    def update_tstar(attr, old, new):
        global Tstar, Tstarchanged
        Tstar = 10**slider_pt_temp.value
        Tstarchanged = 1
    def update_alpha(attr, old, new):
        global alpha, alphachanged
        alpha = 10**slider_pt_alpha.value
        alphachanged = 1
    def update_betaOverH(attr, old, new):
        global betaOverH, betaOverHchanged
        betaOverH = 10**slider_pt_betaOverH.value
        betaOverHchanged = 1
    def update_vw(attr, old, new):
        global vw, vwchanged
        vw = slider_pt_vw.value
        vwchanged = 1



    # Attach the Python function to the 'value' change event of the slider
    slider_pt_temp.on_change('value', update_tstar)
    slider_pt_alpha.on_change('value', update_alpha)
    slider_pt_betaOverH.on_change('value', update_betaOverH)
    slider_pt_vw.on_change('value', update_vw)
    # Add the layout to the Bokeh document
    doc.add_root(layout2)




plot_app = Application(FunctionHandler(bokeh_plot_app))
phase_transition_app = Application(FunctionHandler(bokeh_phase_transition_app))


# Start Flask app in a separate thread
flask_thread = Thread(target=lambda: app.run(debug=True, port=5003, use_reloader=False))
flask_thread.start()

# Create and start a single Bokeh server with the different apps with different urls
server = Server({'/plot': plot_app, '/phase_transition': phase_transition_app}, io_loop=IOLoop.current(), allow_websocket_origin=["localhost:5006","127.0.0.1:5006","localhost:5003","127.0.0.1:5003"], port=5006)
server.start()




if __name__ == '__main__':
    print('Opening Bokeh application on http://localhost:5006/')
    #server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
    #print('Opening Bokeh application on http://localhost:5007/')
    #server2.io_loop.start()
    # Join threads
    flask_thread.join()

