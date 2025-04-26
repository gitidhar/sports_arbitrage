import os, time, requests, pandas as pd
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ODDS_API_KEY")
BASE = "https://api.the-odds-api.com/v4/sports/soccer_epl/odds"

PARAMS = {
    "apiKey": API_KEY,
    "regions": "uk",
    "markets": "h2h",
    "oddsFormat": "decimal",
    "dateFormat": "iso"
}

# while True:
r = requests.get(BASE, params=PARAMS, timeout=10)
data = r.json()

if isinstance(data, dict) and data.get("error_code"):
    raise RuntimeError(f"{data['error_code']}: {data['message']}")

pd.json_normalize(data).to_csv("prices.csv", mode="a", index=False)
time.sleep(30)
