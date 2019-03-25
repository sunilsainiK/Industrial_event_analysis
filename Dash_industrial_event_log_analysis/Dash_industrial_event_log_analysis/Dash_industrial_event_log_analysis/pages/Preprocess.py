import dash
import dash_table
import pandas as pd
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import plotly.plotly as py
from plotly import figure_factory as FF



def preprocess():
    prep='prepackage=PreProcessing'
    r  = requests.get("http://127.0.0.1:5000/preprocess",params=prep)
    print(r.text)

layout =html.Div('hello')
