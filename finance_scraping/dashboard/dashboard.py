import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output

from finance_scraping import config, loading

from sql_queries import (
    bottom_prog_sql,
    bottom_val_sql,
    top_prog_sql,
    top_val_sql,
)
from text import (
    summary_1,
    summary_2,
)
from utils import (
    capitalize,
    get_all_data,
    get_attributes,
    get_companies,
    get_max_date,
    get_min_date,
)


def serve_layout():
    attributes = get_attributes()

    return html.Div(
        [
            # page title
            html.Title(["Euronext Technology Companies"]),
            # page header
            html.Div([html.H1("Technological Companies Stocks Dashboard")]),
            # summary
            html.Div([
                html.H2("Summary", className="summary-title"),
                html.P(summary_1, className="summary-text"),
                html.P(summary_2, className="summary-text"),
                html.A(
                    "Please visit my GitHub!",
                    href="https://github.com/jschnab/finance-scraping.git",
                    className="summary-text",
                ),
            ], className="summary"),
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
                                    options=attributes,
                                    value="last_quote",
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
                                    options=get_companies(),
                                    value=[
                                        "Capgemini SE",
                                        "Ubisoft Entertainment",
                                        "Dassault Systemes SE",
                                    ],
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
                                    min_date_allowed=get_min_date(),
                                    max_date_allowed=get_max_date(),
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
                                            options=attributes,
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
                            html.H3("Bottom 10 values", className="top-values"),
                            # table bottom 10 values dropdown
                            html.Div(
                                [
                                    html.Div("Table attribute", className="label"),
                                    html.Div(
                                        dcc.Dropdown(
                                            id="drop-bottom-values",
                                            options=attributes,
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
                    # single table
                    html.Div(
                        [
                            html.H3("Top 10 movers", className="top-values"),
                            # table top 10 progressions dropdown
                            html.Div(
                                [
                                    html.Div("Table attribute", className="label"),
                                    html.Div(
                                        dcc.Dropdown(
                                            id="drop-top-prog",
                                            options=attributes,
                                            value="capital",
                                            className="dropdown",
                                        )
                                    ),
                                ]
                            ),
                            # table top 10 progressions
                            html.Table(id="top-ten-prog"),
                        ],
                        className="container-one-table",
                    ),
                    # single table
                    html.Div(
                        [
                            html.H3(
                                "Bottom 10 movers",
                                className="top-values"),
                            # table top 10 progressions dropdown
                            html.Div(
                                [
                                    html.Div("Table attribute", className="label"),
                                    html.Div(
                                        dcc.Dropdown(
                                            id="drop-bottom-prog",
                                            options=attributes,
                                            value="capital",
                                            className="dropdown",
                                        )
                                    ),
                                ]
                            ),
                            # table bottom 10 progressions
                            html.Table(id="bottom-ten-prog"),
                        ],
                        className="container-one-table",
                    )
                ],
                className="container-tables",
            ),
        ],
        className="main",
    )


app = dash.Dash("Finance Scraping")
server = app.server
app.layout = serve_layout()


@app.callback(
    Output(component_id="top-ten-values", component_property="children"),
    [Input(component_id="drop-top-values", component_property="value")],
)
def top_ten_values(attribute):
    con = loading.get_connection(config.get_db_env_vars())
    df = pd.read_sql(top_val_sql.format(attribute=attribute), con)
    con.close()
    if attribute == "yield_percent":
        df["yield_percent"] = df["yield_percent"] * 100
    if max(df[attribute]) > 1e6:
        df[attribute] = (df[attribute] / 1e6).round(5).apply("{:,}".format)
        df.rename(columns={attribute: f"{attribute} (M)"}, inplace=True)
    else:
        df[attribute] = df[attribute].round(5)
    output_table = html.Table(
        [html.Tr([html.Th(capitalize(col)) for col in df.columns])]
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
    con = loading.get_connection(config.get_db_env_vars())
    df = pd.read_sql(bottom_val_sql.format(attribute=attribute), con)
    con.close()
    if attribute == "yield_percent":
        df["yield_percent"] = df["yield_percent"] * 100
    if max(df[attribute]) > 1e6:
        df[attribute] = (df[attribute] / 1e6).round(5).apply("{:,}".format)
        df.rename(columns={attribute: f"{attribute} (M)"}, inplace=True)
    elif max(df[attribute]) > 1e3:
        df[attribute] = (df[attribute] / 1e3).round(5).apply("{:,}".format)
        df.rename(columns={attribute: f"{attribute} (K)"}, inplace=True)
    else:
        df[attribute] = df[attribute].round(5)
    output_table = html.Table(
        [html.Tr([html.Th(capitalize(col)) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(10)
        ]
    )
    return output_table


@app.callback(
    Output(component_id="top-ten-prog", component_property="children"),
    [Input(component_id="drop-top-prog", component_property="value")],
)
def top_ten_prog(attribute):
    con = loading.get_connection(config.get_db_env_vars())
    df = pd.read_sql(top_prog_sql.format(attribute=attribute), con)
    con.close()
    if attribute == "yield_percent":
        df["diff"] = df["diff"] * 100
    if max(df["diff"]) > 1e6:
        df["diff"] = (df["diff"] / 1e6).round(5).apply("{:,}".format)
        df.rename(columns={"diff": f"diff (M)"}, inplace=True)
    elif max(df["diff"]) > 1e3:
        df["diff"] = (df["diff"] / 1e3).round(5).apply("{:,}".format)
        df.rename(columns={"diff": f"diff (K)"}, inplace=True)
    else:
        df["diff"] = df["diff"].round(5)

    output_table = html.Table(
        [html.Tr([html.Th(capitalize(col)) for col in df.columns])]
        + [
            html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
            for i in range(10)
        ]
    )
    return output_table


@app.callback(
    Output(component_id="bottom-ten-prog", component_property="children"),
    [Input(component_id="drop-bottom-prog", component_property="value")],
)
def bottom_ten_prog(attribute):
    con = loading.get_connection(config.get_db_env_vars())
    df = pd.read_sql(bottom_prog_sql.format(attribute=attribute), con)
    con.close()
    if attribute == "yield_percent":
        df["diff"] = df["diff"] * 100
    if max(df["diff"]) > 1e6:
        df["diff"] = (df["diff"] / 1e6).round(5).apply("{:,}".format)
        df.rename(columns={"diff": f"diff (M)"}, inplace=True)
    elif max(df["diff"]) > 1e3:
        df["diff"] = (df["diff"] / 1e3).round(5).apply("{:,}".format)
        df.rename(columns={"diff": f"diff (K)"}, inplace=True)
    else:
        df["diff"] = df["diff"].round(5)

    output_table = html.Table(
        [html.Tr([html.Th(capitalize(col)) for col in df.columns])]
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
    data = get_all_data()
    traces = []
    for c in companies:
        trace = go.Scatter(
            name=c,
            x=data[data["company_name"] == c][start:end].index,
            y=data[data["company_name"] == c][y_value][start:end],
        )
        traces.append(trace)

    layout = go.Layout(
        title=f"Timeseries analysis of {capitalize(y_value)}",
        xaxis={"title": "Date"},
        yaxis={"title": capitalize(y_value)},
    )

    output_plot = go.Figure(data=traces, layout=layout)
    return output_plot


if __name__ == "__main__":
    app.run_server()
