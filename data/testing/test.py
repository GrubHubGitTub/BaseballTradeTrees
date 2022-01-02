import pandas as pd
trans = pd.read_csv("../transac2021cleaned.csv")
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
# from pybaseball import playerid_reverse_lookup, pitching_stats, batting_stats, bwar_pitch, bwar_bat
# import pandas as pd
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)
#
# joe = playerid_reverse_lookup(["dimaj101"], key_type='retro')
# print(joe)
# id = joe.key_bbref.item()
# team_start = "2012-07-01"
# team_end = "2017-07-01"
# kershaw_stats = pitching_stats('2017-06-01', '2017-07-01', 477132)
#
# data = bwar_bat()
# data.to_csv("data.csv")
#
# all = data.sort_values(by=['year_ID'])
# print(all)
# joed = data[data["player_ID"] == id]
#
# print(joed)