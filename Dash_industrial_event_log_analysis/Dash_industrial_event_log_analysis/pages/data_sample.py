import dash
import dash_table
import pandas as pd
from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State



df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')


PAGE_SIZE = 5


data_raw_sample = html.Div(
              html.Div([
                       html.Div(dash_table.DataTable(
                                id='table-filtering',
                                columns=[
                                    {"name": i, "id": i} for i in sorted(df.columns)
                                ],
                                pagination_settings={
                                    'current_page': 0,
                                    'page_size': PAGE_SIZE
                                },
                                pagination_mode='be',

                                filtering='be',
                                filtering_settings=''
                            ),style={'width':'40.0%','margin-top':'2%','margin-left': '2.0%'},),

                            html.Div(dcc.Dropdown(id='summary_dropdown',value='dropdownvalue',
                                    options=[
                                                {'label': 'correlations', 'value': 'corr'},
                                                {'label': 'null_values', 'value': 'null'},
                                                {'label': 'unique_values', 'value': 'unique'},
                                                {'label': 'stats', 'value': 'stats'}],
                                            ),
                                        html.Div(id='table-summary'),
                                                 style={'width':'40.0%','margin-top':'20%','margin-left': '2.0%'}),

                    ]),
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

@app.callback(Output('table-summary', 'children'), [Input('summary_dropdown', 'value')])
def update_table(value):
    if value == 'corr':
        dff = df.corr()
        return generate_table(dff)
    elif value == 'null':
        dff = pd.DataFrame(df.isna().sum()/len(df),index = df.columns)
        return generate_table(dff)
    elif value == 'unique':
        dff = pd.DataFrame(df.columns.unique(),index = df.columns)
        return generate_table(dff)
    elif value =='stats':
        dff = df.info()
        return generate_table(dff)
    else:
        dff = df.corr()
        return generate_table(dff)
