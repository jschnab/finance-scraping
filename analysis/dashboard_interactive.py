import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime
import os
import pandas as pd
import plotly.graph_objs as go

from db_to_df import db_to_dataframe

data = db_to_dataframe('../finance-data.sq3')
data.set_index('timestamp', inplace=True)

app = dash.Dash(__name__)

attributes = [
    'capital',
    'lastquote',
    'lastabs',
    'lastrel',
    'bid',
    'offer',
    'low',
    'high',
    'dayvol',
    'pe',
    'yield'
]

companies = data['name'].unique()

min_date = data.index.min().strftime('%Y-%m-%d')
max_date = data.index.max().strftime('%Y-%m-%d')

options_dropdown_y = [{'label': a, 'value': a} for a in attributes]
options_dropdown_companies = [{'label': c, 'value': c} for c in companies]

dropdown_y_var = dcc.Dropdown(
    id='y_var',
    options=options_dropdown_y,
    value='capital')

dropdown_companies = dcc.Dropdown(
    id='companies',
    options=options_dropdown_companies,
    value=['Nokia Oyj', 'Ubisoft Entertainment'],
    multi=True)

date_picker = dcc.DatePickerRange(
        id='date_range',
        min_date_allowed=min_date,
        max_date_allowed=max_date,
        initial_visible_month=datetime(2018, 12, 25),
        style={'background': 'black'})

div_variables = html.Div(
    children=[
        html.Label('Y-axis variable'),
        dropdown_y_var,
        html.Label('Companies'),
        dropdown_companies,
        date_picker],
    style={'columnCount': 1, 'display': 'inline-block'})

app.layout = html.Div(children=[
    html.H1('Technological Companies Stocks Dashboard'),
    html.H2('Timeseries Analysis'),
    html.Div(children=[div_variables]),
    dcc.Graph(id='timeseries')])

@app.callback(
    Output(component_id='timeseries', component_property='figure'),
    [Input(component_id='y_var', component_property='value'),
    Input(component_id='companies', component_property='value'),
    Input(component_id='date_range', component_property='start_date'),
    Input(component_id='date_range', component_property='end_date')])
def timeseries_plot(y_value, companies, start, end):
    traces = []
    for c in companies:
        trace = go.Scatter(
            name=c,
            x=data[data['name']==c][start:end].index,
            y=data[data['name']==c][y_value][start:end])
        traces.append(trace)

    layout = go.Layout(
        title=f'Timeseries analysis of {y_value}',
        xaxis={'title': 'Date'},
        yaxis={'title': y_value})

    output_plot = go.Figure(
        data=traces,
        layout=layout)

    return output_plot

if __name__ == '__main__':
    app.run_server(debug=True)
