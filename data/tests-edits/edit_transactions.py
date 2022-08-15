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
#
# pitching = pd.read_csv("../2022/Pitching.csv")
# batting = pd.read_csv("../2022/Batting.csv")
# pitching_bref = pd.read_csv("../2022/war_daily_pitch_filtered.csv")
# batting_bref = pd.read_csv("../2022/war_daily_bat_filtered.csv")
# all_star = pd.read_csv("../2022/AllstarFull.csv")
# playoffs = pd.read_csv("../2022/SeriesPost.csv")
#
# team_franchise_dict = teams.set_index("teamID").to_dict()["franchID"]
# bref_franchise_dict = teams.set_index("teamIDBR").to_dict()["franchID"]
#
# pitching["franchID"] = pitching["teamID"].map(team_franchise_dict)
# batting["franchID"] = batting["teamID"].map(team_franchise_dict)
# all_star["franchID"] = all_star["teamID"].map(team_franchise_dict)
# playoffs["franchIDwinner"] = playoffs["teamIDwinner"].map(team_franchise_dict)
# playoffs["franchIDloser"] = playoffs["teamIDloser"].map(team_franchise_dict)
# pitching_bref["franchID"] = pitching_bref["team_ID"].map(bref_franchise_dict)
# batting_bref["franchID"] = batting_bref["team_ID"].map(bref_franchise_dict)
#
# def get_stats(retro_id, franch, year):
#     year = int(year)
#     try:
#         bref_id = players[players.PLAYERID == retro_id]
#         bref_id = bref_id["key_bbref"].item()
#     except ValueError:
#         print(retro_id)
#     else:
#         # get batting stats
#         player_stats = batting[batting.playerID == bref_id]
#         team_stats = player_stats[player_stats.franchID == franch]
#         year_on_team_stats = team_stats[team_stats.yearID >= year]
#         batting_stats = (year_on_team_stats.to_dict('records'))
#
#         # get pitching stats
#         player_stats = pitching[pitching.playerID == bref_id]
#         team_stats = player_stats[player_stats.franchID == franch]
#         year_on_team_stats = team_stats[team_stats.yearID >= year]
#         pitching_stats = (year_on_team_stats.to_dict('records'))
#
#         # get pwar and salary
#         player_stats = pitching_bref[pitching_bref.player_ID == bref_id]
#         team_stats = player_stats[player_stats.franchID == franch]
#         year_on_team_stats = team_stats[team_stats.year_ID >= year]
#         pwar_stats = (year_on_team_stats.to_dict('records'))
#
#         # get bwar and salary
#         player_stats = batting_bref[batting_bref.player_ID == bref_id]
#         team_stats = player_stats[player_stats.franchID == franch]
#         year_on_team_stats = team_stats[team_stats.year_ID >= year]
#         bwar_stats = (year_on_team_stats.to_dict('records'))
#
#         #  get allstar appearances
#         player_stats = all_star[all_star.playerID == bref_id]
#         team_stats = player_stats[player_stats.franchID == franch]
#         year_on_team_stats = team_stats[team_stats.yearID >= year]
#         allstar = (year_on_team_stats.to_dict('records'))
#
#         return [{"batting_stats": batting_stats}, {"pitching_stats": pitching_stats}, {"pwar_salary": pwar_stats},
#                 {"bwar_salary": bwar_stats}, {"allstar": allstar}]
#
#
# transactions = transactions.loc[transactions['type'] == "T "]
# transactions['stats'] = transactions.apply(lambda x: get_stats(x["player"], x["to_franchise"],
#                                                                                 (x["primary_date"])[0:4]), axis=1)
#
# transactions.to_csv("transactions_stats.csv",index=False)

"""merge trade stats database with all transactions"""
# transactions = pd.read_csv("../tests-edits/transactionsCleaned.csv")
# with_stats = pd.read_csv("../tests-edits/transactions_stats.csv")
#
# combined_transactions = pd.merge(transactions, with_stats[["primary_date","transaction_ID","player","stats"]],
#                          on=["primary_date","transaction_ID","player"], how="left")
#
# combined_transactions.to_csv("transactions_stats_2022.csv", index=False)

"""get comp pick stats and merge"""
picks = pd.read_csv("../comp_picks_retroid.csv")
picks_dict = picks.set_index("year").to_dict()["fa_retroid"]
print(picks_dict)


# player_comp_picks = picks[picks["fa_retroid"] == player_id]
# player_comp_picks_year = player_comp_picks[player_comp_picks["year"] == year]

"""remove spaces in franchise/team columns"""
# trans["from-team"] = trans["from-team"].str.replace(' ', '')
# trans["to-team"] = trans["to-team"].str.replace(' ', '')

"""Replace Nan values in franchise with the data in team columns"""
# trans["from-franchise"].fillna(trans["from-team"], inplace=True)
# trans["to-franchise"].fillna(trans["to-team"], inplace=True)
# trans.to_csv("transac2022cleaned.csv", index=False)






