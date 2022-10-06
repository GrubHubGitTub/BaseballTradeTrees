import pandas as pd
from GetTransactions import GetTransactions as gt
from GetStats import GetStats as gs
from collections import Counter
import json

PLAYERS = pd.read_csv("playerdata.csv").fillna("")
PICKS = pd.read_csv("../comp_picks_retroid.csv")
TEAMS = pd.read_csv("../2022/ChadwickTeams.csv")
POSTSEASON = pd.read_csv("../2022/SeriesPost.csv")
"""add franchise tags to postseason"""
team_franchise_dict = TEAMS.set_index("teamID").to_dict()["franchID"]
POSTSEASON["franchIDwinner"] = POSTSEASON["teamIDwinner"].map(team_franchise_dict)


def format_names(retro_id_list=None, retro_id= None):
    if retro_id_list is not None:
        player_names = {}
        for player in retro_id_list:
            try:
                player_info = PLAYERS[PLAYERS["PLAYERID"] == player]
                name = player_info["name"].item()
            except ValueError:
                name = player
            player_names[player] = name
        return player_names
    else:
        try:
            player_info = PLAYERS[PLAYERS["PLAYERID"] == retro_id]
            name = player_info["name"].item()
        except ValueError:
            name = retro_id
        return name


def format_teams(team, date):
    year = int(str(date)[0:4])
    team_row = TEAMS[(TEAMS["teamIDretro"] == team) & (TEAMS["yearID"] == year)]
    try:
        name = team_row["name"].item()
    except ValueError:
        name = team
    return name


def format_outcomes(outcome_code):
    outcome_keys = {"A ": "assigned from one team to another without compensation",
                    "C ": "signed to another team on a conditional deal",
                    "Cr": "signed to another team on a conditional deal",
                    "D ": "rule 5 draft pick",
                    "Dr": "returned to original team after draft selection",
                    "F ": "free agent signing",
                    "Fg": "became a free agent",
                    "Hd": "declared ineligible",
                    "Hf": "demoted to the minor league",
                    "Hh": "held out",
                    "Hm": "went into military service",
                    "Hs": "suspended",
                    "Hu": "unavailable but not on DL",
                    "Hv": "voluntarity retired",
                    "J ": "jumped teams",
                    "L ": "loaned to another team",
                    "Mr": "rights returned when working agreement with minor league team ended",
                    "P ": "purchased by another team",
                    "R ": "released",
                    "T ": "trade",
                    "Tn": "traded but refused to report",
                    "U ": "unknown",
                    "Vg": "player assigned to league control",
                    "W ": "picked off waivers",
                    "Wf": "first year waiver pick",
                    "Wv": "waiver pick voided",
                    "X ": "lost in expansion draft",
                    "Z ": "voluntarily retired",
                    "Tr": "returned to original team"
                    }
    if outcome_code in outcome_keys:
        return outcome_keys[outcome_code]
    else:
        return outcome_code


def get_outcome_data(connections, transaction_list, trade_tree, franchise_choice, parent_retro, parent_transaction):
    """Takes a list of dictionaries of transactions, and uses the player ID, date and team choice to get a list of outcomes
     for each player"""
    # sort player's transactions by team choice and date and add 1 row outcome to list
    outcomes = []
    for transaction in transaction_list:
        date = transaction["date"]
        try:
            transaction_id = transaction["transaction_id"]
        except KeyError:
            transaction_id = 0
        player_list = transaction["traded_for"]
        parent_node = transaction["node_id"]

        for retro_id in player_list:
            # add PTBNL to tree, or continue if not
            if retro_id == "PTBNL/Cash":
                search = gt(transac_id=transaction_id)
                info = search.get_ptbnl_info()
                tree_node = {"id": len(trade_tree) + 1, "parentId": parent_node, "name": retro_id,
                                    "date": date, "info": info}
                trade_tree.append(tree_node)

            else:
                player_search = gt(retro_id=retro_id)

                # check if a player was re signed
                sorted_transactions = player_search.all_transac.sort_values(["primary_date"], ascending=True)

                sorted_transactions["type_next_row"] = sorted_transactions["type"].shift(-1)
                sorted_transactions["franchise_next_row"] = sorted_transactions["to_franchise"].shift(-1)
                resigned1 = sorted_transactions[(sorted_transactions["type"] == "Fg") & (sorted_transactions["type_next_row"] == "R ") &
                                   (sorted_transactions["franchise_next_row"] == sorted_transactions["from_franchise"])]
                resigned2 = sorted_transactions[(sorted_transactions["type"] == "Fg") & (sorted_transactions["type_next_row"] == "F ") &
                                   (sorted_transactions["franchise_next_row"] == sorted_transactions["from_franchise"])]
                no_released = pd.concat([sorted_transactions, resigned1, resigned2]).drop_duplicates(keep=False)
                all_outcomes = no_released[no_released["from_franchise"] == franchise_choice]

                outcome = all_outcomes[(all_outcomes["primary_date"] >= date) & (all_outcomes["transaction_ID"] != transaction_id)]
                if len(outcome.index) == 1:
                    outcome_dict = {"parentId": parent_node, "outcome": outcome}
                    outcomes.append(outcome_dict)

                # Choose one if there are multiple transactions from a team- first after date
                elif len(outcome.index) > 1:
                    sorted_by_dates = outcome.sort_values(by="primary_date")
                    player_outcomes = sorted_by_dates[sorted_by_dates["primary_date"] >= date]

                    outcome = player_outcomes.head(1)
                    outcome_dict = {"parentId": parent_node, "outcome": outcome}
                    outcomes.append(outcome_dict)

                # if player is retired or a newer player, add to the dictionary- dates can be changed for more accuracy
                elif outcome.empty:
                    sorted_transactions = player_search.all_transac.sort_values(by="primary_date")
                    to_choice = sorted_transactions[sorted_transactions["to_franchise"] == franchise_choice]
                    if to_choice.empty and " " in retro_id:
                        transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "name": retro_id,
                                            "outcome": "Did not play in MLB"}
                        trade_tree.append(transaction_info)

                    else:
                        last_row = sorted_transactions.tail(1)
                        last_date = last_row.primary_date.item()
                        if last_date <= 20150000:
                            transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node,
                                                "name": format_names(retro_id=retro_id), "retro_id": retro_id,
                                                "outcome": "No further transactions, likely retired", "date": date}
                            trade_tree.append(transaction_info)

                        else:
                            transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node,
                                                "name": format_names(retro_id=retro_id), "retro_id": retro_id,
                                                "outcome": "No further transactions, likely in organization", "date": date}
                            trade_tree.append(transaction_info)

    get_player_outcomes(connections, outcomes, trade_tree, franchise_choice,parent_retro,parent_transaction)


def get_player_outcomes(connections, outcomes, trade_tree, franchise_choice, parent_retro, parent_transaction):
    """Takes the list of outcomes to either find more transactions or add node to tradetree"""
    # loop through outcomes- tree line ends or more trades to search and the tree grows
    transactions_list = []
    for outcome in outcomes:
        code = outcome["outcome"]["type"].item()
        outcome_date = outcome["outcome"]["primary_date"].item()
        year = int(str(outcome_date)[0:4]) + 1
        player_id = outcome["outcome"]["player"].item()
        parent_node = outcome["parentId"]
        transaction_id = outcome["outcome"]["transaction_ID"].item()

        # end line if player was not traded or get comp picks to continue tree
        if code == "Fg":
            player_comp_picks = PICKS[PICKS["fa_retroid"] == player_id]
            player_comp_picks_year = player_comp_picks[player_comp_picks["year"] == year]
            all_comp_picks = player_comp_picks_year["signed_retroid"].tolist()
            if len(all_comp_picks) > 0:
                gt(transac_id=transaction_id, franch_id=franchise_choice, parent_retro=parent_retro, parent_transaction=parent_transaction)
                stats = gs(transaction_id=transaction_id, franch_choice=franchise_choice)
                trade_in_stats = stats.get_trade_in_stats()

                transaction_info1 = {"node_id": len(trade_tree) + 1, "date": outcome_date, "traded_for": all_comp_picks}
                transactions_list.append(transaction_info1)
                # add comp pick transaction to tree
                transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "retro_id": player_id,
                                    "name": format_names(retro_id=player_id), "transaction_id": transaction_id,
                                    "info": "Compensation picks", "traded_with": {}, "trade_in_stats": trade_in_stats,
                                    "date": outcome_date}
                trade_tree.append(transaction_info)


            else:
                # End branch and add node to tree
                transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "name": format_names(retro_id=player_id),
                                    "retro_id": player_id, "outcome": format_outcomes(code),
                                    "date": outcome_date}
                trade_tree.append(transaction_info)

        elif code != "T ":
            transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "name": format_names(retro_id=player_id),
                                "retro_id": player_id, "outcome": format_outcomes(code), "date": outcome_date}
            trade_tree.append(transaction_info)

        # get new transaction ids to search
        elif code == "T ":

            transaction = gt(transac_id=transaction_id, franch_id=franchise_choice, parent_retro=parent_retro,
                             parent_transaction=parent_transaction)
            transaction.get_trades()
            traded_with = format_names(retro_id_list=transaction.get_traded_with_ids_list())
            if player_id in traded_with:
                traded_with.pop(player_id)

            stats = gs(transaction_id=transaction_id, franch_choice=franchise_choice)
            trade_out_stats = stats.get_trade_out_stats()
            trade_in_stats = stats.get_trade_in_stats()
            trade_totals = stats.get_trade_totals()

            # check that the transaction isn't already in next search loop or in tree
            match = False
            for node in trade_tree:
                if "transaction_id" in node and node["transaction_id"] == transaction_id:
                    match = True
                    connections.append({"from": len(trade_tree)+1, "to":node["id"], "label": "Tree continues"})

                    if type(outcome["outcome"]["to_franchise"].item()) == float:
                        print("yes")
                        to_franchise = ""
                    else:
                        to_franchise = outcome["outcome"]["to_franchise"].item()

                    node_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "retro_id": player_id,
                                 "name": format_names(retro_id=player_id), "traded_with": traded_with,
                                 "to_team": {"team_id": outcome["outcome"]["to_team"].item(),
                                             "team_name": format_teams(team=outcome["outcome"]["to_team"].item(),
                                                                       date=outcome_date)},
                                 "to_franchise":to_franchise, "date": outcome_date}
                    trade_tree.append(node_info)

            if not match:
                for orgnl in transactions_list:
                    if "transaction_id" in orgnl and orgnl["transaction_id"] == transaction_id:
                        match = True
                        connections.append({"from": len(trade_tree) + 1, "to": orgnl["node_id"], "label": "Tree continues"})

                        if type(outcome["outcome"]["to_franchise"].item()) == float:
                            print("yes")
                            to_franchise = ""
                        else:
                            to_franchise = outcome["outcome"]["to_franchise"].item()

                        node_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "retro_id": player_id,
                                     "name": format_names(retro_id=player_id), "traded_with": traded_with,
                                     "to_team": {"team_id": outcome["outcome"]["to_team"].item(),
                                                 "team_name": format_teams(team=outcome["outcome"]["to_team"].item(),
                                                                           date=outcome_date)},
                                     "to_franchise": to_franchise, "date": outcome_date}
                        trade_tree.append(node_info)

            if not match:
                if type(outcome["outcome"]["to_franchise"].item()) == float:
                    print("yes")
                    to_franchise = ""
                else:
                    to_franchise = outcome["outcome"]["to_franchise"].item()
                node_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "retro_id": player_id,
                             "name": format_names(retro_id=player_id), "transaction_id": transaction_id,
                             "traded_with": traded_with, "trade_out_stats": trade_out_stats,
                             "trade_in_stats": trade_in_stats, "trade_totals": trade_totals,
                             "to_team": {"team_id": outcome["outcome"]["to_team"].item(),
                                         "team_name": format_teams(team=outcome["outcome"]["to_team"].item(),
                                                                   date=outcome_date)},
                             "to_franchise": to_franchise, "date": outcome_date}

                transaction_info = {"node_id": len(trade_tree) + 1, "transaction_id": transaction_id,
                                    "date": outcome_date, "traded_for": transaction.get_traded_for_ids_dict()}
                trade_tree.append(node_info)
                transactions_list.append(transaction_info)

    if len(transactions_list) > 0:
        get_outcome_data(connections, transactions_list, trade_tree, from_franch, parent_retro,parent_transaction)


def get_tree_totals(trade_tree):
    bat = Counter()
    pitch = Counter()
    war_sal_as = Counter()
    era_p_in = []
    era_p_out = []
    baopp_p_in = []
    baopp_p_out = []

    totals = []
    for node in trade_tree:
        if "trade_totals" in node:
            totals.append(node["trade_totals"])
    for total in totals:
        bat.update(total["batting_stats"])
        pitch.update(total["pitching_stats"])
        war_sal_as.update(total["other_stats"])
        if type(total["pitching_other"]["ERA"]["in"]) == float :
            era_p_in.append(total["pitching_other"]["ERA"]["in"])
            baopp_p_in.append(total["pitching_other"]["BAOpp"]["in"])
        if type(total["pitching_other"]["ERA"]["out"]) == float:
            era_p_out.append(total["pitching_other"]["ERA"]["out"])
            baopp_p_out.append(total["pitching_other"]["BAOpp"]["out"])

    war_sal_as["WAR"] = round(war_sal_as["WAR"], 2)
    war_sal_as["salary"] = int(war_sal_as["salary"])
    era_p_in = [x for x in era_p_in if x != []]
    era_p_out = [x for x in era_p_out if x != []]
    baopp_p_in = [x for x in baopp_p_in if x != []]
    baopp_p_out = [x for x in baopp_p_out if x != []]
    if len(era_p_in) > 0:
        pitch["ERA_p_in"] = format(round(sum(era_p_in) / len(era_p_in), 2) , '.2f')
        pitch["BAOpp_p_in"] = format(round(sum(baopp_p_in) / len(baopp_p_in), 3), '.3f')
    if len(era_p_out) > 0:
        pitch["ERA_p_out"] = format(round(sum(era_p_out) / len(era_p_out), 2), '.2f')
        pitch["BAOpp_p_out"] = format(round(sum(baopp_p_out) / len(baopp_p_out), 3), '.3f')

    tree_totals = {"batting_stats": dict(bat), "pitching_stats": dict(pitch), "war_sal": dict(war_sal_as)}
    return tree_totals


def get_ws_wins(trade_tree):
    dates = []
    for node in trade_tree:
        if "date" in node:
            dates.append(node["date"])
    dates.sort()
    first = str(dates[0])[0:4]
    last = str(dates[-1])[0:4]
    wins = POSTSEASON[(POSTSEASON["yearID"] <= int(last)) & (POSTSEASON["yearID"] >= int(first)) &
                      (POSTSEASON["round"] == "WS") & (POSTSEASON["franchIDwinner"] == from_franch)]
    world_series = []
    if not wins.empty:
        world_series += wins["yearID"].tolist()
        print(f"{from_franch} winners in {world_series}")
    return world_series


"""sort fg(with stats) and T transactions by date, then get list of all retroids """
with open("PlayersToGenerate.json", "r") as file:
    retro_ids = json.load(file)

index = 0
all_data = []
for player_transaction in retro_ids[index:]:
    print(index)
    print(player_transaction["player"])
    index += 1
    if (player_transaction["from_franchise"] != "" and player_transaction["to_franchise"] != "") \
            and " " not in player_transaction["player"]:

        transac_id = player_transaction["transaction_ID"]
        from_team = player_transaction["from_team"]
        from_franch = player_transaction["from_franchise"]
        date = player_transaction["primary_date"]
        parent = player_transaction["player"]
        to_team = player_transaction["to_team"]
        to_franchise = player_transaction["to_franchise"]
        tree_name = player_transaction["player"] + "_" + str(transac_id)

        # Get player info
        player_info = PLAYERS[PLAYERS["PLAYERID"] == player_transaction["player"]]
        if player_info.empty:
            continue
        try:
            mlb_id = int(player_info["key_mlbam"].item())
        except ValueError:
            mlb_id = ""

        name = player_info["name"].item()
        hof = player_info["HOF"].item()
        try:
            debut = int(player_info["mlb_played_first"].item())
        except ValueError:
            debut = ""
        end = player_info["mlb_played_last"].item()

        # filters DB for player's trade
        tree_data = gt(transac_id=transac_id, franch_id=from_franch, parent_retro=parent,parent_transaction=transac_id)
        tree_data.get_trades()

        traded_with_players = format_names(retro_id_list=tree_data.get_traded_with_ids_list())
        if player_transaction["player"] in traded_with_players:
            traded_with_players.pop(player_transaction["player"])

        # get stats
        stats = gs(transaction_id=transac_id, franch_choice=from_franch)
        trade_out_stats = stats.get_trade_out_stats()
        trade_in_stats = stats.get_trade_in_stats()
        trade_totals = stats.get_trade_totals()

        # save initial trade to tree-- add additional stats in first transac search
        trade_tree = []
        tree_node = {"id": 1, "parentId": "", "retro_id": player_transaction["player"], "name": name,
                     "transaction_id": transac_id, "date": date,
                     "to_team": {"team_id": to_team, "team_name": format_teams(team=to_team, date=date)},
                     "to_franch": to_franchise, "traded_with": traded_with_players,
                     "trade_in_stats": trade_in_stats, "trade_out_stats": trade_out_stats, "trade_totals": trade_totals}
        trade_tree.append(tree_node)

        # add trade to trans dict for searching
        transactions_list = []
        transaction_details = {"node_id": 1, "parent": player_transaction["player"],
                               "retro_id": player_transaction["player"], "from_team": from_team,
                               "from_franchise": from_franch, "to_team": to_team, "to_franch": to_franchise,
                               "transaction_id": transac_id, "date": date, "traded_with": traded_with_players,
                               "traded_for": tree_data.get_traded_for_ids_dict()}
        transactions_list.append(transaction_details)
        connections = []

        # start the search loop
        get_outcome_data(connections=connections, transaction_list=transactions_list, trade_tree=trade_tree,
                         franchise_choice=from_franch, parent_retro=player_transaction["player"], parent_transaction=transac_id)

        #  calculate totals for tree
        tree_totals = get_tree_totals(trade_tree=trade_tree)

        # get WS wins
        ws_wins = get_ws_wins(trade_tree=trade_tree)

        # get parent tree
        parent_trees = pd.read_csv("ParentTrees.csv")
        parent_row = parent_trees[(parent_trees["transaction_ID"] == transac_id) & (parent_trees["from_franch"] == from_franch)]
        parent_tree_retro = parent_row["parent_tree_retro"].item()
        parent_tree_transaction_id = parent_row["parent_tree_transaction_id"].item()
        if parent_tree_retro == player_transaction["player"] or \
                parent_tree_transaction_id == player_transaction["transaction_ID"]:
            parent_tree_retro = ""
            parent_tree_transaction_id = ""

        # check if ongoing
        ongoing = ""
        for node in trade_tree:
            if "outcome" in node:
                if node["outcome"] == "No further transactions, likely in organization":
                    ongoing = f"{player_transaction['player']}_{transac_id}"

        trade_output = {
            "from_team": {"team_id": from_team, "team_name": format_teams(team=from_team, date=date)},
            "from_franch": from_franch,
            "to_team": {"team_id": to_team, "team_name": format_teams(team=to_team, date=date)},
            "date": date,
            "ongoing": ongoing,
            "transaction_id": transac_id,
            "tree_id": f"{player_transaction['player']}_{transac_id}",
            "largest_tree_id": f"{parent_tree_retro}_{parent_tree_transaction_id}",
            "total_stats": tree_totals,
            "world_series_wins": ws_wins,
            "tree_details": {
                "tree_id": f"{player_transaction['player']}_{transac_id}",
                "tree_display": trade_tree,
                "connections": connections
            }
        }

        match = False
        for data in all_data:
            if "retro_id" in data and data["retro_id"] == player_transaction["player"]:
                data["trades"].append(trade_output)
                match = True
                break

        if not match:
            output = {
                "retro_id": player_transaction["player"],
                "mlb_id": mlb_id,
                "name": name,
                "HOF": hof,
                "debut_year": debut,
                "last_year": end,
                "ongoing_tree": ongoing,
                "trades": [trade_output]
            }
            all_data.append(output)

with open("output.json", "r+") as file:
    json.dump(all_data, file)

# df = pd.read_json("output.json")
# df.to_csv("outputcsv.csv", index= False)


        # with open("output.json", "r+") as file:
        #     file_data = json.load(file)
        #     match = False
        #     for data in file_data["player_data"]:
        #         if data["retro_id"] == player_transaction["player"]:
        #             data["trades"].append(trade_output)
        #             match = True
        #             break
        #     if not match:
        #         output = {
        #             "retro_id": player_transaction["player"],
        #             "mlb_id": mlb_id,
        #             "name": name,
        #             "HOF": hof,
        #             "debut_year": debut,
        #             "last_year": end,
        #             "ongoing_tree": ongoing,
        #             "trades": [trade_output]
        #         }
        #         file_data["player_data"].append(output)
        #     file.seek(0)
        #     json.dump(file_data, file, indent=4)




