import cryptowatch as cw
import requests
from datetime import datetime


# TODO: This is just placeholder code for testing purposes for now.
params = {
    'after': '1637533800',
    'periods': [180],
}
resp = requests.get('https://api.cryptowat.ch/markets/coinbase-pro/ethusd/ohlc', params=params)

if resp.ok:
    doc = resp.json()
    result = doc['result']['180']
    print(result)
else:
    print("failed?")