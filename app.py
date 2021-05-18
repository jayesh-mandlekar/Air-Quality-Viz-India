from datetime import date, datetime
import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
from matplotlib.pyplot import text
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
start_date_year = '0'
start_date_month = '0'
start_date_day = '0'
end_date_year = '0'
end_date_month = '0'
end_date_day = '0'

# ------------------
# -------------------------------------------------------------------------------------------------------

air_quality_df['Date'] = pd.to_datetime(air_quality_df['Date'])

# -------------------------------------------------------------------------------------------------------


app.layout = html.Div(children=[
    html.H1(children='Indian Air Quality User Dashboard',
            style={'textAlign': 'center'}),
    html.Label('States'),
    dcc.Dropdown(
        id='state-dropdown',
        options=[
            {'label': i, 'value': i} for i in air_quality_df['State'].unique()
        ], value="Andhra Pradesh"
    ),
    dcc.Graph(id='dotline-1-graph'),
    dcc.DatePickerRange(id='Time-Slots',
                        start_date_placeholder_text="Start Period",
                        end_date_placeholder_text="End Period",
                        calendar_orientation="vertical"
                        ),
    dcc.Graph(id='top-10-bar-graph'),
    dcc.Dropdown(id='pollutant-dropdown', options=[
        {'label': i, 'value': i} for i in Constant_Pollutants
    ], value=Constant_Pollutants[0]),
    dcc.Graph(id='pollutant-trend-histogram'),
    dcc.Graph(id='pollutant-trend-boxplot'),

])


@app.callback(
    Output('pollutant-trend-boxplot', 'figure'),
    [Input('pollutant-dropdown', 'value'),
     Input('Time-Slots', 'start_date'),
     Input('Time-Slots', 'end_date')]
)
def update_figure(selected_pollutant, start_date, end_date):
    string_prefix = "You have selected: "
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y-%m-%d')
        string_prefix = start_date_string
        start_date_list = string_prefix.split("-")
        start_date_year = start_date_list[0]
        start_date_month = start_date_list[1]
        start_date_day = start_date_list[2]

    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y-%m-%d')
        string_prefix = end_date_string
        end_date_list = string_prefix.split("-")
        end_date_year = end_date_list[0]
        end_date_month = end_date_list[1]
        end_date_day = end_date_list[2]

    Time_Series_df = air_quality_df.loc[
        (air_quality_df['Date'] > datetime(int(start_date_year), int(start_date_month), int(start_date_day), 0, 0, 0)) &
        (air_quality_df['Date'] < datetime(int(end_date_year), int(end_date_month), int(end_date_day), 0, 0, 0))]

    Required_Pollutant = selected_pollutant
    y_values = Time_Series_df.loc[:, Required_Pollutant].values.tolist()
    x_values = Time_Series_df.Date

    fig_4 = go.Figure(go.Box(
        x=y_values,
    ))

    fig_4.update_layout(
        title={
            'text': "Boxplot - Distribution of {} from {} to {}".format(Required_Pollutant, start_date_string, end_date_string),
            'y': 0.92,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig_4.update_xaxes(
        title_text="Count",
        title_font={"size": 20},
        # showgrid=False,
    )

    return fig_4



@app.callback(
    Output('pollutant-trend-histogram', 'figure'),
    [Input('pollutant-dropdown', 'value'),
     Input('Time-Slots', 'start_date'),
     Input('Time-Slots', 'end_date')]
)
def update_figure(selected_pollutant, start_date, end_date):
    string_prefix = "You have selected: "
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y-%m-%d')
        string_prefix = start_date_string
        start_date_list = string_prefix.split("-")
        start_date_year = start_date_list[0]
        start_date_month = start_date_list[1]
        start_date_day = start_date_list[2]

    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y-%m-%d')
        string_prefix = end_date_string
        end_date_list = string_prefix.split("-")
        end_date_year = end_date_list[0]
        end_date_month = end_date_list[1]
        end_date_day = end_date_list[2]

    Time_Series_df = air_quality_df.loc[
        (air_quality_df['Date'] > datetime(int(start_date_year), int(start_date_month), int(start_date_day), 0, 0, 0)) &
        (air_quality_df['Date'] < datetime(int(end_date_year), int(end_date_month), int(end_date_day), 0, 0, 0))]

    Required_Pollutant = selected_pollutant
    y_values = Time_Series_df.loc[:, Required_Pollutant].values.tolist()
    x_values = Time_Series_df.Date

    fig_3 = go.Figure(go.Histogram(
        x=y_values,
        # nbins=30,
    ))

    fig_3.update_layout(
        title={
            'text': "Histogram - Distribution of {} from {} to {}".format(Required_Pollutant, start_date_string, end_date_string),
            'y': 0.92,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig_3.update_xaxes(
        title_text="Distribution",
        title_font={"size": 20},
        # showgrid=False,
    )

    fig_3.update_yaxes(
        title_text="Count",
        # showgrid=False,
        # zeroline=False,
        # visible=False
    )

    return fig_3

@app.callback(
    Output('dotline-1-graph', 'figure'),
    Input('state-dropdown', 'value')
)
def update_figure(selected_state):
    Bar_Plot_Pivot = air_quality_df.loc[(air_quality_df['State'] == selected_state),
                                        ['State', 'Sulphur_Dioxide', 'Nitrogen_Dioxide', 'Respirable_Suspended_Particulate_Matter']].groupby(by='State').mean()

    Pollutants_Numbers = Bar_Plot_Pivot.loc[selected_state].tolist()
    Pollutants_Numbers = ['%.2f' % i for i in Pollutants_Numbers]

    fig_1 = go.Figure(go.Scatter(
        x=Constant_Pollutants,
        y=Pollutants_Numbers,
        mode='lines+markers+text',
        marker=dict(
            color='Red',
            size=40,
            line=dict(
                color='MediumPurple',
                width=4
            )
        ),
        text=Pollutants_Numbers,
        textposition="top center"
    ))

    fig_1.update_layout(
        title={
            'text': "Scatter and Line Plot - Amount of {}, {}, {} in {}".format(Constant_Pollutants[0], Constant_Pollutants[1], Constant_Pollutants[2], selected_state),
            'y': 0.92,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig_1.update_xaxes(
        title_text="Pollutant",
        title_font={"size": 20},
        showgrid=False,
    )

    fig_1.update_yaxes(
        title_text="Average",
        showgrid=False,
        zeroline=False,
        visible=False
    )

    return fig_1


@app.callback(
    Output('top-10-bar-graph', 'figure'),
    [Input('Time-Slots', 'start_date'),
     Input('Time-Slots', 'end_date')]
)
def update_figure(start_date, end_date):
    string_prefix = "You have selected: "
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%Y-%m-%d')
        string_prefix = start_date_string
        start_date_list = string_prefix.split("-")
        start_date_year = start_date_list[0]
        start_date_month = start_date_list[1]
        start_date_day = start_date_list[2]

    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%Y-%m-%d')
        string_prefix = end_date_string
        end_date_list = string_prefix.split("-")
        end_date_year = end_date_list[0]
        end_date_month = end_date_list[1]
        end_date_day = end_date_list[2]

    Time_Series_df = air_quality_df.loc[
        (air_quality_df['Date'] > datetime(int(start_date_year), int(start_date_month), int(start_date_day), 0, 0, 0)) &
        (air_quality_df['Date'] < datetime(int(end_date_year), int(end_date_month), int(end_date_day), 0, 0, 0))]

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

    fig_2.update_layout(
        title={
            'text': 'Bar Plot - Top 10 Polluted States from {} to {}'.format(start_date_string, end_date_string),
            'y': 0.92,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    fig_2.update_xaxes(
        title_text="States",
        title_font={"size": 20},
    )

    fig_2.update_yaxes(
        title_text="Average",
        # showgrid=False,
        # zeroline=False,
        # visible=False
    )

    return fig_2


if __name__ == '__main__':
    app.run_server(debug=True)
