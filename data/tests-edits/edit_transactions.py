import pandas as pd
# transactions = pd.read_csv("../2022/tran.csv")

# """filter bref files"""
# pitching_bref = pd.read_csv("../../data/2022/war_daily_pitch.csv")
# batting_bref = pd.read_csv("../../data/2022/war_daily_bat.csv")
#
# pitching_bref = pitching_bref[["name_common","age","mlb_ID","player_ID","year_ID","team_ID","stint_ID","lg_ID","WAR","salary"]]
# batting_bref = batting_bref[["name_common","age","mlb_ID","player_ID","year_ID","team_ID","stint_ID","lg_ID","WAR","salary"]]
# pitching_bref.to_csv("war_daily_pitch_filtered.csv", index=False)
# batting_bref.to_csv("war_daily_bat_filtered.csv", index=False)

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
players = pd.read_csv("./playerdata.csv")
teams = pd.read_csv("../../data/2022/ChadwickTeams.csv")
transactions = pd.read_csv("../tests-edits/transactionsCleaned.csv")
transactions = transactions.astype(str)
picks = pd.read_csv("../comp_picks_retroid.csv")

pitching = pd.read_csv("../2022/Pitching.csv").fillna(0)
batting = pd.read_csv("../2022/Batting.csv").fillna(0)
pitching_bref = pd.read_csv("../2022/war_daily_pitch_filtered.csv").fillna(0)
batting_bref = pd.read_csv("../2022/war_daily_bat_filtered.csv").fillna(0)
all_star = pd.read_csv("../2022/AllstarFull.csv").fillna(0)

team_franchise_dict = teams.set_index("teamID").to_dict()["franchID"]
bref_franchise_dict = teams.set_index("teamIDBR").to_dict()["franchID"]

pitching["franchID"] = pitching["teamID"].map(team_franchise_dict)
batting["franchID"] = batting["teamID"].map(team_franchise_dict)
all_star["franchID"] = all_star["teamID"].map(team_franchise_dict)
pitching_bref["franchID"] = pitching_bref["team_ID"].map(bref_franchise_dict)
batting_bref["franchID"] = batting_bref["team_ID"].map(bref_franchise_dict)


def get_stats(retro_id, to_franch, from_franch, year, typeof):
    year = int(year)

    if typeof == "T ":
        try:
            bref_id = players[players.PLAYERID == retro_id]
            bref_id = bref_id["key_bbref"].item()
        except ValueError:
            print(retro_id)
        else:
            # get batting stats
            player_stats = batting[batting.playerID == bref_id]
            team_stats = player_stats[player_stats.franchID == to_franch]
            year_on_team_bstats = team_stats[team_stats.yearID >= year]
            if not year_on_team_bstats.empty:
                # get bwar and salary and merge
                player_stats = batting_bref[batting_bref.player_ID == bref_id]
                team_stats = player_stats[player_stats.franchID == to_franch]
                year_on_team_bwar = team_stats[team_stats.year_ID >= year]
                batting_stats = pd.merge(year_on_team_bstats, year_on_team_bwar, left_on=["playerID", "yearID"],
                                          right_on=["player_ID", "year_ID"])
                batting_stats["Name"] = batting_stats["name_common"]
                batting_stats["Year"] = batting_stats["yearID"]
                batting_stats = batting_stats[['Name', 'age', 'Year', 'teamID', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR',
                                               'RBI', 'SB', 'CS', 'BB', 'SO', 'IBB', 'HBP', 'SH', 'SF', 'GIDP',
                                               'salary', 'WAR']]
                batting_stats_list = (batting_stats.to_dict('records'))
            else:
                batting_stats_list = []

            # get pitching stats
            player_stats = pitching[pitching.playerID == bref_id]
            team_stats = player_stats[player_stats.franchID == to_franch]
            year_on_team_pstats = team_stats[team_stats.yearID >= year]
            if not year_on_team_pstats.empty:
                # get pwar and salary and merge
                player_stats = pitching_bref[pitching_bref.player_ID == bref_id]
                team_stats = player_stats[player_stats.franchID == to_franch]
                year_on_team_pwar = team_stats[team_stats.year_ID >= year]
                pitching_stats = pd.merge(year_on_team_pstats, year_on_team_pwar, left_on=["playerID", "yearID"],
                                         right_on=["player_ID", "year_ID"])
                pitching_stats["Name"] = pitching_stats["name_common"]
                pitching_stats["Year"] = pitching_stats["yearID"]

                pitching_stats = pitching_stats[['Name', 'age', 'Year', 'teamID', 'W', 'L', 'G', 'GS', 'CG', 'SHO',
                                                 'SV', 'IPouts', 'H', 'ER', 'HR', 'BB', 'SO', 'BAOpp', 'ERA', 'IBB',
                                                 'WP', 'HBP', 'BK', 'BFP', 'GF', 'R', 'SH', 'SF', 'GIDP',
                                                 'salary', 'WAR']]
                pitching_stats_list = (pitching_stats.to_dict('records'))
            else:
                pitching_stats_list = []

            #  get allstar appearances
            player_stats = all_star[all_star.playerID == bref_id]
            team_stats = player_stats[player_stats.franchID == to_franch]
            all_star_appearances = team_stats[team_stats.yearID >= year]
            if not all_star_appearances.empty:
                years = all_star_appearances["yearID"].tolist()
                if len(batting_stats_list) > 0:
                    for line in batting_stats_list:
                        if line["Year"] in years:
                            line["All Star"] = "Yes"
                        else:
                            line["All Star"] = "No"
                if len(pitching_stats_list) > 0:
                    for line in pitching_stats_list:
                        if line["Year"] in years:
                            line["All Star"] = "Yes"
                        else:
                            line["All Star"] = "No"

            else:
                for line in batting_stats_list:
                    line["All Star"] = "No"
                for line in pitching_stats_list:
                    line["All Star"] = "No"

            if len(batting_stats_list) == 0 and len(pitching_stats_list) == 0:
                return None
            return {"batting_stats": batting_stats_list, "pitching_stats": pitching_stats_list}

    elif typeof == "Fg":
        player_comp_picks = picks[picks["fa_retroid"] == retro_id]
        player_comp_picks_year = player_comp_picks[player_comp_picks["year"] == year + 1]
        all_comp_picks = player_comp_picks_year["signed_retroid"].tolist()

        if len(all_comp_picks) > 0:
            batting_stats_list = []
            pitching_stats_list = []
            for player in all_comp_picks:
                try:
                    bref_id = players[players.PLAYERID == player]
                    bref_id = bref_id["key_bbref"].item()
                except ValueError:
                    print(player)
                else:
                    # get batting stats
                    player_stats = batting[batting.playerID == bref_id]
                    team_stats = player_stats[player_stats.franchID == from_franch]
                    year_on_team_bstats = team_stats[team_stats.yearID >= year]
                    if not year_on_team_bstats.empty:
                        # get bwar and salary and merge
                        player_stats = batting_bref[batting_bref.player_ID == bref_id]
                        team_stats = player_stats[player_stats.franchID == from_franch]
                        year_on_team_bwar = team_stats[team_stats.year_ID >= year]
                        batting_stats = pd.merge(year_on_team_bstats, year_on_team_bwar, left_on=["playerID", "yearID"],
                                                 right_on=["player_ID", "year_ID"])
                        batting_stats["Name"] = batting_stats["name_common"]
                        batting_stats["Year"] = batting_stats["yearID"]
                        batting_stats = batting_stats[
                            ['Name', 'age', 'Year', 'teamID', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR',
                             'RBI', 'SB', 'CS', 'BB', 'SO', 'IBB', 'HBP', 'SH', 'SF', 'GIDP',
                             'salary', 'WAR']]
                        bat_stats = (batting_stats.to_dict('records'))
                    else:
                        bat_stats = []

                    # get pitching stats
                    player_stats = pitching[pitching.playerID == bref_id]
                    team_stats = player_stats[player_stats.franchID == from_franch]
                    year_on_team_pstats = team_stats[team_stats.yearID >= year]
                    if not year_on_team_pstats.empty:
                        # get pwar and salary and merge
                        player_stats = pitching_bref[pitching_bref.player_ID == bref_id]
                        team_stats = player_stats[player_stats.franchID == from_franch]
                        year_on_team_pwar = team_stats[team_stats.year_ID >= year]
                        pitching_stats = pd.merge(year_on_team_pstats, year_on_team_pwar,
                                                  left_on=["playerID", "yearID"],
                                                  right_on=["player_ID", "year_ID"])
                        pitching_stats["Name"] = pitching_stats["name_common"]
                        pitching_stats["Year"] = pitching_stats["yearID"]

                        pitching_stats = pitching_stats[
                            ['Name', 'age', 'Year', 'teamID', 'W', 'L', 'G', 'GS', 'CG', 'SHO',
                             'SV', 'IPouts', 'H', 'ER', 'HR', 'BB', 'SO', 'BAOpp', 'ERA', 'IBB',
                             'WP', 'HBP', 'BK', 'BFP', 'GF', 'R', 'SH', 'SF', 'GIDP',
                             'salary', 'WAR']]
                        pitch_stats = (pitching_stats.to_dict('records'))
                    else:
                        pitch_stats = []

                    #  get allstar appearances
                    player_stats = all_star[all_star.playerID == bref_id]
                    team_stats = player_stats[player_stats.franchID == to_franch]
                    all_star_appearances = team_stats[team_stats.yearID >= year]
                    if not all_star_appearances.empty:
                        years = all_star_appearances["yearID"].tolist()
                        if len(bat_stats) > 0:
                            for line in bat_stats:
                                if line["Year"] in years:
                                    line["All Star"] = "Yes"
                                else:
                                    line["All Star"] = "No"
                        if len(pitch_stats) > 0:
                            for line in pitch_stats:
                                if line["Year"] in years:
                                    line["All Star"] = "Yes"
                                else:
                                    line["All Star"] = "No"
                    else:
                        for line in bat_stats:
                            line["All Star"] = "No"
                        for line in pitch_stats:
                            line["All Star"] = "No"

                    if len(bat_stats) > 0:
                        batting_stats_list += bat_stats
                    if len(pitch_stats) > 0:
                        pitching_stats_list += pitch_stats

            if len(batting_stats_list) == 0 and len(pitching_stats_list) == 0:
                return None
            return {"batting_stats": batting_stats_list, "pitching_stats": pitching_stats_list}


transactions['stats'] = transactions.apply(lambda x: get_stats(x["player"], x["to_franchise"], x["from_franchise"],
                                                    (x["primary_date"])[0:4], x["type"]), axis=1)

transactions = transactions.fillna('')
transactions.to_json("stats_transactions_06092022.json")
transactions.to_csv("stats_transactions_06092022.csv", index=False)










