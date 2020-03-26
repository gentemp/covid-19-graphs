import data

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

from datetime import datetime as dt

REFERENCE_COUNTRY = 'Italy'

def align_data(df, pop, n = None):
    values = df.to_numpy()

    result = []
    if n is None:
        result = [int(x) for x in values]

    else:
        # align time series to start on comparable dates
        # (where the number of confirmed deaths >= p, and
        # where p = country's population / 10 million * n)
        p = pop / 10000000.0 * n
        for i in range(len(values)):
            if values[i] >= p:
                result = [int(x) for x in values[i:]]
                break

    return result

def run_for(close, country, pop, reference = None, reference_pop = None):
    df_ref = reference
    if reference is None:
        df_ref = data.get_country_time_series('deaths', REFERENCE_COUNTRY)

    ref_pop = reference_pop
    if reference_pop is None:
        df_pop = data.get_populations([REFERENCE_COUNTRY, ])
        ref_pop = int(df_pop[df_pop['Country'] == REFERENCE_COUNTRY].Population)

    df = data.get_country_time_series('deaths', country)

    # get the timeseries of cumulative confirmed deaths
    rows = align_data(df, pop, n = 1)
    rows_ref = align_data(df_ref, ref_pop, n = 1)

    fig, ax = plt.subplots()

    ax.plot(rows_ref, color = 'black', linestyle = '--')
    ax.plot(rows, color = 'red', marker ='o')
    
    try:
        ax.vlines(len(rows) - 1, 0, 0.8,
                transform = ax.get_xaxis_transform(),
                linestyle = '--', colors = 'r')

        ax.text(len(rows) - 1, 0.85,
                "Day %d\n%.1f Deaths per Million" % (len(rows) - 1, rows[-1]/pop*1000000.0),
                horizontalalignment = 'center',
                color = 'r', fontweight = 'bold',
                transform = ax.get_xaxis_transform())

    except IndexError:
        # if we end up here it's because we haven't reached Day 0 yet
        pass

    ax.set_xlabel('Number of Days Since Day 0')

    ax.grid(True, axis = 'y')

    ax.set_title(country)

    plt.savefig(data.img_path + 'RequestedGraph1-Figure-%s-latest.png' % (country.replace(' ', '-')))
    if close:
        plt.close(fig)

def run(close = True, countries = None):
    reference = data.get_country_time_series('deaths', REFERENCE_COUNTRY)

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
    df_pop = data.get_populations(countries + [REFERENCE_COUNTRY, ])
    for country in countries:
        pop = int(df_pop[df_pop['Country'] == country].Population)
        ref_pop = int(df_pop[df_pop['Country'] == REFERENCE_COUNTRY].Population)
        run_for(close, country, pop, reference, ref_pop)

if __name__ == "__main__":
    run(close = False, countries = [
            'France', 'Germany',
            'Canada', 'Spain', 'Sweden',
            'Switzerland', 'United Kingdom', 'United States'])
    plt.show()