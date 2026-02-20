# src/sports_arbitrage/cli/main.py
from sparb.config.settings import load_settings
from sparb.app.arbscan import run_arb_scan

def main() -> None:
    settings = load_settings()
    count = run_arb_scan(settings, snapshot=True)
    if count == 0:
        print("No arbs found (or no live odds).")
    else:
        print(f"Logged {count} arbs to {settings.arbs_log_path}")

if __name__ == "__main__":
    main()
