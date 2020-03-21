## access data from the COVID-19 CSVs

import numpy as np
import pandas as pd

import os

def check_for_CSSE_repo():
    msg = """Cannot find the COVID-19 repository!

In order to use this repo yourself you'll have to `clone https://github.com/CSSEGISandData/COVID-19.git` first."""
    if 'COVID-19' not in os.listdir('.'):
        raise FileNotFoundError(msg)

if __name__ == "__main__":
    check_for_CSSE_repo()