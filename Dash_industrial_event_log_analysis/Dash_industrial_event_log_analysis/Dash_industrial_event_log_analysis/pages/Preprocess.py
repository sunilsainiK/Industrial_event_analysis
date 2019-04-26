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
from dash.exceptions import CantHaveMultipleOutputs


import re
import json
df = pd.read_csv('df_raw')
prep='prepackage=PreProcessing'
r  = requests.get("http://127.0.0.1:5000/preprocess",params=prep)
list =re.split(',',r.text)

display_style={}
view_opt_list=[]
prepro_display={}
df_inter_mediate = df
dff = df
columns_list = df.columns.tolist()

add_displ=0

def Input_modal():
    return html.Div(
             html.Div(
                       [
                        html.Div(
                            [
                            html.Div(
                            [

                                html.Span(
                                    "×",
                                    id="Input_text_preprocess",
                                    n_clicks=0,
                                    style={
                                        "float": "right",
                                        "cursor": "pointer",
                                        "marginTop": "0",
                                        "marginBottom": "17",
                                    },
                                ),
                            ],
                            className="row",
                            style={"borderBottom": "1px solid #C8D4E3"},
                        ),

                        # Project Form
                        html.Div(
                            [
                                html.P(
                                    [
                                        "Enter the Text",

                                    ],
                                    style={
                                        "float": "left",
                                        "marginTop": "4",
                                        "marginBottom": "2",
                                    },
                                    className="row",
                                ),

                                dcc.Input(
                                    id="Input_Text",
                                    placeholder="Enter the text here",
                                    type="text",
                                    value="",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),
                            ],
                            className="row",
                            style={"padding": "2% 8%"},
                        ),

                        # submit button
                        html.Span(
                            "Submit",
                            id="submit_new_text",
                            n_clicks=0,
                            className="button button--primary add"
                        ),
                    ],
                    className="modal-content",
                    style={"textAlign": "center"},
                )],
                className="modal",
                ),
                id="Input_project_modal",
        style={"display": "none"},
)


def layoutdialog(columns_list, view_opt_list):
    global display_style
    global add_displ
    if view_opt_list==[]:
       display_style_tit={'width':'50%','marginLeft':'30%','border':'solid',"display": "none"}
       display_style = {"display": "none",'width':'50%','marginLeft':'50%'}
       view_opt_list=['nothing','in_list']
    else:
        if add_displ == 0:
            display_style_tit={'width':'50%','marginLeft':'30%','border':'solid',"display": "block"}
            display_style = {"display": "block",'width':'50%','marginLeft':'50%'}
        else:
            display_style = {"display": "none",'width':'50%','marginLeft':'50%'}


    lay=html.Div([
    html.Div(dcc.Checklist(id='checklist',
            options=[{'label': '{}'.format(name), 'value': '{}'.format(name)} for name in columns_list],
                    values=['{}'.format(columns_list[0])],style={'marginLeft':'5%'}),),
              html.Div(html.H3('Select Option for below',style=display_style_tit),id='select_option'),
              html.Div(dcc.RadioItems(id='option_checklist',
              options=[{'label': '{}'.format(opt_li), 'value': '{}'.format(opt_li)} for opt_li in view_opt_list],
              labelStyle={'display': 'inline-block'},
              style=display_style),id='opt_check'),

    html.Div(
        html.Span(
            "Add Input Text",
            id="Add_Input_Text",
            n_clicks=0,
            className="button button--primary",
            style={
                "height": "34",
                "background": "#119DFF",
                "border": "1px solid #119DFF",
                "color": "white",
            },
        ),
        className="two columns",
        style={'float':'right'},
       ),

       Input_modal(),
      html.Button('close',id='close_dialog_panel',style={'border':'solid','marginLeft':'80%'})],)
    return lay

def button_values(list):
    i=1
    btn_values =[]
    for i in range (len(list)):
       if not  list[i]=='':
           value=list[i]
           btn_values.append(html.Div(html.Button(list[i] ,id='info'+str(i),n_clicks=0,title=value,style={'width':'100%',
                                                                                   'margin-top':'4%',
                                                                                   'margin-left':'4%',
                                                                                   'margin-bottom':'4%',
                                                                                   'border':'solid',
                                                                                   'textAlign':'left'}),
                                                                                   className="row"))
    return btn_values

def info_prep(list):
    i=1
    btn = []
    for i in range (len(list)):
       if not  list[i]=='':
           value=list[i]
           btn.append(html.Div(html.Button('i' ,id='info'+value,title=value,style={'width':'1%',
                                                                                   'margin-bottom':'12%',
                                                                                   'border':'solid'}),
                                                                                    className="row"))
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
            val.append(html.Div(id=list[i]+str(i)+'prep_box',style={'border':'solid'}, className="row"))
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
            html.A(html.Button('Back',id='log-btn',style={'text-align':'left'}),href='/login'),
            html.A(html.Button('Model',id='Modal-btn',style={'text-align':'right','float':'right'}),href='/Modal'),
            html.Div([html.Button('update',id='up-pdata',style={'text-align':'left','margin-left':'55%',
            "background": "#119DFF",
            "border": "1px solid #119DFF","color": "white",'float':'left'},type='submit'),
                html.Button('save result',id='save_result',style={'text-align':'left',
                'margin-left':'80%','float':'right',"background": "#119DFF",
                "border": "1px solid #119DFF","color": "white"},type='submit')],
                style={'margin-left':'50%'}),

#Preprocessing lsit box
               html.Div([
                html.Div(html.H5(children='Preprocess Options', style={'border':'solid','width':'20%'})),
                        html.Div([
#Preprocesssteps
                                html.Div(html.Div(button_values(list), style={'textAlign':'left'},className="seven columns"),
                                         style={'width':'100%','margin-top':'2%','margin-bottom':'2%','height':'400px',
                                         'margin-left':'2%'}),
#infolist Preprocess
                                         html.Div(html.Div(info_prep(list)),
                                         style={'margin-bottom':'2%','height':'200px',
                                         'margin-top':'-170%','float':'right'}),],
                                style={'float':'left','width':'20%','border':'solid','overflowY':'scroll','height':'500px'}),
#InfoBox
             html.Div(info(list),className="seven columns"),
             html.Div(prep_dialog_box(list),className="seven columns"),
]),

# Process data
    html.Div([html.H5(children='process data',
                style={'float':'right','marginLeft':'8%','width':'25%','border':'solid','textAlign':'center','marginTop':'-3%'},
             ),
          html.Div(id='Process_data',
             style={
                 "maxHeight": "350px",
                 "overflowY": "scroll",
                 "padding": "8",
                 "marginLeft":"25%",
                 "backgroundColor":"white",
                 "border": "solid",
                 "width":"30%",
                 "borderRadius": "3px",
                 "float":"right"}),],
                 id='process_data_div',style=prepro_display),
                    #Sample data
                    html.Div([html.H5(children='sample raw data',
                    style={'margin-left':'8%','border':'solid','width':'90%','text-align':'center'}),
                            html.Div(
                                 dash_table.DataTable(
                                                         id='sample_raw_data',
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
                                             ],style={'display':'inline-block','width':'33%','marginTop':'-6%'},id='sample_raw_data')
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
            return 0


# controlling box hide and display based on clicks
for val in range(len(list)):
    if not  list[val]=='':
        @app.callback(Output(generate_output_id(list[val]),"style"),
        [Input(generate_input_id(list[val]),'n_clicks')],)
        def close_info_div(n):
            if  n > 0:
                return {"display": "block"}
            return  {"display": "none"}

#Show prep Dialog Box
for val in  range(len(list)):
    if  not  list[val]=='':
        inp_val = list[val]+str(val)
        inp_val = inp_val+'prep_box'
        @app.callback(Output(generate_output_id(inp_val),'children'),
        [Input(generate_input_id(val),'n_clicks')],
        [State(generate_input_id(val),'title')],)
        def dialog_box(n_clicks, title):
            if not ((n_clicks is None)  or (n_clicks==0)):
                algs = 'algs='+title
                alg_args = requests.get("http://127.0.0.1:5000/get_pre_Args",params=algs)
                select_options = alg_args
                option_list =re.split(',',select_options.text)
                view_opt_list=[]
                for k in range(len(option_list)):
                    if not option_list[k]=='':
                        view_opt_list.append(option_list[k])
                return layoutdialog(columns_list,view_opt_list)

for val in range(len(list)):
    if not  list[val]=='':
        @app.callback(Output(generate_input_id(val),'n_clicks'),
        [Input('close_dialog_panel','n_clicks')],
        [State('checklist','values'),
         State(generate_input_id(val),'title'),
         State(generate_input_id(val),'n_clicks'),
         State('option_checklist','value'),
         State("Input_Text",'value')])
        def close_dia_panel(n,n_title,values,n_click,opt,optional_text):
            if not ((n_click is None)  or (n_click==0)):
                print(values,n_click,opt,optional_text)
                global dff
                if not optional_text =='':
                    pre_run={'prestep_run': n_title,'opt':opt,'optedprepro':values,'optional_text':optional_text}
                    print(pre_run)
                else:
                    pre_run={'prestep_run': n_title,'opt':opt,'optedprepro':values}
                print('about to enter')
                inter_df = requests.get("http://127.0.0.1:5000/run_preprocess",json=dff.to_json(),params=pre_run)
                global df_inter_mediate
                print('after run')
                df_inter_mediate = pd.read_json(inter_df.text)
                print(df_inter_mediate.head())
                prepro_display={'display':'block'}
                print('clb_box')
                print('hello')
                print(n)
                return 0

for val in range(len(list)):
    if not  list[val]=='':
        inp_val = list[val]+str(val)
        inp_val = inp_val+'prep_box'
        @app.callback(Output(generate_output_id(inp_val),"style"),
                      [Input(generate_input_id(val),'n_clicks')],
                      [State(generate_input_id(val),'title')])
        def close_dialog_div(n,values):
            global prepro_display
            if not ((n is None)  or (n==0)):
                prepro_display = {"display": "block"}
                return {"display": "block"}
            prepro_display = {"display": "block"}
            return  {"display": "none"}


def df_to_table(df_int):
    return  dash_table.DataTable(id ='table',
                             columns=[
                                 {"name": i, "id": i} for i in (df_int.columns)
                             ],

                             style_header={'fontWeight': 'bold'},
                             pagination_settings={
                                 'current_page': 0,
                                 'page_size': 5
                             },
                             pagination_mode='be',
                             filtering='be',
                             filtering_settings='',
                             style_table={'overflowX': 'scroll'},
                         ),


@app.callback(Output('table','data'),
[Input('table','pagination_settings')])
def update_date(pagination_settings):
    global dff
    global df_inter_mediate
    dff = df_inter_mediate
    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')


@app.callback(
    Output("Process_data", "children"),
    [Input("up-pdata", "n_clicks")],
)
def update_preprcosee_data(n):
    if not ((n is None)  or (n==0)):
        global df_inter_mediate
        df_int = df_inter_mediate
        return df_to_table(df_int)
    return 'hi'


@app.callback(Output("up-pdata", "n_clicks"),
[Input('save_result','n_clicks')])
def up_data_clck(n):
    print('close',n)
    return 0

@app.callback(
    Output("process_data_div", "style"),
    [Input("up-pdata", "n_clicks"),
    Input('save_result','n_clicks')],
)
def update_preprcosee_data_style(n,n_save):
    if not ((n_save is None)  or (n_save==0)):
        global prepro_display
        if not ((n is None)  or (n==0)):
            prepro_display = {"display": "block"}
        else:
            prepro_display = {"display": "none"}
        return prepro_display
    if not ((n is None)  or (n==0)):
        return {"display": "block"}
    return  {"display": "none"}


@app.callback(Output('sample_raw_data', "data"),
             [Input('sample_raw_data', "pagination_settings"),
             Input('save_result','n_clicks')])
def update_data(pagination_settings, n):
    global prepro_display
    global dff
    if not ((n is None)  or (n==0)):
        global df_inter_mediate
        dff = df_inter_mediate
        prepro_display = {"display": "none"}
    else:
        global df
        dff = df
    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')


@app.callback(Output('sample_raw_data', "columns"),
             [Input('sample_raw_data', "pagination_settings"),
             Input('save_result','n_clicks')])
def update_col(pagination_settings, n):
    global dff
    if not ((n is None)  or (n==0)):
        global df_inter_mediate
        dff = df_inter_mediate
        global columns_list
        columns_list = dff.columns.tolist()
        global prepro_display
        prepro_display={'display':'none'}
    else:
        global df
        dff = df
    straw= [{"name": i, "id": i} for i in (dff.columns)]
    return straw

@app.callback(
    Output("Add_Input_Text", "n_clicks"),
    [Input("Input_text_preprocess", "n_clicks"),
    Input("submit_new_text", "n_clicks"),
    ],
)
def close_modal_callback(n,n2):
    print('print',n2)
    if not ((n2 is None)  or (n2==0)):
       return 0

@app.callback(Output("Input_project_modal", "style"),
 [Input("Add_Input_Text", "n_clicks"),
 Input("submit_new_text", "n_clicks")])
def display_leads_modal_callback(n,n2):
    print('Add_Input_Text',n,n2)
    if not ((n is None)  or (n==0)):
        return {"display": "block"}
    return {"display": "none"}


@app.callback(
    Output('opt_check',"style"),
    [Input("Add_Input_Text", "n_clicks")])
def display_opt_check(n):
    if not ((n is None)  or (n==0)):
        return {"display": "none"}
    return  {"display": "block"}




@app.callback(
    Output('select_option',"style"),
    [Input("Add_Input_Text", "n_clicks")])
def display_opt_check(n):
    if not ((n is None)  or (n==0)):
        return {"display": "none"}
    return  {"display": "block"}
