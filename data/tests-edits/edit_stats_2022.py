import pandas as pd

"""filter bref files"""
pitching_bref = pd.read_csv("../../data/2022/war_daily_pitch.csv")
batting_bref = pd.read_csv("../../data/2022/war_daily_bat.csv")

pitching_bref = pitching_bref[["name_common","age","mlb_ID","player_ID","year_ID","team_ID","stint_ID","lg_ID","WAR","salary"]]
batting_bref = batting_bref[["name_common","age","mlb_ID","player_ID","year_ID","team_ID","stint_ID","lg_ID","WAR","salary"]]
pitching_bref.to_csv("war_daily_pitch_filtered.csv", index=False)
batting_bref.to_csv("war_daily_bat_filtered.csv", index=False)