import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import requests
import bs4 as bs
import dash_core_components as dcc
import dash_html_components as html

def EDA_content():
    folder='folder=EDA'
    r  = requests.get("http://127.0.0.1:5000/Algo_info",params=folder)
    return html.Div(html.Iframe(srcDoc=r.text,style={'width':'80%','height':'100%'},draggable='yes'),style={'margin-top':'20'})
layout = EDA_content()
