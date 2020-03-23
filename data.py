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

def get_dataframe(dataset):
    """Returns a DataFrame for <dataset>.

    <dataset> can be one of 'confirmed', 'deaths' or 'recovered'. If it's not, an
    ArgumentError is raised."""

    # sanity check
    check_for_CSSE_repo()
    if dataset.lower() not in ['confirmed', 'deaths', 'recovered']:
        raise ArgumentError("%s is not a valid dataset. Please use 'confirmed', 'deaths' or 'recovered'." % (dataset))

    base_path = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-'
    filename = base_path + dataset.title() + '.csv'

    return pd.read_csv(filename)

def get_country_time_series(dataset, country):
    """Returns a DataFrame with the summed number of cases for <country> from <dataset> per date.

    <dataset> can be one of 'confirmed', 'deaths' or 'recovered'. If it's not, an
    ArgumentError is raised."""

    df = get_dataframe(dataset)

    # a special case for the United States
    if country == "United States":
        country = "US"
    df = df[df['Country/Region'] == country]

    # All of these columns become irrelevant once we've filtered out the Country
    df = df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis = 'columns')

    return df.sum()

def get_total_time_series(dataset):
    """Returns a DataFrame with the summed number of cases from <dataset> per date.

    <dataset> can be one of 'confirmed', 'deaths' or 'recovered'. If it's not, an
    ArgumentError is raised."""

    df = get_dataframe(dataset)

    # All of these columns become irrelevant so we'll drop them
    df = df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis = 'columns')

    # and return the sum of all the others. 
    return df.sum()

if __name__ == "__main__":
    check_for_CSSE_repo()