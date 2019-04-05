#!/usr/bin/env python3

# import data from sqlite3 database into pandas dataframe

import pandas as pd
import numpy as np
import sqlite3

def db_to_dataframe(db_name):
    """Reads a table of financial data stored in a table name euronext_techno
a SQLite3 database and convert it into a pandas dataframe.

    Parameters:
    db_name (str): name of the SQLite3 database
    
    Returns:
    pandas.DataFrame: dataframe containing table data"""

    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute('SELECT * FROM euronext_techno;')
    data = [line for line in cur]
    cur.execute('PRAGMA table_info(euronext_techno);')
    fields = [line[1] for line in cur]
    cur.close()
    con.close()
    df = pd.DataFrame(data, columns=fields)
    df.astype({'date':np.datetime64, 'time':np.datetime64})

    return df
