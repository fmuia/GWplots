# Standard libraries

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import hvplot.pandas
from matplotlib.pyplot import cm
plt.rcParams['text.usetex'] = True

# Panel

import panel as pn
from panel.interact import interact
pn.extension()

# Bokeh

from bokeh.models import ColumnDataSource, Div, Spacer, BoxAnnotation, Toggle, Slider, RangeSlider, CustomJS
from bokeh.models.formatters import CustomJSTickFormatter
from bokeh.plotting import figure, show
from bokeh.models.widgets import RangeSlider
from bokeh.layouts import layout
from bokeh.resources import INLINE

import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models import RangeSlider, CustomJSTickFormatter, CustomJS, ColumnDataSource
from bokeh.layouts import layout
from bokeh.io import output_file, show
from bokeh.embed import components
from bokeh.models import VArea
from flask import Flask, render_template, request, jsonify

# Import necessary libraries
from bokeh.models import RangeSlider, CustomJSTickFormatter, CustomJS, Slider  # Ensure Slider is imported

##Import SMASH benchmarks

inflation_1_data=np.loadtxt('SignalCurves/CosmologicalSources/hc_inflation_SMASH/hc_inflation_SMASH_benchmark_1', dtype=float)
inflation_2_data=np.loadtxt('SignalCurves/CosmologicalSources/hc_inflation_SMASH/hc_inflation_SMASH_benchmark_2', dtype=float)
preheating_1_data=np.loadtxt('SignalCurves/CosmologicalSources/hc_inflation_SMASH/hc_preheating_SMASH_benchmark_1', dtype=float)
preheating_2_data=np.loadtxt('SignalCurves/CosmologicalSources/hc_inflation_SMASH/hc_preheating_SMASH_benchmark_2', dtype=float)
thermal_1_data=np.loadtxt('SignalCurves/CosmologicalSources/hc_inflation_SMASH/hc_thermal_SMASH_benchmark_1', dtype=float)
thermal_2_data=np.loadtxt('SignalCurves/CosmologicalSources/hc_inflation_SMASH/hc_thermal_SMASH_benchmark_2', dtype=float)

# Load Omega data for stochastic signal from PBHs.

data_PBH6_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass6.csv', delimiter=',', dtype=float)
data_PBH7_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass7.csv', delimiter=',', dtype=float)
data_PBH8_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass8.csv', delimiter=',', dtype=float)
data_PBH9_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass9.csv', delimiter=',', dtype=float)
data_PBH10_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass10.csv', delimiter=',', dtype=float)
data_PBH11_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass11.csv', delimiter=',', dtype=float)
data_PBH12_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass12.csv', delimiter=',', dtype=float)
data_PBH13_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass13.csv', delimiter=',', dtype=float)
data_PBH14_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass14.csv', delimiter=',', dtype=float)
data_PBH15_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass15.csv', delimiter=',', dtype=float)
data_PBH16_Omega = np.loadtxt('SignalCurves/PBHs/Stochastic/PBH_StochasticOmega_mass16.csv', delimiter=',', dtype=float)

# Generate hc data.

data_PBH6_Strain = np.concatenate((data_PBH6_Omega[:,0].reshape(data_PBH6_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH6_Omega[:,0]/10**9)**(-1)*(data_PBH6_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH6_Omega[:,0].shape[0],1)), axis = 1)
data_PBH7_Strain = np.concatenate((data_PBH7_Omega[:,0].reshape(data_PBH7_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH7_Omega[:,0]/10**9)**(-1)*(data_PBH7_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH7_Omega[:,0].shape[0],1)), axis = 1)
data_PBH8_Strain = np.concatenate((data_PBH8_Omega[:,0].reshape(data_PBH8_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH8_Omega[:,0]/10**9)**(-1)*(data_PBH8_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH8_Omega[:,0].shape[0],1)), axis = 1)
data_PBH9_Strain = np.concatenate((data_PBH9_Omega[:,0].reshape(data_PBH9_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH9_Omega[:,0]/10**9)**(-1)*(data_PBH9_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH9_Omega[:,0].shape[0],1)), axis = 1)
data_PBH10_Strain = np.concatenate((data_PBH10_Omega[:,0].reshape(data_PBH10_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH10_Omega[:,0]/10**9)**(-1)*(data_PBH10_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH10_Omega[:,0].shape[0],1)), axis = 1)
data_PBH11_Strain = np.concatenate((data_PBH11_Omega[:,0].reshape(data_PBH11_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH11_Omega[:,0]/10**9)**(-1)*(data_PBH11_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH11_Omega[:,0].shape[0],1)), axis = 1)
data_PBH12_Strain = np.concatenate((data_PBH12_Omega[:,0].reshape(data_PBH12_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH12_Omega[:,0]/10**9)**(-1)*(data_PBH12_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH12_Omega[:,0].shape[0],1)), axis = 1)
data_PBH13_Strain = np.concatenate((data_PBH13_Omega[:,0].reshape(data_PBH13_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH13_Omega[:,0]/10**9)**(-1)*(data_PBH13_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH13_Omega[:,0].shape[0],1)), axis = 1)
data_PBH14_Strain = np.concatenate((data_PBH14_Omega[:,0].reshape(data_PBH14_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH14_Omega[:,0]/10**9)**(-1)*(data_PBH14_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH14_Omega[:,0].shape[0],1)), axis = 1)
data_PBH15_Strain = np.concatenate((data_PBH15_Omega[:,0].reshape(data_PBH15_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH15_Omega[:,0]/10**9)**(-1)*(data_PBH15_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH15_Omega[:,0].shape[0],1)), axis = 1)
data_PBH16_Strain = np.concatenate((data_PBH16_Omega[:,0].reshape(data_PBH16_Omega[:,0].shape[0],1), (2*10**-31*(data_PBH16_Omega[:,0]/10**9)**(-1)*(data_PBH16_Omega[:,1]/10**-7)**(1/2)).reshape(data_PBH16_Omega[:,0].shape[0],1)), axis = 1)

data_PBH = (data_PBH6_Strain, data_PBH7_Strain, data_PBH8_Strain, data_PBH9_Strain, data_PBH10_Strain, data_PBH11_Strain, data_PBH12_Strain, data_PBH13_Strain, data_PBH14_Strain, data_PBH15_Strain, data_PBH16_Strain)

## Import data

dataBAW = np.loadtxt('../DetectorCurves/BAW.txt', delimiter=',', dtype=float)
dataLSDweak = np.loadtxt('../DetectorCurves/LSDweak.txt', delimiter=',', dtype=float)
dataLSDstrong = np.loadtxt('../DetectorCurves/LSDstrong.txt', delimiter=',', dtype=float)
dataStrongARCADE = np.loadtxt('../DetectorCurves/StrongARCADE.txt', delimiter=',', dtype=float)
dataWeakARCADE = np.loadtxt('../DetectorCurves/WeakARCADE.txt', delimiter=',', dtype=float)
dataIAXOSPD = np.loadtxt('../DetectorCurves/IAXOSPD.txt', delimiter=',', dtype=float)
dataIAXOHET = np.loadtxt('../DetectorCurves/IAXOHET.txt', delimiter=',', dtype=float)
dataIAXO = np.loadtxt('../DetectorCurves/IAXO.txt', delimiter=',', dtype=float)
dataALPSII = np.loadtxt('../DetectorCurves/ALPSII.txt', delimiter=',', dtype=float)
dataJURA = np.loadtxt('../DetectorCurves/JURA.txt', delimiter=',', dtype=float)
dataOSQAR = np.loadtxt('../DetectorCurves/OSQAR.txt', delimiter=',', dtype=float)
dataCAST = np.loadtxt('../DetectorCurves/CAST.txt', delimiter=',', dtype=float)
dataHOL = np.loadtxt('../DetectorCurves/HOL.txt', delimiter=',', dtype=float)
dataAkutsu = np.loadtxt('../DetectorCurves/Akutsu.txt', delimiter=',', dtype=float)
dataMagnonLow = np.loadtxt('../DetectorCurves/MagnonLow.txt', delimiter=',', dtype=float)
dataMagnonHigh = np.loadtxt('../DetectorCurves/MagnonHigh.txt', delimiter=',', dtype=float)
dataEDGESstrong = np.loadtxt('../DetectorCurves/EDGESstrong.txt', delimiter=',', dtype=float)
dataEDGESweak = np.loadtxt('../DetectorCurves/EDGESweak.txt', delimiter=',', dtype=float)


dataADMX = np.loadtxt('../DetectorCurves/ADMX.txt', delimiter=',', dtype=float)
dataHAYSTAC = np.loadtxt('../DetectorCurves/HAYSTAC.txt', delimiter=',', dtype=float)
dataCAPP = np.loadtxt('../DetectorCurves/CAPP.txt', delimiter=',', dtype=float)
dataSQMS = np.loadtxt('../DetectorCurves/SQMS.txt', delimiter=',', dtype=float)

dataGaussianBeamWeak = np.loadtxt('../DetectorCurves/GaussianBeamWeak.txt', delimiter=',', dtype=float)

dataGaussianBeamStrong = np.loadtxt('../DetectorCurves/GaussianBeamStrong.txt', delimiter=',', dtype=float)

##Import data with 1 point bound (narrow)
dataORGAN = np.loadtxt('../DetectorCurves/ORGAN.txt', delimiter=',', dtype=float)

## Import more complex data curves
dataNamur = np.loadtxt('../DetectorCurves/ResonantAntennas.txt', dtype=float)
dataDMR8=  np.loadtxt('../DetectorCurves/DMR8.txt', dtype=float)
dataDMR100=  np.loadtxt('../DetectorCurves/DMR100.txt', dtype=float)



########################
#Direct bounds
dataDirectBounds=[ dataBAW, dataHOL, dataAkutsu, dataMagnonLow, dataMagnonHigh, dataOSQAR, dataCAST]
labelDirectBounds= ["BAW", "HOL", "Akutsu", "MagnonLow", "MagnonHigh", "OSQAR", "CAST"]

clearer='#fd94aeff'

darker='#da76a2ff'

colorDirectBounds = [darker,clearer,clearer,clearer, clearer,clearer,clearer]
opacityDirectBounds = [1,1,1,1,1,1,1]
levelDirectBounds = ["glyph" for _ in range(len(dataDirectBounds)) ]

#####################
#Indirect bounds
dataIndirectBounds=[dataStrongARCADE, dataWeakARCADE,  dataEDGESstrong,  dataEDGESweak]
labelIndirectBounds=["ARCADEstrong", "ARCADEweak", "EDGESstrong",  "EDGESweak"]


colorIndirectBounds = ['darkgreen','green', 'darkgreen','green']
opacityIndirectBounds = [.5,.5,.5,.5]
levelIndirectBounds = [ "underlay", "underlay", "glyph", "glyph"]

#####################
#Projected bounds
dataProjections = [ dataLSDstrong, dataLSDweak, dataIAXO, dataJURA,  dataALPSII,  dataIAXOHET, dataIAXOSPD, dataADMX, dataHAYSTAC, dataCAPP, dataSQMS, dataORGAN, dataGaussianBeamWeak, dataGaussianBeamStrong ]
labelProjections = ["LSDstrong", "LSDweak", "IAXO", "JURA",  "ALPSII",  "IAXOHET", "IAXOSPD", "ADMX", "HAYSTAC", "CAPP", "SQMS", "ORGAN", "GaussianBeamWeak", "GaussianBeamStrong" ]

#Data Projections  dataLSDstrong, dataLSDweak, dataIAXO, dataJURA,  dataALPSII,  dataIAXOHET, dataIAXOSPD, dataADMX, dataHAYSTAC, dataCAPP, dataSQMS, dataORGAN dataGaussianBeamWeak dataGaussianBeamStrong
colorProjections = ['#fd94aeff','#da76a2ff','#da76a2ff','#fd94aeff','#da76a2ff','#da76a2ff','#fd94aeff', '#bd618aff','#fd94aeff', '#da76a2ff', '#fd94aeff', '#da76a2ff', '#da76a2ff', '#da76a2ff']

def linestylesProjections(x):
    if (x==13):
        return('dashed')
    else:
        return('solid')

dataProjetionsCurves = [ dataNamur, dataDMR8, dataDMR100 ]

######ET

file_ET = open("../DetectorCurves/plis_ET.dat","r")
file_ET_list = file_ET.readlines()
ET_data = np.array([[float(val) for val in line.split()] for line in file_ET_list[14:]])
file_ET.close()

######LISA

file_LISA = open("../DetectorCurves/plis_LISA.dat","r")
file_LISA_list = file_LISA.readlines()
LISA_data = np.array([[float(val) for val in line.split()] for line in file_LISA_list[14:]])
file_LISA.close()

######DECIGO

file_DECIGO = open("../DetectorCurves/plis_DECIGO.dat","r")
file_DECIGO_list = file_DECIGO.readlines()
DECIGO_data = np.array([[float(val) for val in line.split()] for line in file_DECIGO_list[14:]])
file_DECIGO.close()

######CE

file_CE = open("../DetectorCurves/plis_CE.dat","r")
file_CE_list = file_CE.readlines()
CE_data = np.array([[float(val) for val in line.split()] for line in file_CE_list[14:]])
file_CE.close()

######BBO

file_BBO = open("../DetectorCurves/plis_BBO.dat","r")
file_BBO_list = file_BBO.readlines()
BBO_data = np.array([[float(val) for val in line.split()] for line in file_BBO_list[14:]])
file_BBO.close()

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

# Global set to keep track of "on" buttons
on_buttons = set()

# Global ColumnDataSource to manage plot data
plot_source = ColumnDataSource(data=dict(x=[], y=[]), name='plot_source')

# Connect plot_source to fig using the line glyph method
#fig.line(x='x', y='y', source=plot_source, line_width=2, alpha=0.8, legend_label="Data Line")
fig.line(x='x_BAW', y='y_BAW', source=plot_source, line_width=2, alpha=0.8, legend_label="BAW")
fig.line(x='x_LSDweak', y='y_LSDweak', source=plot_source, line_width=2, alpha=0.8, legend_label="LSD weak")
fig.line(x='x_LSDstrong', y='y_LSDstrong', source=plot_source, line_width=2, alpha=0.8, legend_label="LSDstrong")

# Define the global variable
on_buttons = []

# Define the initial dictionary
curves_dict = {
    'BAW': {'x': dataBAW[:,0], 'y': dataBAW[:,1]},
    'LSDweak': {'x': dataLSDweak[:,0], 'y': dataLSDweak[:,1]},
    'LSDstrong': {'x': dataLSDstrong[:,0], 'y': dataLSDstrong[:,1]}
}

def update_plot(button_label):
    global on_buttons  # Declare on_buttons as global to modify it

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
            result_dict[f'{key}_{btn}'] = value

    print(result_dict)

    return result_dict


app = Flask(__name__)

@app.route('/')
def index():
    script, div = components(layout([fig, range_slider_x, range_slider_y, slider_width, slider_height]))
    return render_template(
        'table.html',
        script=script,
        div=div,
        bokeh_css=INLINE.render_css(),
        bokeh_js=INLINE.render_js()
    )

@app.route('/update_plot', methods=['GET'])
def update_plot_route():
    button_label = request.args.get('button_label')
    new_data = update_plot(button_label)  # Call the update_plot function and update new_data
    print(f'New Data: {new_data}')  # Debugging line
    return jsonify(new_data)  # Return new_data to the client

if __name__ == '__main__':
    app.run(debug=True, port=5001)

