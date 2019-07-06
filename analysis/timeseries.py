#!/usr/bin/python3

# plots a time series

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pandas as pd

def plot_time_series(
        x,
        y,
        ylabel='',
        title='',
        time_interval='month'
):
    """
    Plots a time series with datetime as x and variable as y.

    Parameters:
    x (list-like): datetimes
    y (list-like): variable
    ylabel (str): label of the y axis
    title (str): title of the plot
    time_interval (str): datetime interval between x axis ticks
                         accepted values are 'month' or 'week'

    Returns:
    None
    """
    
    # convert datetimes to datetime objects
    if not isinstance(x.iloc[0], pd._libs.tslibs.timestamps.Timestamp):
        dates = [datetime.strptime(i, "%Y-%m-%d") for i in x]
    else:
        dates = x

    # plot data
    fig, ax = plt.subplots()
    ax.plot(dates, y)

    # modify x axis
    if time_interval == 'month':
        ax.get_xaxis().set_major_locator(mdates.MonthLocator(interval=1))
        ax.get_xaxis().set_major_formatter(mdates.DateFormatter('%b %Y'))
    elif time_interval == 'week':
        ax.get_xaxis().set_major_locator(mdates.DayLocator(interval=7))
        ax.get_xaxis().set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
    fig.autofmt_xdate()

    # adjust figure appearance
    for i in ['top', 'right', 'bottom', 'left']:
        ax.spines[i].set_visible(False)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=16)
    if title:
        ax.set_title(title, fontsize=18)
    ax.grid(color='grey', linestyle=':')

    plt.show()
