import datetime
import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from dash_html_components.Div import Div
from matplotlib.pyplot import cla, fill, text, title
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from app import app
from apps import historic, realtime


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/historic':
        return historic.layout
    elif pathname == '/apps/realtime':
        return realtime.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
