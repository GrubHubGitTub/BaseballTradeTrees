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

trans = pd.read_csv("sorted_transactions_final.csv")

non = trans["from-franchise"].fillna(0, inplace = True)
nont = trans["to-franchise"].fillna(0, inplace = True)

fromf = trans[(trans["typeof"] == "T ") & (trans["from-franchise"] == 0)]
tof = trans[(trans["typeof"] == "T ") & (trans["to-franchise"] == 0)]

fromf.to_csv("fromf.csv")
tof.to_csv("tof.csv")

