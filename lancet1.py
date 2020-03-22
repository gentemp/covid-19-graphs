import data

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt

if __name__ == "__main__":
    confirmed = data.get_total_time_series('confirmed')
    deaths = data.get_total_time_series('deaths')

    # cut out earlier dates
    confirmed = confirmed['1/26/20':]
    deaths = deaths['1/26/20':]

    # re-estimate mortality rates by dividing the number of deaths
    # on a given day by the number of patients with confirmed COVID-19
    # infection 14 days before.

    ratio, dates = [], []
    for i in range(len(deaths)):
        j = i - 14
        if j >= 0:
            dates.append(deaths.index[i])
            ratio.append(float(deaths[i]) / confirmed[j] * 100)

    fig, ax = plt.subplots(figsize = [12, 5])
    ax.plot(dates, ratio, 'bo-')

    ax.set_ylabel('Mortality rate (%)')
    ax.set_ybound(0, 25)

    ax.set_xlabel('WHO report date')
    ax.set_xticks(dates[::5])

    plt.savefig(data.img_path + 'Lancet1-Figure1-new.png')
