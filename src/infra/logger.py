import logging
from src.domain.models import ArbitrageOpportunity
from pathlib import Path

def initialize_logger(log_path: str) -> logging.Logger:
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("arbs")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(log_path)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)
    return logger

def log_opportunities(logger: logging.Logger, opps: list[ArbitrageOpportunity]) -> None:
    for opp in opps:
        logger.info("")
        logger.info(f"\n  ARB FOUND    {opp.home_team} vs {opp.away_team}   edge={opp.edge*100:.2f}%")
        for leg in opp.legs:
            logger.info(
                f"   {leg.outcome_name:<18}  @ {leg.price:<6.2f} "
                f"{leg.bookmaker_key:<12}  stake ${leg.stake:.2f}"
            )
        logger.info(f"   Guaranteed profit (bankroll ${opp.bankroll:.2f}) ➜  ${opp.guaranteed_profit:.2f}")

