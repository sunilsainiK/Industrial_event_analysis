import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests
from app import app

layout = html.Div([
                  html.H1(children='Industrial Event Log Analysis',style={
                                                         'padding-left': '2.0%',
                                                         'padding-right': '2.0%',
                                                         'border':'solid',
                                                         #'background-color':'DodgerBlue',
                                                         'text-align':'center'}),

                            html.Div([
                                  html.Label('User Name  ',style={'height':'25px'}),
                                  dcc.Input(id='user', type='text', placeholder='Please Enter the Username',
                                           style={'marginTop':'2%','width':'40%','height':'25px'}),
                                  html.A(
                                   html.Button('Login',id='log_btn',
                                  style={"background": "#119DFF","border": "1px solid #119DFF","color": "white", 'height':'30px'}),
                                  id = 'output-container-button')

                            ],
                         style={'float':'center','marginLeft':'30%','marginTop':'10%'})
            ])
@app.callback(Output('output-container-button', 'href'),
              [Input('log_btn','n_clicks')],
              [State('user','value')])
def update_output(n_clicks,value):
    pr = "pr="+value
    r  = requests.get("http://127.0.0.1:5000/login",params=pr)
    return "/login"
