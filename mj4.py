import data

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

from datetime import datetime as dt
from datetime import timedelta

from statistics import mean

def align_data(df, n = None, d = None):
    if d:
        # this graph starts on the date <d> so we'll
        # cut out all columns before that
        df = df[d:]

    dates = df.index
    values = df.to_numpy()

    if n is None:
        return values, dates

    else:
        # align the time series to start on the day
        # when the number of confirmed deaths >= n
        for i in range(len(values)):
            if values[i] >= n:
                return values[i:], dates[i:]

    return [], []

def change_rate(values, dates):
    result = []

    for i in range(1, len(values)):
        result.append(values[i] - values[i-1])

    return result, dates[1:]

def rolling_average(values, dates, n):
    result = []

    # calculate a rolling average of n days
    for i in range(n, len(values)):
        result.append(mean(values[i-n:i]))

    return result, dates[3:-1]

def fit_a_line(values, deg = 2):
    x = np.linspace(0, len(values), len(values))
    return np.poly1d(np.polyfit(x, values, deg))

def extend_dates(dates, n = None):
    if n is None:
        n = 7 # days

    result = list(dates)
    curr = dt.strptime(dates[-1], "%m/%d/%y")
    for i in range(n):
        curr += timedelta(days = 1)
        result.append(dt.strftime(curr, "%m/%d/%y"))

    return [dt.strftime(dt.strptime(d, "%m/%d/%y"), "%b %d") for d in result]

def run_for(close, country):
    df = data.get_country_time_series('deaths', country)

    # get the timeseries of cumulative confirmed deaths
    # starting on the day of the first death
    values, dates = align_data(df, n = 1)

    # calculate the rolling average of the confirmed deaths
    _values, _ = rolling_average(values, dates, n = 4)

    # calculate the rolling average of the change rate
    rows, dates = rolling_average(*change_rate(values, dates), n = 4)

    # calcualate the percentage of change rate/total deaths
    _rows = [(r/v)*100 for r, v in zip(rows, _values)]

    # we'll start on the first day > 0%
    for i in range(len(_rows)):
        if _rows[i] > 0:
            _rows = _rows[i:]
            dates = dates[i:]
            break

    fig, ax = plt.subplots(figsize = [14, 5])
    ax.plot(_rows, color = 'red', marker ='o')
    
    _dates = extend_dates(dates, 7)

    p1 = fit_a_line(_rows, deg = 1)
    t = np.linspace(0, len(_dates), len(_dates))

    ax.plot(_dates, p1(t), color = '#ff0000', linestyle ='--')

    ax.grid(True)

    ax.set_title(country)

    ax.set_yticklabels(['%d%%' % (x) for x in ax.get_yticks()])
    ax.set_xticks(_dates[::2])

    plt.setp(ax.get_xticklabels(), rotation = 30)

    plt.savefig(data.img_path + 'MotherJones4-Figure-%s-latest.png' % (country.replace(' ', '-')))
    if close:
        plt.close(fig)

def run(close = True, countries = None):
    if countries is None:
        countries = [
            'Italy', 'France', 'Germany',
            'Canada', 'Spain', 'Sweden',
            'Switzerland', 'United Kingdom', 'United States', ]

            #'Iceland', 'Norway', 'Finland',
            #'Estonia', 'Latvia', 'Denmark',
            #'Lithuania', 'Ireland', 'Netherlands',
            #'Poland', 'Belgium', 'Czechia',
            #'Austria', 'Portugal', 'Greece', ]
    for country in countries:
        run_for(close, country)

if __name__ == "__main__":
    run(close = False)
    plt.show()