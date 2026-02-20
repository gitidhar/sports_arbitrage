# src/sports_arbitrage/app/services.py
from sparb.config.settings import Settings
from sparb.ingestion.providers.odds_api import fetch_all_live
from sparb.domain.arb import analyze_for_arb
from sparb.infra.logger import initialize_logger, log_opportunities

def run_arb_scan(settings: Settings, snapshot: bool = True) -> int:
    events = fetch_all_live(
        api_key=settings.odds_api_key,
        regions=settings.regions,
        markets=settings.markets,
        odds_format=settings.odds_format,
        date_format=settings.date_format,
    )

    if not events:
        return 0

    opps = analyze_for_arb(
        events=events,
        bankroll=settings.bankroll,
        market_key=settings.market_key,
    )

    logger = initialize_logger(settings.arbs_log_path)
    log_opportunities(logger, opps)
    return len(opps)
