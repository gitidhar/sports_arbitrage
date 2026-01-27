import os, time, requests, pandas as pd, pathlib
from dotenv import load_dotenv
from arb_engine import scan_arbs

load_dotenv()
API_KEY = os.getenv("ODDS_API_KEY")
CSV_PATH = pathlib.Path("prices.csv")

BASE = "https://api.the-odds-api.com/v4/sports/{}/odds"
PARAMS = {
    "apiKey": API_KEY,
    "regions": "us,us2",          # both U-S bookmaker clusters
    "markets": "h2h",
    "oddsFormat": "decimal",
    "dateFormat": "iso",
}

def fetch_all_live():
    sport_keys = [
        s["key"] for s in requests.get(
            "https://api.the-odds-api.com/v4/sports",
            params={"apiKey": API_KEY}, timeout=10
        ).json() if s["active"]          # filter off-season sports
    ]

    events = []
    for sk in sport_keys:
        resp = requests.get(BASE.format(sk), params=PARAMS, timeout=10)
        if resp.status_code == 200 and resp.json():
            events.extend(resp.json())
        # time.sleep(1.1)   # stay under free-tier rate limit
    return events

if __name__ == "__main__":
    data = fetch_all_live()
    if data:
        header_needed = not CSV_PATH.exists() or CSV_PATH.stat().st_size == 0
        pd.json_normalize(data).to_csv(CSV_PATH, mode="a", index=False, header=header_needed)
        scan_arbs(CSV_PATH)
    else:
        print("No live odds across active sports; skipping arb scan.")
