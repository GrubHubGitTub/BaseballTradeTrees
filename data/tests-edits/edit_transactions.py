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
# trans  = trans[["primary_date", "transaction_id", "player", "typeof", "from-franchise", "from-team", "to-franchise", "to-team", "info"]]
# trans.to_csv("trans1-1_franchise.csv", index=False)

"""remove spaces in franchise/team columns"""
# trans["from-team"] = trans["from-team"].str.replace(' ', '')
# trans["to-team"] = trans["to-team"].str.replace(' ', '')

"""Replace Nan values in franchise with the data in team columns"""
# trans["from-franchise"].fillna(trans["from-team"], inplace=True)
# trans["to-franchise"].fillna(trans["to-team"], inplace=True)
# trans.to_csv("transac2022cleaned.csv", index=False)






