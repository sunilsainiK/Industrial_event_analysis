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


df = pd.read_csv('df_raw')

prep='prepackage=PreProcessing'
r  = requests.get("http://127.0.0.1:5000/preprocess",params=prep)
list =re.split(',',r.text)

def button_values(list):
    i=1
    btn_values =[]
    for i in range (len(list)):
       if not  list[i]=='':
           value=list[i]
           btn_values.append(html.Div(html.Button(list[i] ,id='id_0_'+str(i) ,title=value, n_clicks=0, style={'width':'80%',
                                                                                   'margin-top':'4%',
                                                                                   'margin-left':'4%',
                                                                                   'margin-bottom':'4%'}),
                                                                                   className="row"))
    return btn_values


def info_prep(list):
    i=1
    btn = []
    for i in range (len(list)):
       if not  list[i]=='':
           value=list[i]
           btn.append(html.Div(html.Button('i' ,id=value ,title=value, n_clicks=0, style={'width':'1%','margin-top':'4%'})))
    return btn

layout = html.Div(
       html.Div([
                html.H1(children='Industrial Event Log Analysis',style={
                                                                  'padding-left': '2.0%',
                                                                  'padding-right': '2.0%',
                                                                  'border':'solid',
                                                                  #'background-color':'DodgerBlue',
                                                                  'text-align':'center'}
                 ),




                   html.Div([html.H2(children='Preprocessing',style={
                                                            'padding-left': '2.0%',
                                                            'padding-right': '2.0%',
                                                             'margin-top':'2%',
                                                             'border':'solid',
                                                             'text-align':'center'
                                                               }),]),



#Preprocessing lsit box
               html.Div([
                html.Div(html.H5(children='Preprocess Options', style={'border':'solid','width':'20%','text-align':'center'})),
                        html.Div([
                                html.Div(html.Div(button_values(list),className="seven columns"),
                                         style={'width':'85%','margin-top':'2%','margin-bottom':'2%','margin-left':'2%'}),
                                         html.Div(info_prep(list),style={'margin-bottom':'2%','margin-top':'2%','margin-left':'20%'}),
                                         ],style={'float':'left','width':'20%','border':'solid','overflowY':'scroll'}),

]),




# Process data

                        html.Div([html.H5(children='process data',style={'margin-left':'8%','border':'solid','width':'80%','text-align':'center'}),
                                html.Div(
                                     dash_table.DataTable(
                                                             id='table-filtering',
                                                             columns=[
                                                                 {"name": i, "id": i} for i in (df.columns)
                                                             ],style_header={'fontWeight': 'bold'},
                                                             pagination_settings={
                                                                 'current_page': 0,
                                                                 'page_size': 5
                                                             },
                                                             pagination_mode='be',
                                                             filtering='be',
                                                             filtering_settings='',style_table={'overflowX': 'scroll'}
                                                         ),
                                                       style={'margin-top':'2%', 'margin-left':'8%', 'width':'80%'})
                                                    ],style={'float':'right','width':'30%'}),
                            #Sample data

                            html.Div([html.H5(children='sample raw data',style={'margin-left':'8%','border':'solid','width':'100%','text-align':'center'}),
                                    html.Div(
                                         dash_table.DataTable(
                                                                 id='table-filtering',
                                                                 columns=[
                                                                     {"name": i, "id": i} for i in (df.columns)
                                                                 ],style_header={'fontWeight': 'bold'},
                                                                 pagination_settings={
                                                                     'current_page': 0,
                                                                     'page_size': 5
                                                                 },
                                                                 pagination_mode='be',

                                                                 filtering='be',
                                                                 filtering_settings='',style_table={'overflowX': 'scroll'}
                                                             ),

                                                        style={'margin-top':'2%', 'margin-left':'8%'}
                                                        ),
                                                     ],style={'display':'inline-block','width':'33%'})


]),

)
