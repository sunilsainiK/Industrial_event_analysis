import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests







v_r  = requests.get("http://127.0.0.1:5000/visual_result")
print(v_r.text)

layout = html.Div(
              html.Div([
                 html.Div([html.H1(children='Industrial Event Log Analysis',style={
                                                                                   'padding-left': '2.0%',
                                                                                   'padding-right': '2.0%',
                                                                                   'border':'solid',
                                                                                   #'background-color':'DodgerBlue',
                                                                                   'text-align':'center'                                                                                  }
                 ),
                 html.Div([html.H2(children='Modeling Result',style={
                                                                             'padding-left': '2.0%',
                                                                             'padding-right': '2.0%',
                                                                              'margin-top':'2%',

                                                                              'border':'solid',
                                                                              #'background-color':'DodgerBlue',
                                                                              'text-align':'center'
                                                                                })]),

                 html.Div([
                  html.Div(html.H5(children='Details Visualization', style={'border':'solid','width':'20%'})),
                          html.Div([
                                              html.Div(html.Div( style={'textAlign':'left'},className="seven columns"),
                                                       style={'width':'100%','margin-top':'2%','margin-bottom':'2%','height':'400px',
                                                       'margin-left':'2%'}),
                                                                            ])
                 ])
        ])
    ])
)
