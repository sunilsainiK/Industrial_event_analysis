import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

import dash_core_components as dcc
import dash_html_components as html


layout = html.Div(html.A((html.Button('Next',id='Event_epi',type='submit')),href ='/Preprocess'))
