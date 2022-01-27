# from bs4 import BeautifulSoup
# import requests
import pandas as pd

# round = 1
# year = 1978
# all_comp_picks = []
# problems = []
# prob_text = []
# while year < 2021:
#     response = requests.get(f"https://www.baseball-reference.com/draft/?draft_round={round}&year_ID={year}&draft_type=junreg&query_type=year_round")
#     webpage = response.text
#     soup = BeautifulSoup(webpage, "html.parser")
#
#     comp = soup.select('p.note')[0]
#     # signed = {}
#     # for l in comp.find_all('strong'):
#     #     if "*" in l.get_text():
#     #         pass
#     #     else:
#     #         signed.append(l.get_text())
#     #
#     # free_agent = []
#     # for l in comp.find_all('a'):
#     #     free_agent.append(l.get_text())
#     #
#     # if len(signed) != len(free_agent):
#     #     picks = {}
#     for element in comp:
#         if "Compensation" in element.get_text():
#             for el in comp:
#                 if "Compensation" in el.get_text():
#                     pass
#                 else:
#                     next = el.next_element
#                     nextnext = next.next_element
#                     nextnextnext = nextnext.next_element
#                     if el.name == "strong" and nextnextnext.name == "a":
#                         pick = {}
#                         pick["signed"] = el.get_text()
#                         pick["free agent"] = nextnextnext.get_text()
#                         pick["year"] = str(year)
#                         all_comp_picks.append(pick)
#                         print("pick added")
#                     elif el.name == "strong":
#                         pick = {}
#                         pick["signed"] = el.get_text()
#                         pick["free agent"] = "None"
#                         pick["year"] = str(year)
#                         all_comp_picks.append(pick)
#                         print("pick added no f/a")
#                     else:
#                         prob_text.append(f"{el}, {year}, {round}")
#             print(f" Good {year} {round}")
#             break
#         else:
#             pass
#     # else:
#     #     zip_iterator = zip(signed, free_agent)
#     #     picks = dict(zip_iterator)
#     #     all_comp_picks.append(picks)
#
#     if round == 4:
#         round = 1
#         print(f"done {year}")
#         year += 1
#     else:
#         round += 1
#
# result = pd.DataFrame(all_comp_picks)
# result.to_csv("test2.csv")
#
# all_problems = pd.DataFrame(problems)
# all_problems.to_csv("probs2.csv")

"""add retro ids to draft pick file"""
# add name splits
# picks = pd.read_csv("Old Data/comp_picks_with_year.csv")
# picks[['first_signed','last_signed']] = picks['signed'].loc[picks['signed'].str.split().str.len() == 2].str.split(expand=True)
# picks[['first_fa', 'last_fa']] = picks['FreeAgent'].loc[picks['FreeAgent'].str.split().str.len() == 2].str.split(expand=True)
# picks.to_csv("picks_with_names.csv", index=False)

#add retroid to csv
picks = pd.read_csv("../picks_with_names.csv")
players = pd.read_csv("../Players2022.csv")
all_rows=[]
for index, row in picks.iterrows():
    first_signed = row["first_signed"]
    last_signed = row["last_signed"]
    first_fa = row["first_fa"]
    last_fa = row["last_fa"]

    row_with_signed_name = players[(players.nickname == first_signed) & (players.Last == last_signed)]
    try:
        row["signed_retroid"] = row_with_signed_name.ID.item()
    except ValueError:
        row["signed_retroid"] = f"{first_signed} {last_signed}"

    row_with_fa_name = players[(players.nickname == first_fa) & (players.Last == last_fa)]
    try:
        row["fa_retroid"] = row_with_fa_name.ID.item()
    except ValueError:
        row["fa_retroid"] = f"{first_fa} {last_fa}"

    all_rows.append(row)

final = pd.DataFrame.from_dict(map(dict,all_rows))
final.to_csv("comp_picks_retroid.csv",index=False)

