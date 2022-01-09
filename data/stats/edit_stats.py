import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
"""Get combined WAR stats"""
# bwar_bat = pd.read_csv("war_daily_bat.txt")
# bwar_pitch = pd.read_csv("war_daily_pitch.txt")
# bwar_bat = bwar_bat[["name_common","mlb_ID","player_ID","year_ID","team_ID", "PA", "G", "WAR"]]
# bwar_pitch = bwar_pitch[["name_common","mlb_ID","player_ID","year_ID","team_ID","G","IPouts","WAR"]]
# bwar_pitch.to_csv("test1.csv")
# bwar_bat.to_csv("teams_combined_IDs.csv")
# combined = [bwar_bat, bwar_pitch]
# combined_WAR = pd.concat(combined)
# combined_WAR= combined_WAR[["name_common","mlb_ID","player_ID","year_ID","team_ID", "G", "PA", "IPouts", "WAR"]]
# sorted = combined_WAR.sort_values(["name_common", "year_ID"], ascending=[True, True])
# sorted.to_csv("combined_WAR.csv", index=False)

"""combine Bref and retrosheet IDS"""
# all = pd.read_csv("People.csv")
# all = all[["retroID","bbrefID"]]
# stats = pd.read_csv("combined_WAR.csv")
# id_dict = all.set_index("bbrefID").to_dict()["retroID"]
# stats["retroID"] = stats["player_ID"].map(id_dict)
# stats.to_csv("test.csv", index= False)
#
# stats = pd.read_csv("test.csv")
# stats = stats[["name_common","retroID","player_ID","year_ID","team_ID", "G", "PA", "IPouts", "WAR"]]
# stats.to_csv("Stats_Combined_IDs.csv", index=False)

"""replace Nan values in WAR to 0"""
# stats = pd.read_csv("../tests-edits/Old Data/Stats_Combined_IDs.csv")
# stats['WAR'] = stats['WAR'].fillna(0)
# stats.to_csv("Stats_noWARnan.csv", index=False)

"""replace Nan Values in other stat columns"""
# stats = pd.read_csv("../stats/StatsCombinedIDsFranchises.csv")
# stats['G'] = stats['G'].fillna(0)
# stats['PA'] = stats['PA'].fillna(0)
# stats['IPouts'] = stats['IPouts'].fillna(0)
# stats.to_csv("StatsAllIDsNoStatNan.csv", index=False)


"""add retroIDs to stat file"""
# teams = pd.read_csv("../Retrosheet-BRef-Chadwick Untouched/chadwick/Teams.csv")
# teams = teams[["teamID", "teamIDBR", "teamIDretro", "franchID",]]
# nodupes = teams.drop_duplicates()
# nodupes.to_csv("teams_combined_IDs.csv", index=False)
# teams = pd.read_csv("teams_combined_IDs.csv")
# team_match_dict = teams.set_index("teamIDBR").to_dict()["teamIDretro"]
# war = pd.read_csv("Stats_noWARnan.csv")
# war["teamIDretro"] = war["team_ID"].map(team_match_dict)
# # trans = trans[["primary_date", "transaction_id", "player", "typeof", "from-franchise", "from-team", "to-franchise", "to-team", "info"]]
# war.to_csv("StatsCombinedIDs", index=False)

"""add franchise tags from teams.csv"""
# teams = pd.read_csv("../teams.csv")
# franchise_match_dict = teams.set_index("TeamID").to_dict()["Franchise"]
# war = pd.read_csv("StatsCombinedIDs")
# war["Franchise"] = war["teamIDretro"].map(franchise_match_dict)
# war = war[["name_common","retroID","brefID","year_ID","team_ID","teamIDretro","Franchise","G","PA","IPouts","WAR",]]
# war.to_csv("StatsCombinedIDsFranchises.csv", index=False)

"""combine with salary"""
all = pd.read_csv("StatsAllIDsNoStatNan.csv")
salary = pd.read_csv("salary1.csv")

test = pd.concat([all, salary], axis=1)
test["salary"] = test["salary"].fillna(0)
test = test[["name_common","retroID","brefID","year_ID","team_ID","teamIDretro","Franchise","G","PA","IPouts","WAR","salary"]]

test.to_csv("StatsSalaryCombinedIDs.csv", index=False)

test.to_csv("PlayerStats.csv", index=False)