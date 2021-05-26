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
exec(open('./AQI Data Retrieval.py').read())

app = dash.Dash(__name__)

server = app.server
