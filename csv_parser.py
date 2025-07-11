import pandas as pd

def parse_csv(filepath):
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['Timestamp'])  # adapt column names
    df['symbol'] = df['Currency']  # map to ATH logic
    return df.to_dict(orient='records')
