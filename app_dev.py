#app_dev.py

# Import all the relevant libraries and packages

from aux.imports import *
from aux.data_files import detector_data
from aux.aux_functions import load_and_categorize_data
from aux.aux_functions import create_sliders
from aux.aux_functions import create_curves_dict
from aux.aux_functions import update_plot

## Load detector curves

# Load data into Data class instances collected in the dictionary data_instances
# Create a dictionary category_dict containing the experiment labels divided into categories (Indirect bounds, Direct bounds, Projected bounds)

data_instances, category_dict = load_and_categorize_data(detector_data)

print(data_instances['BAW'].x_coord)
print(category_dict)






## Load signal curves






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

# Create dictionary of curves

curves_dict = create_curves_dict(data_instances)
print(curves_dict)

## Define app section

# Define the on_buttons variable
on_buttons = []

# Initialize app
app = Flask(__name__)

@app.route('/')
def index():
    script, div = components(layout([fig, slider_x, slider_y, slider_width, slider_height]))
    return render_template(
        'simple_layout.html',
        script=script,
        div=div,
        bokeh_css=INLINE.render_css(),
        bokeh_js=INLINE.render_js(),
	category_dict=category_dict
    )

@app.route('/update_plot', methods=['GET'])
def update_plot_route():
    button_label = request.args.get('button_label')
    new_data = update_plot(button_label, on_buttons, curves_dict)  # Call the update_plot function and update new_data
    print(f'New Data: {new_data}')  # Debugging line
    return jsonify(new_data)  # Return new_data to the client

if __name__ == '__main__':
    app.run(debug=True, port=5001)
