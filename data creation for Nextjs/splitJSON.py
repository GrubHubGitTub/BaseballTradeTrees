import json
import pandas as pd

split = 4000
all_data = []
with open("all_data1.json", "r") as file1:
    all_data += json.load(file1)
with open("all_data2.json", "r") as file2:
    all_data += json.load(file2)
with open("all_data3.json", "w") as file3:
    json.dump(all_data[:split], file3)
with open("all_data4.json", "w") as file4:
    json.dump(all_data[split:], file4)

# with open("all_parent_trees_no_details.json", "r") as file:
#     data = json.load(file)
#     # for tree in data:
#     df = pd.json_normalize(data[0], sep='_')
#     print(df.to_dict(orient='records')[0])

# with open("stats_transactions_06092022.json", "r") as file:
# df = pd.read_json("stats_transactions_06092022.json")
# new_d = df.to_dict("records")
# all_transac=[]
# for transac in new_d:
#     if transac["stats"] != "":
#         all_transac.append(transac)
#
# with open("transaction_list.json", "w") as file1:
#     json.dump(all_transac, file1)



