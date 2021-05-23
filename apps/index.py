# Dash and Plotly Libraries
import dash_core_components as dcc
import dash_html_components as html

layout = html.Div([
    dcc.Link('Static Data Page', href='/static-data'),
    html.Br(),
    dcc.Link('Dynamic Data Page', href='/dynamic-data'),
])
