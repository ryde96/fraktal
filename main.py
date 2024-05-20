import httpx
import pandas as pd
from flask import Flask
import csv
import nve
import frost
import matplotlib.pyplot as plt
from ydata_profiling import ProfileReport

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

    df_observations = frost.get_observations()
    v = frost.clean_transform_observations(df_observations)

    print(v.head)
    frames = [t, v]

    result = pd.merge(t, v, on='month')
    print("------")
    print(result.head)
    result.to_csv("out.csv", index=False)
    result.to_json("out.json", index=False)

    # TODO: Fix this
    fig1, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    ax1.plot(result['fyllingsgrad'])
    ax2.plot(result['precipitation'])
    fig1.savefig("test.png")

    plt.plot(t['fyllingsgrad'])
    plt.ylabel("Fyllingsgrad")
    plt.xlabel("Måned")
    plt.savefig('fyllingsgrad.png')
    plt.cla()
    plt.plot(t['fylling_TWh'])
    plt.ylabel("Fyllingsgrad TWh")
    plt.xlabel("Måned")
    #plt.show()
    plt.savefig('fyllingsgrad_twh.png')
    plt.cla()
    plt.plot(result['precipitation'])
    plt.ylabel("Nedbør MM")
    plt.xlabel("Måned")
    plt.savefig('precipitation.png')


if __name__ == "__main__":
    main()
