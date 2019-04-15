import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

columns_list = ['colum1', 'colum2', 'colum3', 'colum4', 'colum5']
view_opt_list=['avg', 'median', 'mean']

layout =  html.Div([
        html.Div(dcc.Checklist(id='checklist',
        options=[{'label': '{}'.format(name), 'value': '{}'.format(name)} for name in columns_list],
                values=['{}'.format(columns_list[0])],style={'border':'solid'})),
        html.H3('Select Option for below',style={'border':'solid'}),
    html.Div(dcc.RadioItems(id='option_checklist',options=[{'label': '{}'.format(opt_li), 'value': '{}'.format(opt_li)} for opt_li in view_opt_list],
    value=['{}'.format(view_opt_list[0])],labelStyle={'display': 'inline-block'},style={'border':'solid'})),
html.Button('close',id='close_dialog_panel',style={'border':'solid','marginLeft':'80%'})],)
