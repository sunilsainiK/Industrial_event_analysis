
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as  pd
import dash_table
import datetime
import requests
import json
from pages import data_sample, EDAinfo, sentimental_info, Event_episode_info
from app import app

data_summary_layout = html.Div([html.H1(children='Industrial Event Log Analysis',style={
                                                                                   'padding-left': '2.0%',
                                                                                   'padding-right': '2.0%',
                                                                                   'border':'solid',
                                                                                   #'background-color':'DodgerBlue',
                                                                                   'text-align':'center'}),
                           html.Div([
                              html.H2(children='Data',style={'padding-left': '2.0%',
                                                                'padding-right': '2.0%',
                                                                 'margin-top':'2%',
                                                                 'border':'solid',
                                                                 #'background-color':'DodgerBlue',
                                                                 'text-align':'center'
                                                                                }),
                                html.A(html.Button('Back',id='b-btn',style={'text-align':'left'}),href='/files_page.py'),
                            ]),
                                        html.Hr(),
                                        dcc.Tabs(id="Tabs", value='tab-value',
                                             children=[
                                             dcc.Tab(id='Data', label='Data', value='Data_value'),
                                             dcc.Tab(id='EDA', label='EDA', value='EDA_value'),
                                             dcc.Tab(id='Event_value', label='Event Episode Classification', value='Event_value'),
                                             dcc.Tab(id='Sentimental_value', label='Sentimental Analysis', value='sentimental_value')
                                            ]),
                                               html.Div(id='tabs-content'),

                          html.A(html.Button('Next',id='n-btn',style={'text-align':'right','margin-left':'86.6%'}),href='/Preprocess')


])

@app.callback(Output('tabs-content', 'children'),
              [Input('Tabs', 'value')])
def render_content(tab):
    if tab == 'Data_value':
       return  data_sample.data_raw_sample
    elif tab == 'EDA_value':
        return EDAinfo.layout
    elif tab == 'sentimental_value':
       return sentimental_info.layout
    else:
        return data_sample.data_raw_sample
