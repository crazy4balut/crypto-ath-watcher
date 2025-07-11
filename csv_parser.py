import pandas as pd

def parse_crypto_app_csv(filepath):
    df = pd.read_csv(filepath)

    # Normalize column names (update if different in your export)
    df.rename(columns={
        'Timestamp': 'timestamp',
        'Currency': 'symbol',
        'Amount': 'amount',
        'Transaction Type': 'tx_type',
        'To': 'destination',
        'From': 'source'
    }, inplace=True)

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(by='timestamp', inplace=True)

    return df
