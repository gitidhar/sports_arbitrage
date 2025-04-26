

import pandas as pd
snap = pd.read_csv("prices.csv").tail(1)
best = snap.groupby('outcome')['price'].max()
edge = 1 - (1/best).sum()
if edge > 0:
    print(f"ARB! edge={edge:.3%}")
