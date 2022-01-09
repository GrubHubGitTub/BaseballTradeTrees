import pandas as pd
trans = pd.read_csv()
"""filter only columns needed"""
# transactions = trans[["primary_date", "transaction_id", "player", "typeof", "from-team", "to-team", "info"]]
# transactions.to_csv("trans1-1filter.csv", index=False)

"""replace Nan with PTBNL/Cash"""
# trans['player'] = trans['player'].fillna("PTBNL/Cash")
# trans.to_csv("trans1-1filterPTBNL.csv", index=False)

"""add franchise tags to teams"""
# teams = pd.read_csv("../teams.csv")
# team_franchise_dict = teams.set_index("TeamID").to_dict()["Franchise"]
# trans["from-franchise"] = trans["from-team"].map(team_franchise_dict)
# trans["to-franchise"] = trans["to-team"].map(team_franchise_dict)
# trans = trans[["primary_date", "transaction_id", "player", "typeof", "from-franchise", "from-team", "to-franchise", "to-team", "info"]]
# trans.to_csv("trans1-1_franchise.csv", index=False)

"""remove spaces in franchise/team columns"""
# trans["from-team"] = trans["from-team"].str.replace(' ', '')
# trans["to-team"] = trans["to-team"].str.replace(' ', '')

"""Replace Nan values in franchise with the data in team columns"""
# trans["from-franchise"].fillna(trans["from-team"], inplace=True)
# trans["to-franchise"].fillna(trans["to-team"], inplace=True)
# trans.to_csv("transac2022cleaned.csv", index=False)

# """sort trans by name and date and then check for F/Fg or R/Fg """ THIS WAS PUT INTO THE SEARCH FUNCTION
# sorted = trans.sort_values(["player", "primary_date"], ascending=[True, True])
# sorted["typeof_prev_row"] = sorted["typeof"].shift(1)
# sorted["from-franchise_prev_row"] = sorted["from-franchise"].shift(1)
# sorted["player_prev_row"] = sorted["player"].shift(1)
# all_r = sorted[(sorted["typeof"] == "F ") & (sorted["typeof_prev_row"] == "R ") & (sorted["from-franchise_prev_row"] == sorted["to-franchise"]) & (sorted["player_prev_row"] == sorted["player"])]
# ind = all_r.index.values.tolist()
# new_index = []
# for n in ind:
#     new1 = n-1
#     new2 = n
#     new_index.append(new1)
#     new_index.append(new2)
# print(new_index)
# sorted = trans.sort_index()
# ## sorted.to_csv("sorted.csv", index=False)
# deleted = sorted.drop(sorted.index[new_index])
# deleted.to_csv("transac2022cleaned.csv", index=False)




