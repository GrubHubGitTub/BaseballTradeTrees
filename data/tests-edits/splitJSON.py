import json

# split = 3500
# with open("all_data.json", "r") as file:
#     data = json.load(file)
#     with open("all_data1.json", "w") as file1:
#         json.dump(data[:split], file1)
#     with open("all_data2.json", "w") as file2:
#         json.dump(data[split:], file2)

# data = []
#
# with open("all_data1.json", "r") as file1:
#     data += json.load(file1)
#
# with open("all_data2.json", "r") as file2:
#     data += json.load(file2)
#
# with open("all_data.json", "w") as file3:
#     json.dump(data, file3)


with open("all_data.json", "r") as file3:
    data = json.load(file3)

all_trees = []
for player in data:
    for trade in player["trades"]:
        all_trees.append(trade)

with open("all_treetest.json", "w") as file4:
    json.dump(all_trees, file4)


