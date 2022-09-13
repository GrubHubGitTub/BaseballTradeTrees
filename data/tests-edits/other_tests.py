import pandas as pd
import json

trans = pd.read_csv("stats_transactions_06092022.csv")
"""get dict of all players traded for data generation """
allt = trans[(trans["type"] == "T ")]
allt = allt[["primary_date", "player", "transaction_ID", "type", "from_franchise"]]
allt = allt[allt.player != "PTBNL/Cash"]
allt = allt.sort_values(by=['primary_date'], ascending=True)
names = allt.to_dict('records')

with open("PlayersToGenerate.json", "w") as file:
    json.dump(names, file, indent=4)

