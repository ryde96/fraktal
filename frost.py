import httpx
import pandas as pd

client_id = "553f1144-551b-450c-8abe-0f696239188d"
client_secret = ""

def get_observations(parameters):
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
    columns = ['sourceId', 'referenceTime', 'elementId', 'value', 'unit']
    df = dataframe[columns].copy()
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])
    print(df)