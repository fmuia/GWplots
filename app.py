#app.py

# Import all the relevant libraries and packages

from aux.imports import *
from bokeh.models import SaveTool
from aux.data_files import detector_data,signal_data
from aux.aux_functions import load_and_categorize_data
from aux.aux_functions import create_sliders
from aux.aux_functions import create_curves_dict
from aux.aux_functions import add_curves_to_plot
from aux.aux_functions import update_plot

# Define the on_buttons variable
on_buttons = []

## Load detector curves

# Load data into Data class instances collected in the dictionary data_instances
# Create a dictionary category_dict containing the experiment labels divided into categories (Indirect bounds, Direct bounds, Projected bounds)

data_instances, category_dict = load_and_categorize_data(detector_data, signal_data)
 
# print('This are the data instances:')
#
# print(data_instances['BAW'].x_coord)
# print(data_instances['BAW'].y_coord)
# print(data_instances['BAW'].color)
# print(data_instances['BAW'].depth)

print('This is the category dictionary:')
print(category_dict)
#print(data_instances['BAW'].x_coord)
#print(category_dict)






## Load signal curves






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
             tools='save')
fig.output_backend = "svg"
fig.xgrid.level = 'image'
fig.ygrid.level = 'image'

# Set up the sliders

slider_x, slider_y, slider_width, slider_height = create_sliders(fig)

# Create dictionary of curves

curves_dict = create_curves_dict(data_instances, category_dict, hmax)
#print('This is the curves dictionary:')
#print(curves_dict)

# Global ColumnDataSource to manage plot data
plot_source = ColumnDataSource(data=dict(), name='plot_source')
plot_source_proj = ColumnDataSource(data=dict(), name='plot_source_proj')
plot_source_proj_curves = ColumnDataSource(data=dict(), name='plot_source_proj_curves')

# Link curves to a chart
add_curves_to_plot(fig, curves_dict, category_dict, plot_source, plot_source_proj, plot_source_proj_curves)

## Define app section

# Initialize app
app = Flask(__name__)

@app.route('/')
def index():
    script, div = components(layout([fig, slider_x, slider_y, slider_width, slider_height]))
    return render_template(
        'index.html',
        script=script,
        div=div,
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

if __name__ == '__main__':
    app.run(debug = True, port=5001)
