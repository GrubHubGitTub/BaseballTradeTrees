import pandas as pd

teams = pd.read_csv("../2022/ChadwickTeams.csv")
teams = teams[["teamIDretro", "teamID", "teamIDBR", "franchID", "name" ]]
teams = teams.drop_duplicates()
teams.to_csv("FranchiseList.csv", index=False)

"""check for duplicate Ids for stat problems"""

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