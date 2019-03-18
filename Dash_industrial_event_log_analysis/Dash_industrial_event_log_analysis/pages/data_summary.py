
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
#def data_content():
#    url_dataraw_dash = 'http://127.0.0.1:5000/data_summary'
#    summ_Df_1_flask = requests.get(url_dataraw_dash)
#    if summ_Df_1_flask:
#       data = summ_Df_1_flask.json()
#       df = pd.DataFrame(data)
#       return html.Div(['hello'])
#    else:
#         return html.Div(['hi'])

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
                                        ]),
                                        dcc.Tabs(id="Tabs", value='tab-value',
                                             children=[
                                             dcc.Tab(id='Data', label='Data', value='Data_value'),
                                             dcc.Tab(id='EDA', label='EDA', value='EDA_value'),
                                             dcc.Tab(id='Event_value', label='Event Episode Classification', value='Event_value'),
                                             dcc.Tab(id='sentimental_value', label='Sentimental Analysis', value='sentimental_value')
                                            ]),
                                               html.Div(id='tabs-content')




])

@app.callback(Output('tabs-content', 'children'),
              [Input('Tabs', 'value')])
def render_content(tab):
    if tab == 'Data_value':
       return  data_sample.data_raw_sample
    elif tab == 'EDA_value':
        return EDAinfo.layout
    elif tab == 'Event_value':
        return Event_episode_info.layout
    elif tab == 'sentimental_value':
       return sentimental_info.layout
    else:
        return EDAinfo.layout
