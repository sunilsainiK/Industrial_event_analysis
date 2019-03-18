import dash
import dash_table
import pandas as pd
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State



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

                                        html.Div(dcc.Dropdown(id='summary_dropdown',value='dropdownvalue',
                                                    options=[
                                                                {'label': 'correlations', 'value': 'corr'},
                                                                {'label': 'null_values', 'value': 'null'},
                                                                {'label': 'unique_values', 'value': 'unique'},
                                                                {'label': 'stats', 'value': 'stats'}
                                                            ],
                                                    ),
                                        html.Div(
                                                   dash_table.DataTable(id='table-summary',
                                                                        columns=[
                                                                            {"name": i, "id": i} for i in (df_sum)]
                                                                       )
                                                 ),
                                                 className="five columns", style={'margin-top':'20','margin-right':'10'}),


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

@app.callback(Output('table-summary', 'data'), [Input('summary_dropdown', 'value')])
def update_table(value):
    df_stats = df
    if value == 'corr':
        return df_stats.corr()
    elif value == 'null':
        return pd.DataFrame(df_stats.isna().sum()/len(df_stats),index = df_stats.columns)
    elif value == 'unique':
        return pd.DataFrame(df_stats.columns.unique(),index = df_stats.columns)
    elif value =='stats':
        return df_stats.info()
    else:
        return pd.DataFrame(df_stats.columns.unique(),index = df_stats.columns)
