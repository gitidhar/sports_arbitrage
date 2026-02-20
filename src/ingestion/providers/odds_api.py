# src/sports_arbitrage/ingestion/providers/odds_api.py
import requests

SPORTS_URL = "https://api.the-odds-api.com/v4/sports"
ODDS_URL = "https://api.the-odds-api.com/v4/sports/{}/odds"

def fetch_active_sport_keys(api_key: str) -> list[str]:
    resp = requests.get(SPORTS_URL, params={"apiKey": api_key}, timeout=10)
    resp.raise_for_status()
    sports = resp.json()
    return [s["key"] for s in sports if s.get("active")]

def fetch_odds_for_sport(
    api_key: str,
    sport_key: str,
    regions: str,
    markets: str,
    odds_format: str,
    date_format: str,
) -> list[dict]:
    params = {
        "apiKey": api_key,
        "regions": regions,
        "markets": markets,
        "oddsFormat": odds_format,
        "dateFormat": date_format,
    }
    resp = requests.get(ODDS_URL.format(sport_key), params=params, timeout=10)
    if resp.status_code != 200:
        print("Odds API error:", resp.status_code, resp.text[:200])
        return []
    data = resp.json()
    return data if data else []

def fetch_all_live(api_key: str, regions: str, markets: str, odds_format: str, date_format: str) -> list[dict]:
    events: list[dict] = []
    for sk in fetch_active_sport_keys(api_key):
        events.extend(fetch_odds_for_sport(api_key, sk, regions, markets, odds_format, date_format))
    return events
