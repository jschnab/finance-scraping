import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import sqlite3

from dash.dependencies import Input, Output
from datetime import datetime

from db_to_df import db_to_dataframe

database_path = "/home/jonathans/finance-scraping/finance-data.sq3"
data = db_to_dataframe(database_path)
data.set_index("timestamp", inplace=True)

app = dash.Dash(__name__)

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

app.layout = html.Div(
    [
        # page header
        html.Div([html.H1("Technological Companies Stocks Dashboard")]),
        # timeseries
        html.Div([html.H2("Timeseries Analysis")]),
        # dropdown grid
        html.Div(
            [
                # select y axis dropdown
                html.Div(
                    [
                        html.Div("Select y-axis", className="label"),
                        html.Div(
                            dcc.Dropdown(
                                id="y_var",
                                options=options_dropdown_y,
                                value="capital",
                                className="dropdown",
                            )
                        ),
                    ],
                    className="subcontainer-dropdown",
                ),
                # select companies dropdown
                html.Div(
                    [
                        html.Div("Select companies", className="label"),
                        html.Div(
                            dcc.Dropdown(
                                id="companies",
                                options=options_dropdown_companies,
                                value=["Nokia Oyj", "Ubisoft Entertainment"],
                                multi=True,
                                className="dropdown",
                            )
                        ),
                    ],
                    className="subcontainer-dropdown",
                ),
                # date picker
                html.Div(
                    [
                        html.Div("Select date range", className="label"),
                        html.Div(
                            dcc.DatePickerRange(
                                id="date_range",
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                initial_visible_month=datetime(2018, 12, 25),
                                className="datepicker",
                            )
                        ),
                    ],
                    className="subcontainer-dropdown",
                ),
            ],
            className="container-dropdown",
        ),
        # graph grid
        html.Div(
            [html.Div([dcc.Graph(id="timeseries")])],
            className="timeseries-container",
        ),
        html.Div(html.H2("Company rankings")),
        # tables container
        html.Div(
            [
                # single table
                html.Div(
                    [
                        html.H3("Top 10 values", className="top-values"),
                        # table top 10 values dropdown
                        html.Div(
                            [
                                html.Div("Table attribute", className="label"),
                                html.Div(
                                    dcc.Dropdown(
                                        id="drop-top-values",
                                        options=options_dropdown_y,
                                        value="capital",
                                        className="dropdown",
                                    )
                                ),
                            ]
                        ),
                        # table top 10 values
                        html.Table(id="top-ten-values"),
                    ],
                    className="container-one-table",
                ),
                # single table
                html.Div(
                    [
                        html.H3("Worst 10 values", className="top-values"),
                        # table bottom 10 values dropdown
                        html.Div(
                            [
                                html.Div("Table attribute", className="label"),
                                html.Div(
                                    dcc.Dropdown(
                                        id="drop-bottom-values",
                                        options=options_dropdown_y,
                                        value="capital",
                                        className="dropdown",
                                    )
                                ),
                            ]
                        ),
                        # table bottom 10 values
                        html.Table(id="bottom-ten-values"),
                    ],
                    className="container-one-table",
                ),
            ],
            className="container-tables",
        ),
    ],
    className="main",
)


@app.callback(
    Output(component_id="top-ten-values", component_property="children"),
    [Input(component_id="drop-top-values", component_property="value")],
)
def top_ten_values(attribute):
    sql = f"""
        SELECT name, {attribute}, date
        FROM euronext_techno
        WHERE date in (SELECT MAX(date) FROM euronext_techno)
        ORDER BY {attribute} DESC
        LIMIT 10;
    """
    con = sqlite3.connect(database_path)
    df = pd.read_sql(sql, con)
    if max(df[attribute]) > 1e6:
        df[attribute] = (df[attribute] / 1e6).round(5).apply("{:,}".format)
        df.rename(columns={attribute: f"{attribute} (M)"}, inplace=True)
    else:
        df[attribute] = df[attribute].round(5)
    output_table = html.Table(
        [html.Tr([html.Th(col) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(10)
        ]
    )
    return output_table


@app.callback(
    Output(component_id="bottom-ten-values", component_property="children"),
    [Input(component_id="drop-bottom-values", component_property="value")],
)
def bottom_ten_values(attribute):
    sql = f"""
        SELECT name, {attribute}, date
        FROM euronext_techno
        WHERE date in (SELECT MAX(date) FROM euronext_techno)
        AND {attribute} IS NOT NULL
        ORDER BY {attribute}
        LIMIT 10;
    """
    con = sqlite3.connect(database_path)
    df = pd.read_sql(sql, con)
    if max(df[attribute]) > 1e6:
        df[attribute] = (df[attribute] / 1e6).round(5).apply("{:,}".format)
        df.rename(columns={attribute: f"{attribute} (M)"}, inplace=True)
    elif max(df[attribute]) > 1e3:
        df[attribute] = (df[attribute] / 1e3).round(5).apply("{:,}".format)
        df.rename(columns={attribute: f"{attribute} (K)"}, inplace=True)
    else:
        df[attribute] = df[attribute].round(5)
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
