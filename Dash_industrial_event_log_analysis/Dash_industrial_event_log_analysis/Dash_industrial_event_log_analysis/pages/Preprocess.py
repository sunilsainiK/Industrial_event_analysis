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
           btn_values.append(html.Div(html.Button(list[i] ,id='info'+str(i),title=value,style={'width':'80%',
                                                                                   'margin-top':'4%',
                                                                                   'margin-left':'4%',
                                                                                   'margin-bottom':'4%'}),
                                                                                   className="row"))
           print('info'+str(i))
    return btn_values

def info_prep(list):
    i=1
    btn = []
    for i in range (len(list)):
       if not  list[i]=='':
           value=list[i]
           btn.append(html.Div(html.Button('i' ,id='info'+value,title=value,style={'width':'1%',
                                                                                          'margin-top':'0.2%',
                                                                                          'margin-bottom':'95%'}),style={'margin-top':'4%',
                                                                                                                        'margin-bottom':'4%'},
                                                                                          className="row"))
           print('info'+value)

    return btn

def info(list):
    i=1
    val =[]
    for i in range (len(list)):
       if not  list[i]=='':
           value=list[i]
           val.append(html.Div(id=value,className="row"))
    return  val




def prep_dialog_box(list):
    i=1
    val=[]
    for i in range (len(list)):

        if not list[i]=='':
            val.append(html.Div(id=list[i]+str(i)+'prep_box', className="row"))
            print(list[i]+str(i)+'prep_box')
    return val

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
#Preprocesssteps
                                html.Div(html.Div(button_values(list),className="seven columns"),
                                         style={'width':'60%','margin-top':'2%','margin-bottom':'2%','height':'400px','margin-left':'2%'}),
#infolist Preprocess
                                         html.Div(html.Div(info_prep(list)),
                                         style={'margin-bottom':'2%','height':'200px',
                                         'margin-top':'-112%','float':'right'}),],
                                style={'float':'left','width':'20%','border':'solid','overflowY':'scroll','height':'500px'}),
#InfoBox
             html.Div(info(list),className="seven columns"),
             html.Div(prep_dialog_box(list),className="seven columns"),
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

                    html.Div([html.H5(children='sample raw data',style={'margin-left':'8%','border':'solid','width':'90%','text-align':'center'}),
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

def generate_output_id(value1):
    return '{}'.format(value1)


def generate_input_id(value1):
    return 'info{}'.format(value1)

# information box and callback based on list
for val in range(len(list)):
    if not  list[val]=='':
        @app.callback(Output(generate_output_id(list[val]),'children'),
        [Input(generate_input_id(list[val]),'n_clicks')],
        [State(generate_input_id(list[val]),'title')])
        def inp(n_clicks, title):
            if not ((n_clicks is None)  or (n_clicks==0)):
                prpro_info='prestep_info='+title
                r  = requests.get("http://127.0.0.1:5000/preprocess_Info",params=prpro_info)
                print(r.text)
                return html.Div([
                                html.Iframe(srcDoc=r.text,style={'width':'80%',
                                'height':'50px','border':'solid'},draggable='yes'),
                                html.Button('close',id='close_info_panel',style={'border':'solid','marginLeft':'80%'})]
                                ,style={'border':'solid','height':'200px'})


#setting value to zero for closing infobox
for val in range(len(list)):
    if not  list[val]=='':
        @app.callback(Output(generate_input_id(list[val]),'n_clicks'),
        [Input('close_info_panel','n_clicks')],)
        def close_info_panel(n):
            print('panel',n)
            return 0


# controlling box hide and display based on clicks
for val in range(len(list)):
    if not  list[val]=='':
        @app.callback(Output(generate_output_id(list[val]),"style"),
        [Input(generate_input_id(list[val]),'n_clicks')],)
        def close_info_div(n):
            if  n > 0:
                print('div',n)
                return {"display": "block"}
            return  {"display": "none"}


#Show prep Dialog Box
for val in  range(len(list)):
    if  not  list[val]=='':
        inp_val = list[val]+str(val)
        inp_val = inp_val+'prep_box'
        print(inp_val)
        print('info'+list[val])
        @app.callback(Output(generate_output_id(inp_val),'children'),
        [Input(generate_input_id(val),'n_clicks')],
        [State(generate_input_id(val),'title')],)
        def dialog_box(n_clicks, title):
            if not ((n_clicks is None)  or (n_clicks==0)):
                print(title)
                algs = 'algs='+title
                alg_args = requests.get("http://127.0.0.1:5000/get_pre_Args",params=algs)
                print(alg_args.text)
            return html.Div([html.Input(placeholder='enter'),
            html.Button('close',id='close_dialog_panel',style={'border':'solid','marginLeft':'80%'})],)


for val in range(len(list)):
    if not  list[val]=='':
        @app.callback(Output(generate_input_id(val),'n_clicks'),
        [Input('close_dialog_panel','n_clicks')],)
        def close_dia_panel(n):
            print('panel',n)
            return 0



for val in range(len(list)):
    if not  list[val]=='':
        @app.callback(Output(generate_output_id(inp_val),"style"),
        [Input(generate_input_id(val),'n_clicks')])
        def close_dialog_div(n):
            if  n > 0:
                print('div',n)
                return {"display": "block"}
            return  {"display": "none"}
