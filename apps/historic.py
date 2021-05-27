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

# Dataset Manipulation and Analysis
air_quality_df = pd.read_csv('./data/data.csv')

air_quality_df.rename(columns={'stn_code': 'Station_Code',
                               'sampling_date': 'Sampling_Date',
                               'state': 'State',
                               'location': 'City',
                               'agency': 'Agency',
                               'type': 'Area Category',
                               'so2': 'Sulphur_Dioxide',
                               'no2': 'Nitrogen_Dioxide',
                               'rspm': 'Respirable_Suspended_Particulate_Matter',
                               'spm': 'Suspended_Particulate_Matter',
                               'location_monitoring_station': 'Monitoring_Station',
                               'pm2_5': 'Fine_Particulate_Matter',
                               'date': 'Date'}, inplace=True)

air_quality_df.drop(
    columns=['Suspended_Particulate_Matter', 'Fine_Particulate_Matter'], inplace=True)

air_quality_df.drop(
    columns=['Sampling_Date'], inplace=True)

air_quality_df.drop(columns=['Agency', 'Station_Code'], inplace=True)

for i in ['Sulphur_Dioxide', 'Nitrogen_Dioxide', 'Respirable_Suspended_Particulate_Matter']:
    air_quality_df[i].fillna((air_quality_df[i].mean()), inplace=True)

air_quality_df.dropna(axis=0, how='any', inplace=True)

air_quality_df['Area Category'] = air_quality_df['Area Category'].replace(
    ['Residential, Rural and other Areas', 'Residential and others',
        'Industrial Areas', 'Sensitive Areas'],
    ['Residential and Rural Areas', 'Residential Areas', 'Industrial Area', 'Sensitive Area'])

# -----Important Variables

Constant_Pollutants = ['Sulphur_Dioxide', 'Nitrogen_Dioxide',
                       'Respirable_Suspended_Particulate_Matter']
start_date_year = '2015'
start_date_month = '01'
start_date_day = '01'
end_date_year = '2015'
end_date_month = '12'
end_date_day = '31'

# ------------------
# -------------------------------------------------------------------------------------------------------

air_quality_df['Date'] = pd.to_datetime(air_quality_df['Date'])

# -------------------------------------------------------------------------------------------------------

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
                                      {'label': i, 'value': i} for i in air_quality_df['State'].unique()
                                  ],
                                  value="Andhra Pradesh",
                                  clearable=False
                              )]),
                              html.Div(className='padding-utility', children=[
                                  html.Label('Calendar'),
                                  dcc.DatePickerRange(id='Time-Slots',
                                                      start_date=datetime.date(2015, 1, 1),
                                                      end_date=datetime.date(2015,12,31),
                                                      min_date_allowed=datetime.date(1990, 1, 1),
                                                      max_date_allowed=datetime.date(2015,12,31),
                                                      )
                              ]),
                              html.Div(className='padding-utility', children=[
                                  html.Label(
                                      'Pollutants', className='individual-padding'),
                                  dcc.RadioItems(
                                      id='pollutant-dropdown',
                                      options=[{'label': i, 'value': i}
                                               for i in Constant_Pollutants],
                                      value=Constant_Pollutants[0],
                                      labelStyle={'display': 'inline-block'}
                                  ),
                              ]),
                              html.Div(className='padding-utility', children=[
                                  html.Label(
                                      'City', className='individual-padding'),
                                  dcc.Dropdown(
                                      id='city-dropdown',
                                      clearable=False
                                  ),
                              ]),
                              html.Div(className='padding-utility', children=[
                                  html.Label(
                                      'Area Category', className='individual-padding'),
                                  dcc.RadioItems(
                                      id='area-category-options',
                                      options=[{'label': i, 'value': i}
                                               for i in air_quality_df['Area Category'].unique()],
                                      value='Industrial Area',
                                      labelStyle={'display': 'inline-block'}
                                  ),
                              ]),
                          ]),

                 html.Div(className='graph-flex',
                          children=[
                              html.Div(className='graph-child-flex', children=[
                                  dcc.Graph(id='dotline-1-graph'),
                                  dcc.Graph(id='top-10-bar-graph'),
                              ]),
                              html.Div(className='graph-child-flex', children=[
                                  dcc.Graph(id='pollutant-trend-histogram'),
                                  dcc.Graph(id='pollutant-trend-boxplot'),
                              ]),
                              html.Div(className='graph-child-flex', children=[
                                  dcc.Graph(
                                      id='state-wise-area-category-bar-graph'),
                                  dcc.Graph(
                                      id='city-graph'
                                  )
                              ]),

                          ]),
             ]),
])

@app.callback(
    dash.dependencies.Output('city-dropdown', 'options'),
    [dash.dependencies.Input('state-dropdown', 'value')]
)
def update_date_dropdown(name):
    return [{'label': i, 'value': i} for i in air_quality_df.loc[air_quality_df['State'] == name]['City'].sort_values().unique()]

@app.callback(
    Output('city-graph', 'figure'), [
        Input('city-dropdown', 'value'),
        Input('area-category-options', 'value')
    ]
)
def update_figure(selected_city, selected_area_category):
    df_city = air_quality_df.loc[air_quality_df['City'] == selected_city]
    df = df_city.loc[df_city['Area Category'] == selected_area_category]
    y_sulphur = df['Sulphur_Dioxide'].mean()
    y_nitrogen = df['Nitrogen_Dioxide'].mean()
    y_matter = df['Respirable_Suspended_Particulate_Matter'].mean()

    fig_6 = go.Figure(data=go.Scatter(
        x=Constant_Pollutants,
        y=[y_sulphur, y_nitrogen, y_matter],
        mode='markers',
        marker=dict(
            color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)',
                   'rgb(44, 160, 101)'],
            size=[40, 60, 80],
            # showscale=True,
        )
    ))

    fig_6.update_layout(plot_bgcolor=colors['background'],
                        paper_bgcolor=colors['background'],
                        font_color=colors['text'])

    fig_6.update_xaxes(
        title_text="Pollutants",
        title_font={"size": 20},
        showgrid=False,
    )

    fig_6.update_yaxes(
        title_text="Average Quantity",
        showgrid=False,
        zeroline=False,
        # visible=False
    )

    return fig_6


@app.callback(
    Output('state-wise-area-category-bar-graph', 'figure'),
    Input('state-dropdown', 'value')
)
def update_figure(selected_state):
    state = selected_state
    features = ['Area Category', 'Sulphur_Dioxide',
                'Nitrogen_Dioxide', 'Respirable_Suspended_Particulate_Matter']
    required_df = air_quality_df.loc[air_quality_df['State']
                                     == state, features].groupby('Area Category').mean()
    x_columns = required_df.index.tolist()

    fig_5 = go.Figure(data=[
        go.Bar(name=Constant_Pollutants[0], x=x_columns,
               y=required_df[Constant_Pollutants[0]]),
        go.Bar(name=Constant_Pollutants[1], x=x_columns,
               y=required_df[Constant_Pollutants[1]]),
        go.Bar(name=Constant_Pollutants[2], x=x_columns,
               y=required_df[Constant_Pollutants[2]]),

    ])

    fig_5.update_layout(barmode='group',
                        legend=dict(
                            yanchor="top",
                            y=0.99,
                            xanchor="left",
                            x=0.50
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
    fig_5.update_xaxes(
        title_text="Area Category",
        title_font={"size": 20},
        showgrid=False,
    )

    fig_5.update_yaxes(
        title_text="Average Quantity",
        showgrid=False,
        # zeroline=False,
        # visible=False
    )

    return fig_5


@app.callback(
    Output('pollutant-trend-boxplot', 'figure'),
    [Input('Time-Slots', 'start_date'),
     Input('Time-Slots', 'end_date')]
)
def update_figure(start_date, end_date):
    global start_date_year, start_date_month, start_date_day
    global end_date_year, end_date_month, end_date_day
    string_prefix = "You have selected: "
    if start_date is not None:
        start_date_object = datetime.date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y-%m-%d')
        string_prefix = start_date_string
        start_date_list = string_prefix.split("-")
        start_date_year = start_date_list[0]
        start_date_month = start_date_list[1]
        start_date_day = start_date_list[2]

    if end_date is not None:
        end_date_object = datetime.date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y-%m-%d')
        string_prefix = end_date_string
        end_date_list = string_prefix.split("-")
        end_date_year = end_date_list[0]
        end_date_month = end_date_list[1]
        end_date_day = end_date_list[2]

    Time_Series_df = air_quality_df.loc[
        (air_quality_df['Date'] > datetime.datetime(int(start_date_year), int(start_date_month), int(start_date_day), 0, 0, 0)) &
        (air_quality_df['Date'] < datetime.datetime(int(end_date_year), int(end_date_month), int(end_date_day), 0, 0, 0))]

    y_0_values = Time_Series_df.loc[:, Constant_Pollutants[0]].values.tolist()
    y_1_values = Time_Series_df.loc[:, Constant_Pollutants[1]].values.tolist()
    y_2_values = Time_Series_df.loc[:, Constant_Pollutants[2]].values.tolist()

    fig_4 = go.Figure()
    fig_4.add_trace(go.Box(y=y_0_values, name=Constant_Pollutants[0])),
    fig_4.add_trace(go.Box(y=y_1_values, name=Constant_Pollutants[1])),
    fig_4.add_trace(go.Box(y=y_2_values, name=Constant_Pollutants[2])),

    # fig_4.update_layout(
    #     title={
    #         'text': "Boxplot - Distribution of {} from {} to {}".format(Required_Pollutant, start_date_string, end_date_string),
    #         'y': 0.92,
    #         'x': 0.5,
    #         'xanchor': 'center',
    #         'yanchor': 'top'},
    #         )

    fig_4.update_layout(plot_bgcolor=colors['background'],
                        paper_bgcolor=colors['background'],
                        font_color=colors['text'],
                        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01
    ), showlegend=False,)

    fig_4.update_xaxes(
        title_text="Pollutant",
        title_font={"size": 20},
        showgrid=False,
    )

    fig_4.update_yaxes(
        title_text="Count",
        title_font={"size": 20},
        showgrid=False,
    )

    return fig_4


@app.callback(
    Output('pollutant-trend-histogram', 'figure'),
    [Input('pollutant-dropdown', 'value'),
     Input('Time-Slots', 'start_date'),
     Input('Time-Slots', 'end_date')]
)
def update_figure(selected_pollutant, start_date, end_date):
    global start_date_year, start_date_month, start_date_day
    global end_date_year, end_date_month, end_date_day
    string_prefix = "You have selected: "
    if start_date is not None:
        start_date_object = datetime.date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y-%m-%d')
        string_prefix = start_date_string
        start_date_list = string_prefix.split("-")
        start_date_year = start_date_list[0]
        start_date_month = start_date_list[1]
        start_date_day = start_date_list[2]

    if end_date is not None:
        end_date_object = datetime.date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y-%m-%d')
        string_prefix = end_date_string
        end_date_list = string_prefix.split("-")
        end_date_year = end_date_list[0]
        end_date_month = end_date_list[1]
        end_date_day = end_date_list[2]

    Time_Series_df = air_quality_df.loc[
        (air_quality_df['Date'] > datetime.datetime(int(start_date_year), int(start_date_month), int(start_date_day), 0, 0, 0)) &
        (air_quality_df['Date'] < datetime.datetime(int(end_date_year), int(end_date_month), int(end_date_day), 0, 0, 0))]

    Required_Pollutant = selected_pollutant
    y_values = Time_Series_df.loc[:, Required_Pollutant].values.tolist()
    x_values = Time_Series_df.Date

    fig_3 = go.Figure(go.Histogram(
        x=y_values,
        # nbins=30,
    ))

    # fig_3.update_layout(
    #     title={
    #         'text': "Histogram - Distribution of {} from {} to {}".format(Required_Pollutant, start_date_string, end_date_string),
    #         'y': 0.92,
    #         'x': 0.5,
    #         'xanchor': 'center',
    #         'yanchor': 'top'})

    fig_3.update_layout(plot_bgcolor=colors['background'],
                        paper_bgcolor=colors['background'],
                        font_color=colors['text'])

    fig_3.update_xaxes(
        title_text="Distribution",
        title_font={"size": 20},
        showgrid=False,
    )

    fig_3.update_yaxes(
        title_text="Count",
        showgrid=False,
        # zeroline=False,
        # visible=False
    )

    return fig_3


@app.callback(
    Output('dotline-1-graph', 'figure'),
    [Input('state-dropdown', 'value'),
        Input('Time-Slots', 'start_date'),
        Input('Time-Slots', 'end_date'),
        Input('pollutant-dropdown', 'value')
     ]
)
def update_figure(selected_state, start_date, end_date, selected_Pollutant):
    global start_date_year, start_date_month, start_date_day
    global end_date_year, end_date_month, end_date_day
    string_prefix = "You have selected: "
    if start_date is not None:
        start_date_object = datetime.date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y-%m-%d')
        string_prefix = start_date_string
        start_date_list = string_prefix.split("-")
        start_date_year = start_date_list[0]
        start_date_month = start_date_list[1]
        start_date_day = start_date_list[2]

    if end_date is not None:
        end_date_object = datetime.date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y-%m-%d')
        string_prefix = end_date_string
        end_date_list = string_prefix.split("-")
        end_date_year = end_date_list[0]
        end_date_month = end_date_list[1]
        end_date_day = end_date_list[2]

    Time_Series_df = air_quality_df.loc[
        (air_quality_df['Date'] > datetime.datetime(int(start_date_year), int(start_date_month), int(start_date_day), 0, 0, 0)) &
        (air_quality_df['Date'] < datetime.datetime(int(end_date_year), int(end_date_month), int(end_date_day), 0, 0, 0))]

    Time_Series_df = Time_Series_df.loc[(
        Time_Series_df['State'] == selected_state), :]

    fig_1 = go.Figure()

    fig_1.add_trace(go.Scatter(x=Time_Series_df['Date'], y=Time_Series_df[selected_Pollutant],
                               mode='markers',
                               name=selected_Pollutant,
                               ))

    # fig_1.update_layout(
    #     title={
    #         'text': "Scatter and Line Plot - Amount of {}, {}, {} in {}".format(Constant_Pollutants[0], Constant_Pollutants[1], Constant_Pollutants[2], selected_state),
    #         'y': 0.92,
    #         'x': 0.5,
    #         'xanchor': 'center',
    #         'yanchor': 'top'})
    fig_1.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])

    fig_1.update_xaxes(
        title_text="Dates",
        title_font={"size": 20},
        showgrid=False,
    )

    fig_1.update_yaxes(
        title_text="Quantity",
        showgrid=False,
        # showgrid=False,
        # zeroline=False,
        # visible=False
    )

    return fig_1


@app.callback(
    Output('top-10-bar-graph', 'figure'),
    [Input('Time-Slots', 'start_date'),
     Input('Time-Slots', 'end_date')]
)
def update_figure(start_date, end_date):
    global start_date_year, start_date_month, start_date_day
    global end_date_year, end_date_month, end_date_day
    string_prefix = "You have selected: "
    if start_date is not None:
        start_date_object = datetime.date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y-%m-%d')
        string_prefix = start_date_string
        start_date_list = string_prefix.split("-")
        start_date_year = start_date_list[0]
        start_date_month = start_date_list[1]
        start_date_day = start_date_list[2]

    if end_date is not None:
        end_date_object = datetime.date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y-%m-%d')
        string_prefix = end_date_string
        end_date_list = string_prefix.split("-")
        end_date_year = end_date_list[0]
        end_date_month = end_date_list[1]
        end_date_day = end_date_list[2]

    Time_Series_df = air_quality_df.loc[
        (air_quality_df['Date'] > datetime.datetime(int(start_date_year), int(start_date_month), int(start_date_day), 0, 0, 0)) &
        (air_quality_df['Date'] < datetime.datetime(int(end_date_year), int(end_date_month), int(end_date_day), 0, 0, 0))]

    df = Time_Series_df.groupby('State')[Constant_Pollutants].mean()
    df['Sum'] = df.mean(axis=1)
    df.drop(columns=Constant_Pollutants, inplace=True)
    df = df.sort_values(by=['Sum'], ascending=False)
    df = df.iloc[0:10, :]
    y_values = df['Sum'].tolist()
    x_values = df.index.tolist()

    fig_2 = go.Figure(go.Bar(
        x=x_values,
        y=y_values,
        text=y_values
    ))

    # fig_2.update_layout(
    #     title={
    #         'text': 'Bar Plot - Top 10 Polluted States from {} to {}'.format(start_date_string, end_date_string),
    #         'y': 0.92,
    #         'x': 0.5,
    #         'xanchor': 'center',
    #         'yanchor': 'top'})

    fig_2.update_layout(plot_bgcolor=colors['background'],
                        paper_bgcolor=colors['background'],
                        font_color=colors['text'])

    fig_2.update_xaxes(
        title_text="States",
        title_font={"size": 20},
        showgrid=False,
        # zeroline=False,
        # visible=False
    )

    fig_2.update_yaxes(
        title_text="Average",
        showgrid=False,
        # zeroline=False,
        # visible=False
    )

    return fig_2
