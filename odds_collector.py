# odds_collector.py – pulls best prices every 30 s


import os, time, requests, pandas as pd


API_KEY = os.getenv("ODDS_API_KEY")
URL = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds?markets=h2h&apiKey=" + API_KEY
while True:
    df = pd.json_normalize(requests.get(URL).json())
    df.to_csv("prices.csv", mode="a")
    time.sleep(30)
