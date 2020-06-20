import pandas as pd

from finance_scraping import config, loading
from sql_queries import (
    get_all_data_sql,
    get_companies_sql,
    get_max_date_sql,
    get_min_date_sql,
)

ATTRIBUTES = [
    'capital',
    'last_quote',
    'last_close',
    'daily_change_abs',
    'daily_change_rel',
    'bid',
    'offer',
    'low',
    'high',
    'day_volume',
    'p_e',
    'yield_percent',
]


def query_db(sql, db_params):
    con = loading.get_connection(db_params)
    cur = con.cursor()
    try:
        cur.execute(sql)
        result = [row for row in cur]
    finally:
        con.close()
    return result


def capitalize(string):
    return string.replace("_", " ").title()


def get_attributes():
    return [{"label": capitalize(a), "value": a} for a in ATTRIBUTES]


def get_companies():
    db_params = config.get_db_env_vars()
    rows = query_db(get_companies_sql.format(db_params["table"]), db_params)
    companies = [row[0] for row in rows]
    return [{"label": c, "value": c} for c in companies]


def get_max_date():
    db_params = config.get_db_env_vars()
    rows = query_db(get_max_date_sql.format(db_params["table"]), db_params)
    return rows[0][0]


def get_min_date():
    db_params = config.get_db_env_vars()
    rows = query_db(get_min_date_sql.format(db_params["table"]), db_params)
    return rows[0][0]


def get_all_data():
    db_params = config.get_db_env_vars()
    con = loading.get_connection(db_params)
    try:
        data = pd.read_sql(
            get_all_data_sql.format(db_params["table"]),
            con)
    finally:
        con.close()
    data.set_index(pd.to_datetime(data["collection_date"]), inplace=True)
    return data
