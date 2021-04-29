import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Dataset Manipulation and Analysis
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

app.layout = html.Div(children=[
    html.H1(children='Indian Air Quality User Dashboard', style={'textAlign':'center'}),
    html.Label('States'),
    dcc.Dropdown(
        id='state-dropdown',
        options=[
            {'label':i, 'value':i} for i in air_quality_df['State'].unique()
        ], value="Andhra Pradesh"
        ),
    dcc.Graph(id='bar-1-graph')
])

@app.callback(
    Output('bar-1-graph', 'figure'),
    Input('state-dropdown', 'value')
)
def update_figure(selected_state):
    Bar_Plot_Pivot = air_quality_df.loc[(air_quality_df['State'] == selected_state), 
    ['State', 'Sulphur_Dioxide', 'Nitrogen_Dioxide', 'Respirable_Suspended_Particulate_Matter']].groupby(by='State').mean()

    Constant_Pollutants = ['Sulphur_Dioxide', 'Nitrogen_Dioxide',
                           'Respirable_Suspended_Particulate_Matter']

    Pollutants_Numbers = Bar_Plot_Pivot.loc[selected_state].tolist()

    fig = px.bar(x=Constant_Pollutants,
                 y=Pollutants_Numbers,
                 labels=dict(x="Pollutant", y="Average"),
                 text=Pollutants_Numbers
                 )
    fig.update_layout(
        title={
            'text': "Bar Plot - Amount of {}, {}, {} in {}".format(Constant_Pollutants[0], Constant_Pollutants[1], Constant_Pollutants[2], selected_state),
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)
