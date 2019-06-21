#!/usr/bin/env python3

# import data from sqlite3 database into pandas dataframe

import pandas as pd
import numpy as np
import sqlite3

def db_to_dataframe(db_name):
    """Reads a table of financial data stored in a table named euronext_techno
from a SQLite3 database and converts it into a pandas dataframe.

    Parameters:
    db_name (str): name of the SQLite3 database
    
    Returns:
    pandas.DataFrame: dataframe containing table data"""

    # get data from database as a list of rows
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('SELECT * FROM euronext_techno;')
    data = [line for line in cur]
    cur.execute('PRAGMA table_info(euronext_techno);')
    fields = [line[1] for line in cur]
    cur.close()
    con.close()

    # make a dataframe and merge time and date columns
    df = pd.DataFrame(data, columns=fields)
    #df = df.astype({'date':np.datetime64, 'time':np.datetime64})
    df['timestamp'] = pd.to_datetime(df['date'] + ' ' + df['time'])
    for i in ['date', 'time']:
        df.drop(i, axis=1, inplace=True)

    return df
