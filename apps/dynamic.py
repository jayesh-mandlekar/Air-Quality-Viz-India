# Dash and Plotly Libraries
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# External Libraries
from datetime import date, datetime
import pandas as pd

from app import app

colors = {
    'background': '#202020',
    'text': '#B3C100'
}

layout = html.Div([
    html.H1('Dynamic Data Page'),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Static Data Page', href='/static-data'),
    html.Br(),
    dcc.Link('Home Page', href='/')
])
