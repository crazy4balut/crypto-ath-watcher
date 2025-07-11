from exchange_client import fetch_balances, fetch_ticker
from csv_parser import parse_csv

def unify_data(csv_path):
    exchange_data = fetch_balances()
    csv_data = parse_csv(csv_path)
    combined = {
        "exchange": exchange_data,
        "mobile": csv_data
    }
    return combined
