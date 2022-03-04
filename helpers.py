from os import path

import pandas as pd
from datetime import datetime


def chunks(L, n):
    return [L[x: x+n] for x in range(0, len(L), n)]


def get_cities_in_region(np_df, region):
    return list(np_df[np_df['Область'] == region].sort_values(by='Місто')['Місто'].unique())


# def get_schedule_df():
#     return pd.read_excel(f'data/schedule-{datetime.now().strftime("%Y-%m-%d")}.xlsx')

cached_df = None
cached_date = None


def get_schedule_df():
    global cached_df
    global cached_date

    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f'data/schedule-{current_date}.xlsx'

    if (cached_df is None or cached_date != current_date) and path.exists(filename):
        cached_df = pd.read_excel(filename)
        cached_date = current_date

    return cached_df
