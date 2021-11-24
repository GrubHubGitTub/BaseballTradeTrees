# import pandas as pd

# teams = pd.read_csv("teams.csv")
#
# team_franchise_dict = teams.set_index("TeamID").to_dict()["Franchise"]
#
# trans = pd.read_csv("1_transactions_no_nan.csv")
#
# trans["from-franchise"] = trans["from-team"].map(team_franchise_dict)
# trans["to-franchise"] = trans["to-team"].map(team_franchise_dict)
#
# trans.to_csv("trans_with_franchise.csv", index=False)
import pandas as pd

trans = pd.read_csv("../sorted_transactions_final.csv")

allT = trans[trans["typeof"] == "T "]

IDS = allT["player"].tolist()

new_id = []
for id in IDS:
    if " " in id:
        pass
    elif id in new_id:
        pass
    else:
        new_id.append(id)


just_trades = pd.DataFrame(new_id)
just_trades.to_csv("random_ids.csv", index=False)
