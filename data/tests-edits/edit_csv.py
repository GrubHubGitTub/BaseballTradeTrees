import pandas as pd

# df1 = pd.read_csv("test1.csv")
# df2 = pd.read_csv("test2.csv")
# df3 = pd.read_csv("test3.csv")
#
# result = pd.concat([df1, df2, df3])
#
# result.to_csv("tree_info.csv",index=False)

# tree_info = pd.read_csv("tree_info.csv")
#
# tree_info = tree_info[["Player ID","Name","Traded From- Team Name","Traded From- Franchise","Total Transactions",
#                        "Amount Players Traded Away","Amount Players Traded For","Amount Players Total","Earliest Year",
#                        "Latest Year","Year Span","total_WAR_out","total_WAR_in","WAR_total","total_G_out","total_G_in",
#                        "G_total","total_PA_out","total_PA_in","PA_total","total_IP_out","total_IP_in","IP_total",
#                        "total_salary_out","total_salary_in","salary_total"]]

# trees = pd.read_csv("tree_info_filtered.csv")
# trees = trees[~(trees['Player ID'].str.contains(" "))]
#
# trees.to_csv("removed_non_retro.csv", index=False)

trees = pd.read_csv("../../removed_non_retro.csv")

for index,row in trees.iterrows():
    id = row["Player ID"]
    link = f"<a href=/player/{id}>{id}</a>"
    trees.loc[index, 'Link'] = link



trees= trees[["Link","Name","Traded From- Team Name","Traded From- Franchise","Total Transactions",
                       "Amount Players Traded Away","Amount Players Traded For","Amount Players Total","Earliest Year",
                       "Latest Year","Year Span","total_WAR_out","total_WAR_in","WAR_total","total_G_out","total_G_in",
                       "G_total","total_PA_out","total_PA_in","PA_total","total_IP_out","total_IP_in","IP_total",
                       "total_salary_out","total_salary_in","salary_total"]]
trees.to_csv("removed_non_with_ids.csv")