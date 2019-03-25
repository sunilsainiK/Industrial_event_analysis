import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from app import app





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
                    value="all",
                    clearable=False,
                ),
                className="two columns",
            ),

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
]

@app.callback(
    Output("new_project", "n_clicks"),
    [Input("new_project_close", "n_clicks"), Input("submit_new_project", "n_clicks")],
)
def close_modal_callback(n, n2):
    return 0



@app.callback(Output("project_modal", "style"), [Input("new_project", "n_clicks")])
def display_leads_modal_callback(n):
    print(n)
    if n > 0:
        return {"display": "block"}
    return {"display": "none"}
