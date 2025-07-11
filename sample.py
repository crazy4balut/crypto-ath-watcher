if __name__ == "__main__":
    filepath = "path/to/your_export.csv"
    ath_values = check_ath(filepath)
    for symbol, ath in ath_values.items():
        print(f"{symbol}: ATH amount in CSV = {ath}")
