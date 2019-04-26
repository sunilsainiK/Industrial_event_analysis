import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import datetime
import dash_table
from app import app, server
from pages import data_summary
from pages import files_page
from pages import db_page
from pages import Home_Page
#
from pages import Preprocess
from pages import Login
from pages import Log_file
from pages import page_2
from pages import Modal_result

import requests


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/files_page':
        return files_page.files_page_layout
    elif pathname == '/db_page':
        return db_page.db_page_layout
    elif pathname =='/data_summary':
        return data_summary.data_summary_layout
    elif pathname =='/Preprocess':
        return Preprocess.layout
    elif pathname =='/Home':
        return Home_Page.HomePage_layout
    elif pathname == '/login':
        return Login.layout
    elif pathname =='/test':
        return page_2.layout
    elif pathname == '/Modal':
        return Modal_result.layout
    else:
        return Log_file.layout


if __name__ == '__main__':
    app.run_server(debug= True )
