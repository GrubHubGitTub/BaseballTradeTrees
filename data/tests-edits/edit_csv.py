import pandas as pd

# df1 = pd.read_csv("../../test1.csv")
# df2 = pd.read_csv("../../test2.csv")
#
# tree_info = pd.concat([df1, df2])
#
# tree_info = tree_info[["Link","Name","From-Team","From-Franchise","# Transactions","# Players Traded Away",
#                        "# Players Traded For","# Players Total","First Year","Last Year","Year Span","Ongoing",
#                        "Comp Picks","total_WAR_out","total_WAR_in","WAR_total","total_G_out","total_G_in",
#                        "G_total","total_PA_out","total_PA_in","PA_total","total_IP_out","total_IP_in","IP_total",
#                        "total_salary_out","total_salary_in","salary_total"]]
#
# tree_info.to_csv("all_tree_info.csv", index=False)

"""get ongoing trees"""
trees = pd.read_csv("../all_tree_info.csv")

all_ongoing = trees[trees["Ongoing"] == "Yes"]
all_ongoing = all_ongoing[["Link","Name","From-Team","From-Franchise","# Transactions","# Players Total",
                           "First Year","Last Year","Year Span","WAR_total",]]
html = all_ongoing.to_html(index=False, classes="statsTable table table-striped", table_id="ongoing")
with open("tables.txt", "a") as t:
    t.write(html)


# '''get the averages for each franchise'''
# franchises = pd.read_csv("../teams.csv")
# list_franchises = franchises["Franchise"].to_list()
#
# trees = pd.read_csv("../all_trees_with_links.csv")
#
# all_csv = []
#
# for franch in list_franchises:
#     # team names in franch
#     all_teams = franchises[franchises["Franchise"] == franch]
#     team_names = all_teams["CityName"].tolist()
#
#     franch_trees = trees[trees["From-Franchise"] == franch]
#     if franch_trees.empty:
#         pass
#     else:
#
#     #     number of trees
#         amount_trees = len(franch_trees.index)
#
#     #     average war total
#         average_WAR = round(franch_trees["WAR Total"].mean(), 4)
#
#     #     best/worst WAR tree
#         top = franch_trees.sort_values("WAR Total", ascending=False).head(1)
#         best_war = top["WAR Total"].item()
#         best_war_link = top["Link"].item()
#         bot = franch_trees.sort_values("WAR Total", ascending=True).head(1)
#         worst_war = bot["WAR Total"].item()
#         worst_war_link = top["Link"].item()
#
# #     WAR added together
#         total_WAR = round(franch_trees["WAR Total"].sum(), 3)
#
#     # average players
#         average_players = round(franch_trees["# Players Total"].mean(), 4)
#
# #     average transactions
#         average_trans = round(franch_trees["# Transactions"].mean(), 4)
#
# #     average year span
#         average_span = round(franch_trees["Year Span"].mean(), 4)
#
# # longest tree by year
#         longest_tree = franch_trees.sort_values("Year Span", ascending=False).head(1)
#         longest_num = longest_tree["Year Span"].item()
#         longest = longest_tree["Link"].item()
#
#         franch_csv = {"Franchise": franch, "Teams": team_names, "# Trees": amount_trees, "Average Tree WAR": average_WAR,
#                       "Total WAR": total_WAR, "Highest WAR Tree": best_war, "Highest WAR Link": best_war_link,
#                       "Average # Players": average_players, "Average # Transactions": average_trans,
#                       "Average Year Span": average_span, "Longest Tree (Years)": longest_num,"Longest Tree Link": longest}
#
#         all_csv.append(franch_csv)
#
# averages = pd.DataFrame(all_csv)
# averages.drop_duplicates(subset=['Franchise', '# Trees'], inplace=True)
# html = averages.to_html(index=False, classes="statsTable table table-striped", table_id="franchises")
# with open("tables.txt", "a") as t:
#     t.write(html)

"""get the top 100 in each category"""
# trees = pd.read_csv("../../all_trees_with_links.csv")

# # get top and worst war
# top100 = trees.sort_values("WAR Total", ascending=False).head(250)
# top100 = top100[["Link","Name","From-Team","From-Franchise","# Transactions","WAR Total"]]
# html = top100.to_html(index=False, classes="statsTable", table_id="WARpos")
# with open("tables.txt", "a") as t:
#     t.write(html)

# bot100 = trees.sort_values("WAR Total", ascending=True).head(250)
# bot100 = bot100[["Link","Name","From-Team","From-Franchise","# Transactions","WAR Total"]]
# html = bot100.to_html(index=False, classes="statsTable", table_id="WARneg")
# with open("tables.txt", "a") as t:
#     t.write(html)

# players and transactions

# topplayers = trees.sort_values("# Players Total", ascending=False).head(250)
# topplayers = topplayers[["Link","Name","From-Team","From-Franchise","WAR Total","# Players Total"]]
# html = topplayers.to_html(index=False, classes="statsTable", table_id="TopPlayers")
# with open("tables.txt", "a") as t:
#     t.write(html)
# toptrans = trees.sort_values("# Transactions", ascending=False).head(250)
# toptrans = toptrans[["Link","Name","From-Team","From-Franchise","WAR Total","# Transactions"]]
# html = toptrans.to_html(index=False, classes="statsTable", table_id="transactions")
# with open("tables.txt", "a") as t:
#     t.write(html)

# # year span
# long = trees.sort_values("Year Span", ascending=False).head(250)
# long = long[["Link","Name","From-Team","From-Franchise","WAR Total","First Year","Last Year","Year Span"]]
# html = long.to_html(index=False, classes="statsTable", table_id="yearSpan")
# with open("tables.txt", "a") as t:
#     t.write(html)

# franchise = pd.read_csv("../../franchise_averages.csv")
# html = franchise.to_html(index=False, classes="statsTable", table_id="avgFranch")
# with open("tables.txt", "a") as t:
#     t.write(html)