import pandas as pd

"""filter player bio file"""
players = pd.read_csv("../Retrosheet-BRef-Chadwick Untouched/retro/BIOFILE.csv")
players["NAME"] = players["NICKNAME"] + " " + players["LAST"]
players = players[["PLAYERID", "NAME", "PLAY_DEBUT", "PLAY_LASTGAME", "HOF"]]
players.to_csv("PlayerSearch.csv", index=False)

"""Create Json for Next"""
import json, csv

with open('PlayerSearch.csv') as f:
    dict = [{k: v for k, v in row.items()}
            for row in csv.DictReader(f, skipinitialspace=True)]
    with open('../../mlb-trade-trees-next/json/PlayerSearch.json', 'w') as convert_file:
        convert_file.write(json.dumps(dict))





