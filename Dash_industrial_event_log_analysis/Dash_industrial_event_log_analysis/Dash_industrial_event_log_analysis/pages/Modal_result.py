import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests




print('hi')
tr = requests.get("http://127.0.0.1:5000/run_algo")
tr = tr.json()
print(type(tr))
#for key, value in tr.items():
trace = tr
#trace = dict(type="heatmap",z=ht,x=df.columns, y=df.columns)





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

                   dcc.Graph(
        id='example-graph-2',
        figure={
            'data':[
                    {'type':"barplot", 'x':'small_period' , 'y':'score' , 'df':df.to_json()}
                    ],

                        }

    )

                 ])
        ])
    ])
)
