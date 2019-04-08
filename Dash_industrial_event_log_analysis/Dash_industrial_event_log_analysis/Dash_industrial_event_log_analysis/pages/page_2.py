import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


layout =html.Div([
                #html.Div(
                html.Iframe(src='https://images.pexels.com/photos/414612/pexels-photo-414612.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500',style={'width':'80%',
                'height':'50px','border':'solid'},draggable='yes'),

                #html.Hr(),
                html.Button('text',style={'border':'solid','marginLeft':'80%'})]
                ,style={'border':'solid','height':'200px'})
