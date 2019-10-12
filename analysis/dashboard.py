import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd
import plotly.graph_objs as go

from db_to_df import db_to_dataframe


DATABASE = '../finance-data.sq3'
data = db_to_dataframe(DATABASE)
ubisoft = data[data['name']=='Ubisoft Entertainment']

app = dash.Dash(__name__)

trace = go.Scatter(y=ubisoft['capital'], x=ubisoft['timestamp'])

layout = go.Layout(
    title='Ubisoft Capital',
    xaxis={'title': 'Date'},
    yaxis={'title': 'Capital'})

figure = go.Figure(data=[trace], layout=layout)

app.layout = html.Div(children=[
    html.H1('Stocks Report'),
    html.H2('Evolution of Ubisoft Capital'),
    html.P('This graph shows the evolution of Ubisoft\'s capital'),
    dcc.Graph(id='stock-timeseries', figure=figure)])

if __name__ == '__main__':
    app.run_server(debug=False)
