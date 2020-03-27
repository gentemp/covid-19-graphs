import data

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
from scipy.stats import norm

from datetime import datetime as dt
from datetime import timedelta

from statistics import mean

def align_data(df, n = None):
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

    dn = int(n/2)
    return result, dates[dn:-dn]

def run_for(close, country):
    df = data.get_country_time_series('deaths', country)

    # get the timeseries of cumulative confirmed deaths
    # starting on the day of the first death
    values, dates = align_data(df, n = 1)

    # calculate the rolling average of the change rate
    rows, dates = rolling_average(*change_rate(values, dates), n = 4)

    # calculate a date range to cover up to 2020-05-08
    _dates = []
    curr = dt.strptime(dates[0], "%m/%d/%y")
    while curr <= dt.strptime('5/8/20', "%m/%d/%y"):
        _dates.append(dt.strftime(curr, "%b %d"))
        curr += timedelta(days = 1)

    # adjust the dates to correct format
    #dates = [dt.strftime(dt.strptime(d, "%m/%d/%y"), "%b %d") for d in dates]

    fig, ax = plt.subplots(figsize = [12, 5])
    ax.plot(rows, color = 'red', marker ='o')
    ax.grid(True)

    ax.set_title(country)

    # plot a 9 week long normal curve with height 1000
    # NOTE! This is the equivalent of 'eyeball fitting'
    # the normal curve. The parameters for scale and the
    # multiplier of 27,500 are there to make the curve
    # 'fit' the data.
    x = np.linspace(0, len(_dates), len(_dates))
    y = norm.pdf(x, loc = (len(_dates) / 2), scale = 11)

    ax.plot(x, [v * 27500 for v in y], color = 'grey')
    ax.set_xticks(x[4::7])

    ax.set_xticklabels(_dates[4::7])
    plt.setp(ax.get_xticklabels(), rotation = 30)

    plt.savefig(data.img_path + 'MotherJones3-Figure-%s-latest.png' % (country.replace(' ', '-')))
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
    run(close = False, countries = ['Italy'])
    plt.show()