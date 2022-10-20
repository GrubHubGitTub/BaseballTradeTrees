import pandas as pd
import json
import requests

# teams = pd.read_csv("../2022/ChadwickTeams.csv")
# teams = teams[["teamIDretro", "teamID", "teamIDBR", "franchID", "name" ]]
# teams = teams.drop_duplicates()
# teams.to_csv("FranchiseList.csv", index=False)
#
# """check for duplicate Ids for stat problems"""

# teams = pd.read_csv("./FranchiseList.csv")
#
# list = teams['teamIDretro'].tolist()
#
# index = 0
# for team in list:
#     index += 1
#     for team2 in list[index:]:
#         if team == team2:
#             print(team)

response = requests.get("https://statsapi.mlb.com/api/v1/teams")
res = response.json()
all_teams = []
for team in res["teams"]:
    if team["sport"]["name"] == 'Major League Baseball':
        name = team["name"]
        team_id = team["teamCode"].upper()
        mlb_id = team["id"]
        first_year = team["firstYearOfPlay"]
        all_teams.append({"name":name,"team_id":team_id,"mlb_id":mlb_id,"first_year":first_year})

with open("team_info.json", "w") as file :
    json.dump(all_teams, file, indent=4 )


