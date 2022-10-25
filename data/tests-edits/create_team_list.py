import pandas as pd
import json
import requests


# response = requests.get("https://statsapi.mlb.com/api/v1/teams")
# res = response.json()
# all_teams = []
# for team in res["teams"]:
#     if team["sport"]["name"] == 'Major League Baseball':
#         name = team["name"]
#         team_id = team["teamCode"].upper()
#         mlb_id = team["id"]
#         first_year = team["firstYearOfPlay"]
#         division = team["division"]["name"]
#         all_teams.append({"name":name,"team_id":team_id,"mlb_id":mlb_id,"division":division,"first_year":first_year})
#
# with open("team_info.json", "w") as file :
#     json.dump(all_teams, file, indent=4 )
# # changed franch id to chadwick team tags

with open("team_info.json", "r") as file:
    team_info = json.load(file)

for index in range(len(team_info)):
    teams = pd.read_csv("../2022/ChadwickTeams.csv")
    teams = teams[["name", "franchID"]]
    franch = team_info[index]["team_id"]
    print(franch)
    teams = teams[teams.franchID == franch]
    print(teams)
    franch_teams = teams.drop_duplicates()
    team_list = franch_teams["name"].tolist()
    team_info[index]["other_names"] = team_list

with open("team_info1.json", "w") as file1:
    json.dump(team_info,file1,indent=4)
