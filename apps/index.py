# Dash and Plotly Libraries
import dash_core_components as dcc
import dash_html_components as html
from dash_html_components.Header import Header

layout = html.Div(children=[

    html.Header(children=[
        html.H2('Dashboard'),
        html.Nav(children=[
            html.Li(children=[html.A(
                'Codebase', href='https://github.com/jayesh-mandlekar/Air-Quality-Viz-India')])
        ])
    ]),

    html.Section(className="hero", children=[
        html.Div(className="background-image"),
        html.Div(className="hero-content-area", children=[
            html.H1('Indian Air Quality Dashboard'),
            html.Div(className="front-page-links", children=[dcc.Link('Static Data Page', href='/static-data', className='links'),
                                                             dcc.Link('Dynamic Data Page', href='/dynamic-data', className='links')]),
        ]),
    ]),


])

