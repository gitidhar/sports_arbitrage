from .models import ArbitrageOpportunity, OpportunityLeg

def size_bank_roll(prices: dict[str, float], implied_sum, bankroll: float):
    stakes = {}
    for n, price in prices.items():
        stakes[n] = bankroll * (1/price) / implied_sum
    return stakes


def analyze_for_arb(events: list[dict], bankroll: float, market_key: str="h2h") -> list[ArbitrageOpportunity]:
    opportunities: list[ArbitrageOpportunity] = []
    for event in events:
        home = event.get("home_team", "")
        away = event.get("away_team", "")
        books = event.get("bookmakers") or []

        best_price : dict[str, float] = {}
        best_book : dict[str, str] = {}

        for bm in books:
            for mk in bm.get("markets", []):
                if mk.get("key") != market_key: continue
                for outcome in mk.get("outcomes", []):
                    name = outcome["name"]
                    price = float(outcome["price"])
                    if price > best_price.get(name, 0.0):
                        best_price[name] = price
                        best_book[name] = bm.get("key", "")
        
        if len(best_price) < 2:
            continue
        implied_sum = sum(1 / p for p in best_price.values())
        edge = 1 - implied_sum
        if edge <= 0:
            continue # no arbitrage 
        stakes = size_bank_roll(best_price, implied_sum, bankroll)
        profits = {
            n: stakes[n] * (price - 1) - (bankroll - stakes[n])
            for n, price in best_price.items()
        }
        guaranteed_profit = round(min(profits.values()), 2) # technically all stake outcomes are equal
        legs : list[OpportunityLeg] = []
        for n in best_price:
            legs.append(OpportunityLeg(
                outcome_name=n,
                price=best_price[n],
                bookmaker_key=best_book[n],
                stake=round(stakes[n], 2),
            ))
        opportunities.append(
            ArbitrageOpportunity(
                home_team=home,
                away_team=away,
                edge=edge,
                bankroll=bankroll,
                guaranteed_profit=guaranteed_profit,
                legs=legs,
            )
        )
    return opportunities
