import httpx
import pandas as pd

client_id = "553f1144-551b-450c-8abe-0f696239188d"
client_secret = ""

def frost_data():
    df = clean_transform_observations(get_observations())
    return df.to_json(orient="records")

def get_observations():
    endpoint = 'https://frost.met.no/observations/v0.jsonld?sources=SN18700&referencetime=2022-01-01%2F2022-12-31&elements=best_estimate_sum(precipitation_amount%20P1M)'
    r = httpx.get(endpoint, auth=(client_id, ''))
    if r.status_code != 200:
        return pd.DataFrame.empty

    data = r.json()['data']
    rows = list()
    for i in range(len(data)):
        row = pd.DataFrame(data[i]['observations'])
        row['referenceTime'] = data[i]['referenceTime'].split('T')[0]
        row['sourceId'] = data[i]['sourceId']
        rows.append(row)
    df = pd.concat(rows)
    return df

def clean_transform_observations(dataframe):
    dataframe.dropna()
    dataframe[['year', 'month', 'day']] = dataframe['referenceTime'].str.split('-', expand=True)
    dataframe['precipitation'] = dataframe['value']
    columns = ['month', 'precipitation', 'unit']

    df = dataframe[columns].copy()
    df.set_index('month')
    return df
