class OpportunityLeg:
    outcome_name: str
    price: float
    bookmaker_key: str
    stake: float

class ArbitrageOpportunity:
    home_team: str
    away_team: str
    edge: float
    bankroll: float
    guaranteed_profit: float
    legs: list[OpportunityLeg]
