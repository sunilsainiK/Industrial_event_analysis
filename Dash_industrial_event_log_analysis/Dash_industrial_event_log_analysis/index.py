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
    else:
        return Home_Page.HomePage_layout


if __name__ == '__main__':
    app.run_server()
