import dash
import dash_auth

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

VALID_USERNAME_PASSWORD_PAIRS = [
    ['hello', 'world']
]


auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server

app.config.suppress_callback_exceptions = True
