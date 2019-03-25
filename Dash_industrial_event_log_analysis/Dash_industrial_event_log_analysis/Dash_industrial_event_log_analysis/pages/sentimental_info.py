import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import requests
import dash_core_components as dcc
import dash_html_components as html


def Sentimental_content():
    sent_folder='folder=Sentimental_Analysis'
    r  = requests.get("http://127.0.0.1:5000/Algo_info",params=sent_folder)
    return (html.Div('HI'))

layout = Sentimental_content()
