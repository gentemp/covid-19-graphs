import data

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

from datetime import datetime as dt

REFERENCE_COUNTRY = 'Italy'

def align_data(df, n = None):
    values = df.to_numpy()

    result = []
    if n is None:
        result = [int(x) for x in values]

    else:
        # align time series to start on comparable dates
        # (where the number of confirmed cases >= n)
        for i in range(len(values)):
            if values[i] >= n:
                result = [int(x) for x in values[i:]]
                break

    return result

def run_for(close, country, reference = None):
    df_ref = reference
    if reference is None:
        df_ref = data.get_country_time_series('confirmed', REFERENCE_COUNTRY)

    df = data.get_country_time_series('confirmed', country)
    
    # get the timeseries of cumulative confirmed cases
    # the first four columns are province, country, lat and long
    rows = align_data(df, n = 100)
    rows_ref = align_data(df_ref, n = 100)

    fig, ax = plt.subplots()

    ax.plot(rows_ref, color = 'black', linestyle = '--')
    ax.plot(rows, color = 'red', marker ='o')
    
    ax.set_xlabel('Days Since Total Cases > 100')

    # adjust the y scale to reference country multiples
    # [0x, 20x, 40x, ... , 200x, ... NNNx]
    # since the scale for Italy has grown quite a lot past
    # the 200x mark we'll have to calculate a suitable
    # stop value based on the highest value in the series
    unit_val, max_val = rows_ref[0], max(rows_ref)
    yticks = []
    curr_val, step, tick = 0, 20, 0
    while curr_val < max_val:
        yticks.append(curr_val)

        tick += step
        curr_val = unit_val * tick

    # add that last tick to go one above the max value
    yticks.append(curr_val)
    ax.set_yticks(yticks)

    # update the labels to multiples of reference country
    ax.set_yticklabels(['%dx' % (x) for x in range(0, tick+ step, step)])
    ax.grid(True, axis = 'y')

    ax.set_title(country)

    plt.savefig(data.img_path + 'MotherJones1-Figure-%s-latest.png' % (country.replace(' ', '-')))
    if close:
        plt.close(fig)

def run(close = True, countries = None):
    reference = data.get_country_time_series('confirmed', REFERENCE_COUNTRY)

    if countries is None:
        countries = [
            'France', 'Germany',
            'Canada', 'Spain', 'Sweden',
            'Switzerland', 'United Kingdom', 'United States',

            'Iceland', 'Norway', 'Finland',
            'Estonia', 'Latvia', 'Denmark',
            'Lithuania', 'Ireland', 'Netherlands',
            'Poland', 'Belgium', 'Czechia',
            'Austria', 'Portugal', 'Greece', ]
    for country in countries:
        run_for(close, country, reference)

if __name__ == "__main__":
    run(close = False, countries = ['United States'])
    plt.show()