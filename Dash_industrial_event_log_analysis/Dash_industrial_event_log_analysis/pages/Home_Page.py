
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


HomePage_layout = html.Div(
              html.Div([
                 html.Div([html.H1(children='Industrial Event Log Analysis',style={
                                                                                   'padding-left': '2.0%',
                                                                                   'padding-right': '2.0%',
                                                                                   'border':'solid',
                                                                                   #'background-color':'DodgerBlue',
                                                                                   'text-align':'center'                                                                                  }
                 ),
                 html.Div([html.H2(children='Select Your Data Source',style={
                                                                             'padding-left': '2.0%',
                                                                             'padding-right': '2.0%',
                                                                              'margin-top':'2%',

                                                                              'border':'solid',
                                                                              #'background-color':'DodgerBlue',
                                                                              'text-align':'center'
                                                                                })])
                 ]),
            html.Div(
                html.Div([html.A(html.Button('Csv/Pkl/Excel',id='csv-btn',type='submit',style={'width':'10.0%',
                                                                        'height':'200px',
                                                                        'background-color':'lightblue',
                                                                        'margin-top':'15.0%',
                                                                        'margin-left': '5.0%'}),href='/files_page'),
                        html.A(html.Button('SQl Database',id='sql-btn',type='submit',style={'width':'10.0%',
                                                                                 'height':'200px',
                                                                                 'background-color':'lightblue',
                                                                                 'margin-top':'15.0%',
                                                                                 'margin-left': '30.0%'}),href='/db_page'),
                        html.Button('Ability',id='Ab-btn',style={'width':'10.0%',
                                                                                 'height':'200px',
                                                                                 'background-color':'lightblue',
                                                                                 'margin-top':'15.0%',
                                                                                 'margin-left': '30.0%'})

                 ]),style={'border':'solid',
                           'height':'800px'}
            )

             ])


          )
