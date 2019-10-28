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

    # timeseries
    html.Div([html.H2('Timeseries Analysis')]),

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
            ]),

            # date picker
            html.Div([
                html.Div('Select date range', className='three columns'),
                html.Div(dcc.DatePickerRange(
                    id='date_range',
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    initial_visible_month=datetime(2018, 12, 25),
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
    ]),

    html.Div(html.H2('Top 10')),

    # drop down
    html.Div([

        html.Div([

            # table option
            html.Div([
                html.Div('Table attribute', className='six columns'),
                html.Div(dcc.Dropdown(
                    id='drop-top-prog',
                    options=options_dropdown_y,
                    value='capital',
                    className='six columns'))
            ])
        ], className='three columns'),

        # empty
        html.Div(className='nine columns')

    ], className='twelve columns'),

    # table top 10 progressions
    html.Div([
        html.Div(className='one column'),
        html.Div([
            html.Table(id='top-ten-prog')
        ], className='five columns'),
        html.Div(className='six columns')
    ])
])


@app.callback(
    Output(component_id='top-ten-prog', component_property='children'),
    [Input(component_id='drop-top-prog', component_property='value')])
def top_ten_progression(attribute):
    sql = f"""
        SELECT name, {attribute}, date
        FROM euronext_techno
        WHERE date in (SELECT MAX(date) FROM euronext_techno)
        ORDER BY {attribute} DESC
        LIMIT 10;
    """
    con = sqlite3.connect(database_path)
    df = pd.read_sql(sql, con)
    output_table = html.Table([
        html.Tr([html.Th(col) for col in df.columns])
    ] + [
        html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(10)
    ])
    return output_table


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
