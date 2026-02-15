from .models import ArbitrageOpportunity, OpportunityLeg

def analyze_for_arb(events: list[dict], bankroll: float, mrkt_key: str="h2h") -> list[ArbitrageOpportunity]:

    opportunities: list[ArbitrageOpportunity] = []

    for event in events:
        home = event.get("home_team", "")
        away = event.get("away_team", "")
        books = event.get("bookmakers") or []
        