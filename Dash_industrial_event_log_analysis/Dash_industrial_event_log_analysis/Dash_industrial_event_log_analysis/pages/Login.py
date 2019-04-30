import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
import requests


df = pd.read_csv('df_raw')

def modal():
    return html.Div(
             html.Div(
                       [
                        html.Div(
                            [
                            html.Div(
                            [
                                html.Span(
                                    "New Project",
                                    style={
                                        "color": "#506784",
                                        "fontWeight": "bold",
                                        "fontSize": "20",
                                    },
                                ),
                                html.Span(
                                    "×",
                                    id="new_project_close",
                                    n_clicks=0,
                                    style={
                                        "float": "right",
                                        "cursor": "pointer",
                                        "marginTop": "0",
                                        "marginBottom": "17",
                                    },
                                ),
                            ],
                            className="row",
                            style={"borderBottom": "1px solid #C8D4E3"},
                        ),

                        # Project Form
                        html.Div(
                            [
                                html.P(
                                    [
                                        "Project Name",

                                    ],
                                    style={
                                        "float": "left",
                                        "marginTop": "4",
                                        "marginBottom": "2",
                                    },
                                    className="row",
                                ),
                                dcc.Input(
                                    id="new_project_name",
                                    placeholder="Enter project name",
                                    type="text",
                                    value="",
                                    style={"width": "100%"},
                                ),
                                dcc.Input(
                                    id="User Name",
                                    placeholder="Enter User name",
                                    type="text",
                                    value="",
                                    style={
                                        "textAlign": "left",
                                        "marginBottom": "2",
                                        "marginTop": "4",
                                    },
                                ),


                            ],
                            className="row",
                            style={"padding": "2% 8%"},
                        ),

                        # submit button
                        html.Span(
                            "Submit",
                            id="submit_new_project",
                            n_clicks=0,
                            className="button button--primary add"
                        ),
                    ],
                    className="modal-content",
                    style={"textAlign": "center"},
                )],
                className="modal",
                ),
                id="project_modal",
        style={"display": "none"},
)



def filter_table(df):
    return html.Div([
     html.Div(
         dash_table.DataTable(
                                 id='table-project',
                                 columns=[
                                     {"name": i, "id": i} for i in (df.columns)
                                 ],
                                 selected_rows=[{'backgroundColor': '#3D9970',
                                         'color': 'white'}],
                                 style_header={'fontWeight': 'bold'},
                                 pagination_settings={
                                     'current_page': 0,
                                     'page_size': 5
                                 },
                                 pagination_mode='be',
                                 row_selectable="multi",
                                 editable=True,
                                 filtering='be',
                                 filtering_settings='',style_table={'overflowX': 'scroll'}
                             ),
                        className="five columns",style={'margin-top':'20', 'margin-left':'10','width':'40%'},

                     ),

     html.Button('Merge Selected Data', id='editing-rows-button',className="button button--primary",style=
     {'text-align':'right','margin-left':'-8%','margin-top':'22%',"background": "#119DFF",
     "border": "1px solid #119DFF","color": "white"}, n_clicks=0),
     html.A(html.Button('Prepare Data', id='prepare-data-button',className="button button--primary",style=
     {"background": "#119DFF",'margin-left':'-30%',
     "border": "1px solid #119DFF","color": "white"}),href='/Preprocess'),
 ])



layout = [

html.Div(
        [

             html.H1(children='Industrial Event Log Analysis',style={
                                                                      'padding-left': '2.0%',
                                                                      'padding-right': '2.0%',
                                                                      'border':'solid',
                                                                      #'background-color':'DodgerBlue',
                                                                      'text-align':'center'}),
            html.Div(
                [
                   html.H2(children='Project',style={'padding-left': '2.0%',
                                                     'padding-right': '2.0%',
                                                      'margin-top':'2%',
                                                      'border':'solid',
                                                      #'background-color':'DodgerBlue',
                                                      'text-align':'center'
                                                                     }),

                 ]),

            html.Div(
                dcc.Dropdown(
                    id="user_project",
                    options=[
                        {"label": "Project_1", "value": "project-f"},
                        {"label": "Project_2", "value": "project-s"},
                        {"label": "Project_3", "value": "project-th"},
                        {"label": "Project_4", "value": "project-fo"},
                    ],
                    value="project-f",
                    clearable=False,
                ),
                className="two columns",
            ),
           html.A(html.Button('Add Raw data',id='n-btn',className="button button--primary",style={'text-align':'right','margin-left':'15%',"background": "#119DFF",
           "border": "1px solid #119DFF","color": "white"}),href='/Home'),
            # add button
            html.Div(
                html.Span(
                    "new project",
                    id="new_project",
                    n_clicks=0,
                    className="button button--primary",
                    style={
                        "height": "34",
                        "background": "#119DFF",
                        "border": "1px solid #119DFF",
                        "color": "white",
                    },
                ),
                className="two columns",
                style={"float": "right"},
            ),
        ],
        className="row",
        style={"marginBottom": "10"},

    ),

modal(),
filter_table(df),

]


@app.callback(
    Output("new_project", "n_clicks"),
    [Input("new_project_close", "n_clicks"),
    Input("submit_new_project", "n_clicks")],
    [State("User Name","value"),
    State("new_project_name", 'value')],
)
def close_modal_callback(n, n2,Use_name,pr_name):
    if not ((n2 is None)  or (n2 == 0)):
        print('prt',n2)
        load = 'user='+Use_name+'&project='+pr_name
        r = requests.post("http://127.0.0.1:5000/check_project",params=load)
        return 0

@app.callback(Output("project_modal", "style"), [Input("new_project", "n_clicks")])
def display_leads_modal_callback(n):
    print(n)
    if n > 0:
        return {"display": "block"}
    return {"display": "none"}


@app.callback(Output('table-project', "data"),
             [Input('table-project', "pagination_settings"),
             Input('table-project', "filtering_settings")])
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



#@app.callback(
#    Output('adding-rows-table', 'data'),
#    [Input('editing-rows-button', 'n_clicks')],
#    [State('adding-rows-table', 'data'),
#     State('adding-rows-table', 'columns')])
#def add_row(n_clicks, rows, columns):
#    if n_clicks > 0:
#        rows.append({c['id']: '' for c in columns})
#    return rows



#def filter_data(selected_row_indices):
#        dff = df.iloc[selected_row_indices]
#        return dff

#@app.callback(
#    Output('table-project', 'style'),
#    [Input('table-project', 'selected_row_indices')])
#def update_style(selected_row_indices):
#    dff = filter_data(selected_row_indices)
#    print('hi')
#    return { 'backgroundColor': '#3D9970',
#            'color': 'white'}
