import httpx
import pandas as pd
import sys
import numpy as np
sys.setrecursionlimit(1500)

magazine_api_base = "https://biapi.nve.no/magasinstatistikk/api/magasinstatistikk/"


def public_mag_data(omr_type=''):
    df = clean_transform_mag_data(
        get_magazine_data('HentOffentligData')
        , omr_type)

    return df.to_json(orient="records")


def get_magazine_data(endpoint):
    r = httpx.get(magazine_api_base+endpoint)
    if r.status_code != 200:
        return pd.DataFrame.empty
    df = pd.json_normalize(r.json())
    return df




def clean_transform_mag_data(dataframe, omr_type=''):
    dataframe.dropna()
    df = dataframe[dataframe['iso_aar'] == 2022]
    df = df[df['omrnr'] == 1]
    df = df.sort_values(by=['iso_uke'])
    if omr_type != '':
        df = df[df['omrType'] == omr_type]

    print(df.dtypes)
    df['dato_Id'] = pd.to_datetime(df['dato_Id'])
    print(df)
    print(df['dato_Id'])
    print("-------")
    df = df.groupby(
        pd.PeriodIndex(df['dato_Id'], freq="M"))[
        ['fyllingsgrad',
         'kapasitet_TWh',
         'fylling_TWh',
         'endring_fyllingsgrad',
         ]
    ].mean()
    print(df)
    seq = list(range(1, len(df)))
    print(seq)
    #df['id'] = seq
    #df = df.set_index('id')
    print("-------")
    print(df)
    return df
