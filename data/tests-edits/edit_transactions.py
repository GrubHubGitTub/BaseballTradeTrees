import pandas as pd
# transactions = pd.read_csv("../2022/tran.csv")

# """filter only columns needed"""
# transactions = transactions[["primary_date", "transaction_ID", "player", "type", "from_team", "to_team", "info"]]
#
# """replace Nan with PTBNL/Cash"""
# transactions['player'] = transactions['player'].fillna("PTBNL/Cash")
#
# """add franchise tags to teams"""
# teams = pd.read_csv("./FranchiseList.csv")
# team_franchise_dict = teams.set_index("teamIDretro").to_dict()["franchID"]
# transactions["from_franchise"] = transactions["from_team"].map(team_franchise_dict)
# transactions["to_franchise"] = transactions["to_team"].map(team_franchise_dict)
# transactions = transactions[["primary_date", "transaction_ID", "player", "type", "from_franchise", "from_team",
#                               "to_franchise", "to_team", "info"]]
# transactions.to_csv("transactionsCleaned.csv", index=False)

"""get stats and add to transaction database"""
# players = pd.read_csv("./playerdata.csv")
# teams = pd.read_csv("../../data/2022/ChadwickTeams.csv")
# transactions = pd.read_csv("../tests-edits/transactionsCleaned.csv")
# transactions = transactions.astype(str)
# picks = pd.read_csv("../comp_picks_retroid.csv")
#
# pitching = pd.read_csv("../2022/Pitching.csv").fillna(0)
# batting = pd.read_csv("../2022/Batting.csv").fillna(0)
# pitching_bref = pd.read_csv("../2022/war_daily_pitch_filtered.csv").fillna(0)
# batting_bref = pd.read_csv("../2022/war_daily_bat_filtered.csv").fillna(0)
# all_star = pd.read_csv("../2022/AllstarFull.csv").fillna(0)
#
# team_franchise_dict = teams.set_index("teamID").to_dict()["franchID"]
# bref_franchise_dict = teams.set_index("teamIDBR").to_dict()["franchID"]
#
# pitching["franchID"] = pitching["teamID"].map(team_franchise_dict)
# batting["franchID"] = batting["teamID"].map(team_franchise_dict)
# all_star["franchID"] = all_star["teamID"].map(team_franchise_dict)
# pitching_bref["franchID"] = pitching_bref["team_ID"].map(bref_franchise_dict)
# batting_bref["franchID"] = batting_bref["team_ID"].map(bref_franchise_dict)
#
#
# def get_stats(retro_id, to_franch, from_franch, year, typeof):
#     year = int(year)
#
#     if typeof == "T ":
#         try:
#             bref_id = players[players.PLAYERID == retro_id]
#             bref_id = bref_id["key_bbref"].item()
#         except ValueError:
#             print(retro_id)
#         else:
#             # get batting stats
#             player_stats = batting[batting.playerID == bref_id]
#             team_stats = player_stats[player_stats.franchID == to_franch]
#             year_on_team_stats = team_stats[team_stats.yearID >= year]
#             batting_stats = (year_on_team_stats.to_dict('records'))
#
#             # get pitching stats
#             player_stats = pitching[pitching.playerID == bref_id]
#             team_stats = player_stats[player_stats.franchID == to_franch]
#             year_on_team_stats = team_stats[team_stats.yearID >= year]
#             pitching_stats = (year_on_team_stats.to_dict('records'))
#
#             # get pwar and salary
#             player_stats = pitching_bref[pitching_bref.player_ID == bref_id]
#             team_stats = player_stats[player_stats.franchID == to_franch]
#             year_on_team_stats = team_stats[team_stats.year_ID >= year]
#             pwar_stats = (year_on_team_stats.to_dict('records'))
#
#             # get bwar and salary
#             player_stats = batting_bref[batting_bref.player_ID == bref_id]
#             team_stats = player_stats[player_stats.franchID == to_franch]
#             year_on_team_stats = team_stats[team_stats.year_ID >= year]
#             bwar_stats = (year_on_team_stats.to_dict('records'))
#
#             #  get allstar appearances
#             player_stats = all_star[all_star.playerID == bref_id]
#             team_stats = player_stats[player_stats.franchID == to_franch]
#             year_on_team_stats = team_stats[team_stats.yearID >= year]
#             allstar = (year_on_team_stats.to_dict('records'))
#
#             if len(batting_stats) == 0 and len(pitching_stats) == 0:
#                 return None
#             return {"batting_stats": batting_stats, "pitching_stats": pitching_stats, "pwar_salary": pwar_stats,
#                     "bwar_salary": bwar_stats, "allstar": allstar}
#
#     elif typeof == "Fg":
#         player_comp_picks = picks[picks["fa_retroid"] == retro_id]
#         player_comp_picks_year = player_comp_picks[player_comp_picks["year"] == year + 1]
#         all_comp_picks = player_comp_picks_year["signed_retroid"].tolist()
#
#         if len(all_comp_picks) > 0:
#             batting_stats = []
#             pitching_stats = []
#             pwar_stats = []
#             bwar_stats = []
#             allstar = []
#             for player in all_comp_picks:
#                 try:
#                     bref_id = players[players.PLAYERID == player]
#                     bref_id = bref_id["key_bbref"].item()
#                 except ValueError:
#                     print(player)
#                 else:
#                     # get batting stats
#                     player_stats = batting[batting.playerID == bref_id]
#                     team_stats = player_stats[player_stats.franchID == from_franch]
#                     year_on_team_stats = team_stats[team_stats.yearID >= year]
#                     batting_stats += (year_on_team_stats.to_dict('records'))
#
#                     # get pitching stats
#                     player_stats = pitching[pitching.playerID == bref_id]
#                     team_stats = player_stats[player_stats.franchID == from_franch]
#                     year_on_team_stats = team_stats[team_stats.yearID >= year]
#                     pitching_stats += (year_on_team_stats.to_dict('records'))
#
#                     # get pwar and salary
#                     player_stats = pitching_bref[pitching_bref.player_ID == bref_id]
#                     team_stats = player_stats[player_stats.franchID == from_franch]
#                     year_on_team_stats = team_stats[team_stats.year_ID >= year]
#                     pwar_stats += (year_on_team_stats.to_dict('records'))
#
#                     # get bwar and salary
#                     player_stats = batting_bref[batting_bref.player_ID == bref_id]
#                     team_stats = player_stats[player_stats.franchID == from_franch]
#                     year_on_team_stats = team_stats[team_stats.year_ID >= year]
#                     bwar_stats += (year_on_team_stats.to_dict('records'))
#
#                     #  get allstar appearances
#                     player_stats = all_star[all_star.playerID == bref_id]
#                     team_stats = player_stats[player_stats.franchID == from_franch]
#                     year_on_team_stats = team_stats[team_stats.yearID >= year]
#                     allstar += (year_on_team_stats.to_dict('records'))
#
#             if len(batting_stats) == 0 and len(pitching_stats) == 0:
#                 return None
#             else:
#                 return {"batting_stats": batting_stats, "pitching_stats": pitching_stats, "pwar_salary": pwar_stats,
#                         "bwar_salary": bwar_stats, "allstar": allstar}
#
#
# transactions['stats'] = transactions.apply(lambda x: get_stats(x["player"], x["to_franchise"], x["from_franchise"],
#                                                     (x["primary_date"])[0:4], x["type"]), axis=1)
# #
# transactions.to_csv("transactions_stats_17082022.csv", index=False)

"""Remove nan, create json and csv"""
# transactions = pd.read_csv("transactions_stats_17082022.csv")
# transactions = transactions.fillna('')
# transactions.to_json("stats_transactions_17082022.json")
# transactions.to_csv("stats_transactions_17082022.csv", index=False)

"""add empty parent tree column"""
# transactions = pd.read_json("stats_transactions_17082022.json")
# transactions.insert(loc=10, column='parent_tree', value=['' for i in range(transactions.shape[0])])
# transactions.to_json("stats_transactions_25082022.json")
# transactions.to_csv("stats_transactions_25082022.csv", index=False)









