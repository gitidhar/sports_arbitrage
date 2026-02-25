# src/sports_arbitrage/config/settings.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass(frozen=True)
class Settings:
    odds_api_key: str
    regions: str = "us,us2"
    markets: str = "h2h"
    odds_format: str = "decimal"
    date_format: str = "iso"
    bankroll: float = 100.0
    market_key: str = "h2h"
    snapshot_csv_path: str = "data/prices.csv"
    arbs_log_path: str = "src/sparb/outputs/arbs.txt"

def load_settings() -> Settings:
    load_dotenv()
    key = os.getenv("ODDS_API_KEY")
    if not key:
        raise RuntimeError("Missing ODDS_API_KEY in environment or .env")
    return Settings(odds_api_key=key)