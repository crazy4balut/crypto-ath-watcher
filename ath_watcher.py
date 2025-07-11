from csv_parser import parse_crypto_app_csv

def check_ath(filepath):
    df = parse_crypto_app_csv(filepath)
    symbols = df['symbol'].unique()
    aths = {}

    for symbol in symbols:
        coin_df = df[df['symbol'] == symbol]
        high = coin_df['amount'].max()
        aths[symbol] = high

    return aths
