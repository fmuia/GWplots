# imports.py

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
from bokeh.plotting import figure, curdoc
from bokeh.models import RangeSlider, CustomJSTickFormatter, CustomJS, ColumnDataSource
from bokeh.layouts import layout
from bokeh.io import output_file, show
from bokeh.embed import components
from bokeh.models import VArea

# Flask
from flask import Flask, render_template, request, jsonify

# Import necessary libraries
from bokeh.models import RangeSlider, CustomJSTickFormatter, CustomJS, Slider  # Ensure Slider is imported

