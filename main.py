import httpx
import pandas as pd
from flask import Flask
import csv
import nve
import frost
import matplotlib.pyplot as plt

magazine_api_base = "https://biapi.nve.no/magasinstatistikk/api/magasinstatistikk/"
weather_api_base = "https://frost.met.no/"

pd.plotting.register_matplotlib_converters()
#pd.set_option('display.max_columns', None)


def json_to_dataframe(json):
    df = pd.json_normalize(json)
    return df



def main():
    test = httpx.get('https://biapi.nve.no/magasinstatistikk/api/magasinstatistikk/HentOffentligData')

    print(test.status_code)
    # Magazine Data
    df_public_mg_data = nve.get_magazine_data("HentOffentligData")
    t = nve.clean_transform_mag_data(df_public_mg_data)
    print(t.dtypes)
    parameters = "?sources=SN18700&referencetime=2022-01-01%2F2022-02-01&elements=accumulated(percipitation_amount)"

    df_observations = frost.get_observations(parameters=parameters)
    v = frost.clean_transform_observations(df_observations)

    # TODO: Fix this
    plt.plot(t.index, t['fyllingsgrad'])
    plt.ylabel("Some Numbers")
    plt.show()


if __name__ == "__main__":
    main()
