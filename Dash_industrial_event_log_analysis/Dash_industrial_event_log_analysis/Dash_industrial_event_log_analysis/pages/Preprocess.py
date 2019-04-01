import dash
import dash_table
import pandas as pd
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
import plotly.plotly as py
from plotly import figure_factory as FF
import re
prep='prepackage=PreProcessing'
r  = requests.get("http://127.0.0.1:5000/preprocess",params=prep)
list =re.split(',',r.text)
print (list)
def button_values(list):
    i=1
    btn_values =[]
    for i in range (len(list)):
       if not  list[i]=='':
           value=list[i]
           btn_values.append(html.Div(html.Button(list[i] ,id='id_0_'+str(i) ,title=value, n_clicks=0, style={'width':'80%',
                                                                                   'margin-top':'4%',
                                                                                   'margin-left':'4%',
                                                                                   'margin-bottom':'4%' }),
                                                                                   className="row"))
           print (btn_values)
    return btn_values



layout = html.Div(
       html.Div([html.H1(children='Industrial Event Log Analysis',style={
                                                                  'padding-left': '2.0%',
                                                                  'padding-right': '2.0%',
                                                                  'border':'solid',
                                                                  #'background-color':'DodgerBlue',
                                                                  'text-align':'center'                                                                                  }
                 ),
                   html.Div([html.H2(children='Preprocessing',style={
                                                            'padding-left': '2.0%',
                                                            'padding-right': '2.0%',
                                                             'margin-top':'2%',

                                                             'border':'solid',
                                                             #'background-color':'DodgerBlue',
                                                             'text-align':'center'
                                                               })
                                                               ]),
                html.Div(html.Div(button_values(list)),
#                         html.Div(info(list)),
                         style={'width':'20%','margin-top':'2%','margin-left':'2%', 'border':'solid'}),





              ]),

)
