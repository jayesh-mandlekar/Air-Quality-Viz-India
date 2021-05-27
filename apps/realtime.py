import datetime
import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from dash_html_components.Div import Div
import dash_table
from matplotlib.pyplot import cla, fill, text, title
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

from app import app

current_df = pd.read_csv('./data/aqi-data.csv')
current_df = current_df[['Timestamp','State','City','Temperature','Humidity','Condition','AQI','PM 2.5','PM 10']]

colors = {
    'background': '#A3B3C4',
    'text': '#0A3D78'
}

layout = html.Div(style={'backgroundColor': colors['background'], 'color': colors['text']}, children=[
    html.H1(children='Indian Air Quality User Dashboard',
            style={'textAlign': 'center'}),
    html.Div(className='graph-callback-flex',
             children=[
                 html.Div(className='callback-flex',
                          children=[
                          dcc.Link(html.Button('Historic'), href='/apps/historic'),
                          dcc.Link(html.Button('Real Time'), href='/apps/realtime'),
                              html.Div(className='padding-utility', children=[html.Label('States'),
                              dcc.Dropdown(
                                  id='state-dropdown',
                                  options=[
                                      {'label': i, 'value': i} for i in current_df['State'].sort_values().unique()
                                  ],
                                  value=current_df['State'].sort_values().unique()[0],
                                  clearable=False
                              )]),
                              html.Div(className='padding-utility', children=[
                                  html.Label(
                                      'City', className='individual-padding'),
                                  dcc.Dropdown(
                                      id='city-dropdown-2',
                                      clearable=False
                                  ),
                              ]),
                          ]),
                ]),
                html.Div(className='graph-flex',
                         children=[
                             html.Div(className='graph-child-flex', children=[
                                 dcc.Graph(id='pollutant-bar'),
                             ]),
                             html.Div(className='graph-child-flex', children=[
                                 dcc.Graph(id='state-city-bar'),
                        ]),
                ]),
                dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in current_df.columns],
                    data=current_df.to_dict('records'),
                    filter_action="native",
                    sort_action="native",
                )
    ])



@app.callback(
    dash.dependencies.Output('city-dropdown-2', 'options'),
    [dash.dependencies.Input('state-dropdown', 'value')]
)
def update_date_dropdown(name):
    return [{'label': i, 'value': i} for i in current_df.loc[current_df['State'] == name]['City'].sort_values().unique()]

@app.callback(
    Output('pollutant-bar', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('city-dropdown-2', 'value')]
)
def update_figure(state, city):
    features = ['PM 2.5', 'PM 10']
    required_df = current_df[(current_df['State'] == state) & (current_df['City'] == city)][features]
    x_columns = required_df.index.tolist()

    fig_1 = go.Figure(data=[
        go.Bar(name='PM 2.5', x=x_columns,
               y=required_df['PM 2.5']),
        go.Bar(name='PM 10', x=x_columns,
               y=required_df['PM 10']),
    ])

    fig_1.update_layout(autosize=False,
    width=1200,
    height=700,legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="right",
                            x=0.99
                        ), plot_bgcolor=colors['background'],
                        paper_bgcolor=colors['background'],
                        font_color=colors['text']
                        # title={
                        #     'text': "Stacked Bar Plot - Showing the Area Category Wise Pollution in {}".format(state),
                        #     'y': 0.92,
                        #     'x': 0.5,
                        #     'xanchor': 'center',
                        #     'yanchor': 'top'}))
                        )
    fig_1.update_xaxes(
        title_text="Pollutants in "+city,
        title_font={"size": 20},
        showgrid=False,
    )

    fig_1.update_yaxes(
        title_text="Pollutant Quantity (in ug/m3)",
        showgrid=True,
        # zeroline=False,
        # visible=False
    )

    return fig_1

@app.callback(
    Output('state-city-bar', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('city-dropdown-2', 'value')]
)
def update_figure(state, city):
    features = ['City','AQI']
    required_df = current_df[(current_df['State'] == state)][features].sort_values(by='AQI',ascending=True).reset_index()
    x = required_df['AQI'].tolist()
    y = required_df['City'].tolist()
    color=np.array(['rgb(255,255,255)']*len(y))
    pos = required_df.loc[required_df['City'] == city].index
    color[pos] ='rgb(0,0,0)'
    fig_2 = go.Figure(go.Bar(
                x=x,
                y=y,
                marker=dict(color=color.tolist()),
                orientation ='h'
    ))

    fig_2.update_layout(autosize=False,
    width=1200,
    height=700,
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )

    fig_2.update_xaxes(
        title_text="AQI of cities in " + state,
        showgrid=True,
        title_font={"size": 20},
    )

    fig_2.update_yaxes(
        title_text="Cities in "+state,
        title_font={"size": 20},
        showgrid=False,
    )

    return fig_2
