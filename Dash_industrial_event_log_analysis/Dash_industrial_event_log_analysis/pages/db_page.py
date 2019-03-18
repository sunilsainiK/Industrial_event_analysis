import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

db_page_layout =  html.Div(
              html.Div([
                 html.Div([html.H1(children='Industrial Event Log Analysis',style={
                                                                                   'padding-left': '2.0%',
                                                                                   'padding-right': '2.0%',

                                                                                   'border':'solid',
                                                                                   #'background-color':'DodgerBlue',
                                                                                   'text-align':'center'                                                                                  }
                 ),
                 html.Div([html.H2(children='Database',style={
                                                                             'padding-left': '2.0%',
                                                                             'padding-right': '2.0%',
                                                                              'margin-top':'2%',

                                                                              'border':'solid',
                                                                              #'background-color':'DodgerBlue',
                                                                              'text-align':'center'
                                                                                }),])
                 ]),
                 ]),
)
