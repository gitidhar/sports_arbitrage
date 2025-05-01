import pandas as pd
import ast         # safe string-to-Python converter

def print_arbs(csv_path: str = "prices.csv",
               bankroll: float = 100.0,
               market_key: str = "h2h") -> None:
   

    df = pd.read_csv(csv_path)

    for _, row in df.iterrows():
        home, away = row.get("home_team", ""), row.get("away_team", "")

        try:
            books = ast.literal_eval(row["bookmakers"])
        except (ValueError, SyntaxError):
            continue          # malformed JSON – skip this row

        best_price, best_book = {}, {}
        for bm in books:
            for mk in bm.get("markets", []):
                if mk.get("key") != market_key:
                    continue
                for out in mk.get("outcomes", []):
                    name, price = out["name"], float(out["price"])
                    if price > best_price.get(name, 0):
                        best_price[name] = price
                        best_book[name]  = bm["key"]

        if len(best_price) < 2:        
            continue

        implied_sum = sum(1 / p for p in best_price.values())
        edge = 1 - implied_sum
        if edge <= 0:
            print ("no arbitrage here")
            continue                  # no arbitrage here

        
        stakes  = {n: bankroll * (1 / price) / implied_sum
                   for n, price in best_price.items()}
        profits = {n: stakes[n] * (price - 1) - (bankroll - stakes[n])
                   for n, price in best_price.items()}
        profit  = round(next(iter(profits.values())), 2)   # same for every outcome

       
        print(f"\n  ARB FOUND    {home} vs {away}   edge={edge*100:.2f}%")
        for n in best_price:
            print(f"   {n:<18}  @ {best_price[n]:<6.2f} "
                  f"{best_book[n]:<12}  stake ${stakes[n]:.2f}")
        print(f"   Guaranteed profit (bankroll ${bankroll:.2f}) ➜  ${profit:.2f}")
        print("-" * 54)
