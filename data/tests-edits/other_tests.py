import pandas as pd
trans = pd.read_csv("../transac2022cleaned.csv")
"""get list of all players traded for random button"""
# allt = trans[trans["typeof"] == "T "]
# IDS = allt["player"].tolist()
# player = sorted(IDS)
# new_id = []
# for id in player:
#     if " " in id:
#         pass
#     elif id == "PTBNL/Cash":
#         pass
#     elif id in new_id:
#         pass
#     else:
#         new_id.append(id)
# just_trades = pd.DataFrame(new_id)
# just_trades.to_csv("traded_players_2022.csv", index=False)

"""get player WAR"""
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
bwar_bat = pd.read_csv("../Retrosheet-BRef-Chadwick Untouched/bref/war_daily_bat.txt")
bwar_pitch = pd.read_csv("../Retrosheet-BRef-Chadwick Untouched/bref/war_daily_pitch.txt")
# # bwar_bat = bwar_bat[["name_common","mlb_ID","player_ID","year_ID","team_ID","WAR"]]
# # bwar_pitch = bwar_pitch[["name_common","mlb_ID","player_ID","year_ID","team_ID","WAR"]]
# # bwar_pitch.to_csv("test1.csv")
# # bwar_bat.to_csv("teams_combined_IDs.csv")
combined = [bwar_bat, bwar_pitch]
combined_WAR = pd.concat(combined)
# sorted = combined_WAR.sort_values(["name_common", "year_ID"], ascending=[True, True])
# sorted.to_csv("combined_WAR.csv", index=False)

combined_war = combined_WAR[["name_common","year_ID","salary"]]
sorted = combined_war.sort_values(["name_common", "year_ID"], ascending=[True, True])
sorted = sorted[["salary"]]

sorted.to_csv("salary1.csv")