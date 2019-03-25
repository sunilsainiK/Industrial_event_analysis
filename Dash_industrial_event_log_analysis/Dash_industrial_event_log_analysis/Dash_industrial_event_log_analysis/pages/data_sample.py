import dash
import dash_table
import pandas as pd
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

import plotly.plotly as py
from plotly import figure_factory as FF



df = pd.read_csv('df_raw')

df_sum = df.columns.unique()

PAGE_SIZE = 5


data_raw_sample = html.Div(
              html.Div([
                           html.Div(
                                dash_table.DataTable(
                                                        id='table-filtering',
                                                        columns=[
                                                            {"name": i, "id": i} for i in (df.columns)
                                                        ],style_header={'fontWeight': 'bold'},
                                                        pagination_settings={
                                                            'current_page': 0,
                                                            'page_size': PAGE_SIZE
                                                        },
                                                        pagination_mode='be',

                                                        filtering='be',
                                                        filtering_settings='',style_table={'overflowX': 'scroll'}
                                                    ),
                                               className="five columns",style={'margin-top':'20', 'margin-left':'10'}
                                            ),

                                        html.Div([html.Div(dcc.Dropdown(id='summary_dropdown',value='dropdownvalue',
                                                    options=[
                                                                {'label': 'correlations', 'value': 'corr'},
                                                                {'label': 'null_values', 'value': 'null'},
                                                                {'label': 'unique_values', 'value': 'unique'},
                                                                {'label': 'distribution', 'value': 'dist'},
                                                                {'label': 'stats', 'value': 'stats'}
                                                            ],
                                                    ),className="five columns", style={'margin-top':'20','margin-left':'20'}),
                                        html.Div(
                                                  dcc.Graph(id='table-summary'),
                                                  className="five columns", style={'margin-top':'20','margin-left':'20'})
                                                  ],
                                                  className="row",
                                                 ),



                    ],className="row"),
)

@app.callback(Output('table-filtering', "data"),
             [Input('table-filtering', "pagination_settings"),
             Input('table-filtering', "filtering_settings")])
def update_graph(pagination_settings, filtering_settings):
    filtering_expressions = filtering_settings.split(' && ')
    dff = df
    for filter in filtering_expressions:
        if ' eq ' in filter:
            col_name = filter.split(' eq ')[0]
            filter_value = filter.split(' eq ')[1]
            dff = dff.loc[dff[col_name] == filter_value]
        if ' > ' in filter:
            col_name = filter.split(' > ')[0]
            filter_value = float(filter.split(' > ')[1])
            dff = dff.loc[dff[col_name] > filter_value]
        if ' < ' in filter:
            col_name = filter.split(' < ')[0]
            filter_value = float(filter.split(' < ')[1])
            dff = dff.loc[dff[col_name] < filter_value]

    return dff.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')

@app.callback(Output('table-summary', 'figure'), [Input('summary_dropdown', 'value')])
def update_table(value):
    df_graph = df
    if value == 'corr':
        fig = corr(df_graph)
        return fig
    elif value == 'null':
        fig = bar(df_graph)
        return fig
    elif value == 'unique':
        fig = uni_df(df)
        return fig
    elif value =='dist':
        fig = distri(df)
        return fig
    elif value == 'stats':
        fig = stats(df)
        return fig
    else:
        fig = corr(df_graph)
        return fig

def corr(df):
    ht=df.corr().values

    trace = dict(type="heatmap",z=ht,x=df.columns, y=df.columns)
    layout = dict(margin=dict(t=25, l=210, b=85),)
    return go.Figure(data=[trace], layout=layout)


def bar(df):
    trace =  [
    go.Bar(
        x=df.columns,
        y=((df.isna().sum()/len(df))*100), name='Null Values'
    )]
    layout = dict(
        margin=dict(t=25, l=210, b=85, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return go.Figure(data=trace, layout=layout)



def uni_df(df):
    trace =  [
    go.Bar(
        x=df.columns,
        y=df.nunique(), name='Unique Values'
    )]
    layout = dict(
        margin=dict(t=25, l=210, b=85, pad=4),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return go.Figure(data=trace, layout=layout)


def distri(df):
    ht = []
    box_df=df.drop(df.columns[0], axis=1)
    for col in box_df.columns:
        ht.append(go.Box(y=box_df[col], name=col, showlegend=False))
    ht.append(go.Scatter(x =box_df.columns, y =box_df.mean(), mode='lines', name='mean'))


    layout = dict(
        margin=dict(t=25, l=210, b=85),
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return go.Figure(data=ht, layout=layout)

def stats(df):
    stats=pd.DataFrame()
    stats["mean"]=df.mean()
    stats["Std.Dev"]=df.std()
    stats["Var"]= df.var()
    ht = stats.T
    ht = ht.reset_index()
    table = FF.create_table(ht)
    return go.Figure(data=table)
