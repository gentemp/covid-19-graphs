## access data from the COVID-19 CSVs

import numpy as np
import pandas as pd

import os

img_path = 'covid-19-graphs.wiki/img/'

def check_for_CSSE_repo():
    msg = """Cannot find the COVID-19 repository!

In order to use this repo yourself you'll have to `clone https://github.com/CSSEGISandData/COVID-19.git` first."""
    if 'COVID-19' not in os.listdir('.'):
        raise FileNotFoundError(msg)

def get_total_time_series(dataset):
    """Returns a DataFrame with the summed number of cases from <dataset> per date.

    <dataset> can be one of 'confirmed', 'deaths' or 'recovered'. If it's not, an
    ArgumentError is raised."""

    check_for_CSSE_repo() # sanity check
    if dataset.lower() not in ['confirmed', 'deaths', 'recovered']:
        raise ArgumentError("%s is not a valid dataset. Please use 'confirmed', 'deaths' or 'recovered'." % (dataset))

    base_path = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-'
    filename = base_path + dataset.title() + '.csv'

    c = pd.read_csv(filename)

    # All of these columns become irrelevant so we'll drop them
    c = c.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis = 'columns')

    # and return the sum of all the others. 
    return c.sum()

if __name__ == "__main__":
    check_for_CSSE_repo()