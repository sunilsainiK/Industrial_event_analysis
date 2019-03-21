import dash
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import requests

import dash_core_components as dcc
import dash_html_components as html



def EDA_content():
    r  = requests.get("http://127.0.0.1:5000/Algo_info",'EDA')
    print(r)
    return r.content

layout = EDA_content()
