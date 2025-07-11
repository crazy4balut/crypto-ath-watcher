import requests

def get_token_logo(contract_address, chain="eth"):
    url = f"https://deep-index.moralis.io/api/v2/erc20/{contract_address}/metadata?chain={chain}"
    headers = {"X-API-Key": eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjkwZDU4ODllLThjYWMtNDhhOS1hYTEzLTYxZWU4ZjYzMDIzYSIsIm9yZ0lkIjoiNDU4MDMzIiwidXNlcklkIjoiNDcxMjM5IiwidHlwZUlkIjoiZTg4OTEyMWItZDUyMC00NDY0LTliYjktM2JjY2FlZDkyYmZhIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NTE4OTczOTYsImV4cCI6NDkwNzY1NzM5Nn0.nKkhF7kYXOvuomwMOvF0VBLvOyND4DHAWVyduMG8Pv8}
    response = requests.get(url, headers=headers)
    return response.json().get("logo")
