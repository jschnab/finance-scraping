import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
from datetime import datetime
import os
import pandas as pd
import plotly.graph_objs as go
import sqlite3

from db_to_df import db_to_dataframe

database_path = '/home/jonathans/finance-scraping/finance-data.sq3'
data = db_to_dataframe(database_path)
data.set_index('timestamp', inplace=True)

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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

app.layout = html.Div([

    # page header
    html.Div([html.H1('Technological Companies Stocks Dashboard')]),

    # dropdown grid
    html.Div([

        html.Div([

            # select y axis dropdown
            html.Div([
                html.Div('Select y-axis', className='three columns'),
                html.Div(dcc.Dropdown(
                    id='y_var',
                    options=options_dropdown_y,
                    value='capital',
                    className='nine columns'))
            ]),

            # select companies dropdown
            html.Div([
                html.Div('Select companies', className='three columns'),
                html.Div(dcc.Dropdown(
                    id='companies',
                    options=options_dropdown_companies,
                    value=['Nokia Oyj', 'Ubisoft Entertainment'],
                    multi=True,
                    className='nine columns'))
            ])
        ], className='six columns'),

            # empty
            html.Div(className='six columns'),
    ], className='twelve columns'),


    # graph grid
    html.Div([
        html.Div([
            dcc.Graph(id='timeseries')
        ], className='twelve columns')
    ])
])

@app.callback(
    Output(component_id='timeseries', component_property='figure'),
    [Input(component_id='y_var', component_property='value'),
    Input(component_id='companies', component_property='value')])
def timeseries_plot(y_value, companies):
    traces = []
    for c in companies:
        trace = go.Scatter(
            name=c,
            x=data[data['name']==c].index,
            y=data[data['name']==c][y_value])
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
