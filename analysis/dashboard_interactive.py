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

database_path = "/home/jonathans/finance-scraping/finance-data.sq3"
data = db_to_dataframe(database_path)
data.set_index("timestamp", inplace=True)

external_stylesheets = [
    "https://codepen.io/chriddyp/pen/bWLwgP.css",
    {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO",
        "crossorigin": "anonymous",
    },
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

attributes = [
    "capital",
    "lastquote",
    "lastabs",
    "lastrel",
    "bid",
    "offer",
    "low",
    "high",
    "dayvol",
    "pe",
    "yield",
]

companies = data["name"].unique()

min_date = data.index.min().strftime("%Y-%m-%d")
max_date = data.index.max().strftime("%Y-%m-%d")

options_dropdown_y = [{"label": a, "value": a} for a in attributes]
options_dropdown_companies = [{"label": c, "value": c} for c in companies]

dropdown_y_var = dcc.Dropdown(
    id="y_var", options=options_dropdown_y, value="capital"
)

dropdown_companies = dcc.Dropdown(
    id="companies",
    options=options_dropdown_companies,
    value=["Nokia Oyj", "Ubisoft Entertainment"],
    multi=True,
)

date_picker = dcc.DatePickerRange(
    id="date_range",
    min_date_allowed=min_date,
    max_date_allowed=max_date,
    initial_visible_month=datetime(2018, 12, 25),
    style={"background": "black"},
)

dropdown_top_prog = dcc.Dropdown(
    id="drop-top-prog",
    options=options_dropdown_y,
    value="capital",
    style={"width": "150px"},
)

div_var_table_prog = html.Div(
    children=[html.Label("Attribute"), dropdown_top_prog]
)

div_variables = html.Div(
    children=[
        html.Div("Y-axis variable", className="two columns"),
        html.Div(dropdown_y_var, className="two columns"),
        html.Div("Companies", className="two columns"),
        html.Div(dropdown_companies, className="two columns"),
        html.Div("Period selection", className="two columns"),
        html.Div(date_picker, className="two columns"),
    ],
    className="twelve columns",
)

app.layout = html.Div(
    children=[
        html.H1("Technological Companies Stocks Dashboard"),
        html.H2("Timeseries Analysis"),
        html.Div(children=[div_variables], className="twelve columns"),
        dcc.Graph(id="timeseries"),
        html.H2("Top 10"),
        html.Div(children=[div_var_table_prog]),
        html.Table(id="top-ten-prog"),
    ],
    className="twelve columns",
)


@app.callback(
    Output(component_id="top-ten-prog", component_property="children"),
    [Input(component_id="drop-top-prog", component_property="value")],
)
def top_ten_progressions(attribute):
    sql = f"""
        SELECT name, {attribute}, date
        FROM euronext_techno
        WHERE date in (SELECT MAX(date) FROM euronext_techno)
        ORDER BY {attribute} DESC
        LIMIT 10;
        """
    con = sqlite3.connect(database_path)
    df = pd.read_sql(sql, con)
    output_table = html.Table(
        [html.Tr([html.Th(col) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(10)
        ]
    )
    return output_table


@app.callback(
    Output(component_id="timeseries", component_property="figure"),
    [
        Input(component_id="y_var", component_property="value"),
        Input(component_id="companies", component_property="value"),
        Input(component_id="date_range", component_property="start_date"),
        Input(component_id="date_range", component_property="end_date"),
    ],
)
def timeseries_plot(y_value, companies, start, end):
    traces = []
    for c in companies:
        trace = go.Scatter(
            name=c,
            x=data[data["name"] == c][start:end].index,
            y=data[data["name"] == c][y_value][start:end],
        )
        traces.append(trace)

    layout = go.Layout(
        title=f"Timeseries analysis of {y_value}",
        xaxis={"title": "Date"},
        yaxis={"title": y_value},
    )

    output_plot = go.Figure(data=traces, layout=layout)

    return output_plot


if __name__ == "__main__":
    app.run_server(debug=True)
