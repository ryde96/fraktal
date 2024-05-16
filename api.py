def json_to_dataframe(json):
    df = pd.json_normalize(json)
    return df
