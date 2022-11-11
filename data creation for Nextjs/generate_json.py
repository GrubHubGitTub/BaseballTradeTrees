import pandas as pd
from GetTransactions import GetTransactions as gt
from GetStats import GetStats as gs
from collections import Counter
import json

PLAYERS = pd.read_csv("create_data_output/playerdata.csv").fillna("")
PICKS = pd.read_csv("2022 raw files/comp_picks_retroid.csv")
TEAMS = pd.read_csv("2022 raw files/ChadwickTeams.csv")
POSTSEASON = pd.read_csv("2022 raw files/SeriesPost.csv")
FRANCHISES = pd.read_json("create_data_output/team_info.json")
"""add franchise tags to postseason"""
team_franchise_dict = TEAMS.set_index("teamID").to_dict()["franchID"]
POSTSEASON["franchIDwinner"] = POSTSEASON["teamIDwinner"].map(team_franchise_dict)


def format_names(retro_id_list=None, retro_id=None):
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


def format_teams(team, date, to_team=False, franchise=None):
    if to_team is False and franchise is None:
        year = int(str(date)[0:4])
        team_row = TEAMS[(TEAMS["teamIDretro"] == team) & (TEAMS["yearID"] == year)]
        try:
            name = team_row["name"].item()
        except ValueError:
            try:
                year += 1
                team_row = TEAMS[(TEAMS["teamIDretro"] == team) & (TEAMS["yearID"] == year)]
                name = team_row["name"].item()
            except ValueError:
                name = team
        return name
    elif franchise is not None:
        franchise_row = FRANCHISES[FRANCHISES["team_id"] == franchise]
        try:
            franchise_name = franchise_row["name"].item()
        except ValueError:
            franchise_name = franchise
        return franchise_name
    else:
        year = int(str(date)[0:4])
        team_row = TEAMS[(TEAMS["teamIDretro"] == team) & (TEAMS["yearID"] == year)]
        try:
            name = team_row["name"].item()
            franch = team_row["franchID"].item()
        except ValueError:
            name = team
            franch = team
        return {"name": name, "to_franch": franch}


def format_outcomes(outcome_code):
    outcome_keys = {"A ": "assigned from one team to another without compensation",
                    "C ": "signed to another team on a conditional deal",
                    "Cr": "signed to another team on a conditional deal",
                    "D ": "rule 5 draft pick",
                    "Da": "amateur draft pick",
                    "Df": "first year draft pick",
                    "Dm": "minor league draft pick",
                    "Dn": "selected in amateur draft but did not sign",
                    "Dr": "returned to original team after draft selection",
                    "Ds": "special draft pick",
                    "Dv": "amateur draft pick voided",
                    "F ": "free agent signing",
                    "Fa": "amateur free agent signing",
                    "Fb": "amateur free agent 'bonus baby' signing under the 1953 - 57 rule requiring player to stay on ML roster",
                    "Fc": "free agent compensation pick",
                    "Fg": "became a free agent",
                    "Fo": "free agent signing with first ML team",
                    "Fv": "free agent signing voided",
                    "Hb": "went on the bereavement list",
                    "Hbr": "came off the bereavement list",
                    "Hd": "declared ineligible",
                    "Hdr": "reinistated from the ineligible list",
                    "Hf": "demoted to the minor league",
                    "Hfr": "promoted from the minor league",
                    "Hh": "held out",
                    "Hhr": "ended hold out",
                    "Hi": "went on the disabled list",
                    "Hir": "came off the disabled list",
                    "Hm": "went into military service",
                    "Hmr": "returned from military service",
                    "Hs": "suspended",
                    "Hsr": "reinstated after a suspension",
                    "Hu": "unavailable but not on DL",
                    "Hur": "returned from being unavailable",
                    "Hv": "voluntarity retired",
                    "Hvr": "unretired",
                    "J ": "jumped teams",
                    "Jr": "returned to original team after jumping",
                    "L ": "loaned to another team",
                    "Lr": "returned to original team after loan",
                    "M ": "obtained rights when entering into working agreement with minor league team",
                    "Mr": "rights returned when working agreement with minor league team ended",
                    "P ": "purchased by another team",
                    "Pr": "returned to original team after purchase",
                    "Pv": "purchase voided",
                    "R ": "released",
                    "T ": "traded",
                    "Tn": "traded but refused to report",
                    "Tp": "added to trade(usually because one of the original players refused to report or retired)",
                    "Tv": "trade voided",
                    "U ": "unknown",
                    "Vg": "player assigned to league control",
                    "V": "player purchased or assigned to team from league",
                    "W ": "waiver pick",
                    "Wf": "first year waiver pick",
                    "Wr": "returned to original team after waiver pick",
                    "Wv": "waiver pick voided",
                    "X ": "lost in expansion draft",
                    "Xe": "premium phase of expansion draft",
                    "Xm": "either the 1960 AL minor league expansion draft or the premium phase of the 1961 NL draft",
                    "Xp": "added as expansion pick at a later date",
                    "Xr": "returned to original team after expansion draft",
                    "Z ": "voluntarily retired",
                    "Zr": "returned from voluntarily retired list",
                    "Tr": "returned to original team"
                    }
    if outcome_code in outcome_keys:
        return outcome_keys[outcome_code]
    else:
        return outcome_code


def format_retrosheet(list_of_transactions):
    for transaction in list_of_transactions:
        date = transaction["primary_date"]
        transaction["type"] = format_outcomes(transaction["type"])
        transaction["from_team"] = format_teams(date=date, team=transaction["from_team"])
        transaction["to_team"] = format_teams(date=date, team=transaction["to_team"])
        transaction["from_franchise"] = format_teams(franchise=transaction["from_franchise"], date=None, team=None)
        transaction["to_franchise"] = format_teams(franchise=transaction["to_franchise"], date=None, team=None)
    return list_of_transactions


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
                resigned1 = sorted_transactions[
                    (sorted_transactions["type"] == "Fg") & (sorted_transactions["type_next_row"] == "R ") &
                    (sorted_transactions["franchise_next_row"] == sorted_transactions["from_franchise"])]
                resigned2 = sorted_transactions[
                    (sorted_transactions["type"] == "Fg") & (sorted_transactions["type_next_row"] == "F ") &
                    (sorted_transactions["franchise_next_row"] == sorted_transactions["from_franchise"])]
                no_released = pd.concat([sorted_transactions, resigned1, resigned2]).drop_duplicates(keep=False)

                all_outcomes = no_released[no_released["from_franchise"] == franchise_choice]
                outcome = all_outcomes[
                    (all_outcomes["primary_date"] >= date) & (all_outcomes["transaction_ID"] != transaction_id)]

                # fix cody ross- was purchased by a team before original trade was finalized
                if retro_id == "rossc001" and parent_retro == "kozlb001":
                    outcome = all_outcomes[
                        (all_outcomes["primary_date"] >= 20060526) & (all_outcomes["transaction_ID"] != transaction_id)]

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
                    if (to_choice.empty and " " in retro_id) or sorted_transactions.empty:
                        transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "retro_id": retro_id,
                                            "name": retro_id, "outcome": "Did not play in MLB"}
                        trade_tree.append(transaction_info)

                    else:
                        last_row = sorted_transactions.tail(1)
                        last_date = last_row.primary_date.item()
                        if last_date <= 20000000:
                            transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node,
                                                "name": format_names(retro_id=retro_id), "retro_id": retro_id,
                                                "outcome": "retired", "date": last_date}
                            trade_tree.append(transaction_info)
                        elif 20130000 >= last_date > 20000000:
                            transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node,
                                                "name": format_names(retro_id=retro_id), "retro_id": retro_id,
                                                "outcome": "No further transactions, likely retired", "date": last_date}
                            trade_tree.append(transaction_info)

                        else:
                            transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node,
                                                "name": format_names(retro_id=retro_id), "retro_id": retro_id,
                                                "outcome": "No further transactions, likely in organization",
                                                "date": last_date}
                            trade_tree.append(transaction_info)

    get_player_outcomes(connections, outcomes, trade_tree, franchise_choice, parent_retro, parent_transaction)


def get_player_outcomes(connections, outcomes, trade_tree, franchise_choice, parent_retro, parent_transaction):
    """Takes the list of outcomes to either find more transactions or add node to tradetree"""
    # loop through outcomes- tree line ends or more trades to search and the tree grows
    transactions_list = []
    for outcome in outcomes:
        code = outcome["outcome"]["type"].item()
        outcome_date = outcome["outcome"]["primary_date"].item()
        draft_year = int(str(outcome_date)[0:4]) + 1
        player_id = outcome["outcome"]["player"].item()
        parent_node = outcome["parentId"]
        transaction_id = outcome["outcome"]["transaction_ID"].item()

        # end line if player was not traded or get comp picks to continue tree
        if code == "Fg":
            player_comp_picks = PICKS[PICKS["fa_retroid"] == player_id]
            player_comp_picks_year = player_comp_picks[player_comp_picks["year"] == draft_year]
            all_comp_picks = player_comp_picks_year["signed_retroid"].tolist()
            if len(all_comp_picks) > 0:
                gt(transac_id=transaction_id, franch_id=franchise_choice, parent_retro=parent_retro,
                   parent_transaction=parent_transaction)
                stats = gs(transaction_id=transaction_id, franch_choice=franchise_choice)

                # need to flip the trade stats because of it being a comp pick and the from team is the choice.
                trade_in_stats = stats.get_trade_out_stats()
                trade_totals = stats.get_comp_totals()

                transaction_info1 = {"node_id": len(trade_tree) + 1, "date": outcome_date, "traded_for": all_comp_picks}
                transactions_list.append(transaction_info1)
                # add comp pick transaction to tree
                transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "retro_id": player_id,
                                    "name": format_names(retro_id=player_id), "transaction_id": transaction_id,
                                    "info": "Compensation picks", "traded_with": {}, "trade_in_stats": trade_in_stats,
                                    "trade_out_stats": [], "trade_totals": trade_totals, "date": outcome_date}
                trade_tree.append(transaction_info)

            else:
                # End branch and add node to tree
                transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node,
                                    "name": format_names(retro_id=player_id),
                                    "retro_id": player_id, "outcome": format_outcomes(code),
                                    "date": outcome_date}
                trade_tree.append(transaction_info)

        elif code != "T ":
            transaction_info = {"id": len(trade_tree) + 1, "parentId": parent_node,
                                "name": format_names(retro_id=player_id),
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
                    connections.append({"from": len(trade_tree) + 1, "to": node["id"], "label": "Tree continues"})

                    if type(outcome["outcome"]["to_franchise"].item()) == float:
                        to_franchise = ""
                    else:
                        to_franchise = outcome["outcome"]["to_franchise"].item()

                    node_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "retro_id": player_id,
                                 "name": format_names(retro_id=player_id), "traded_with": traded_with,
                                 "to_team": {"team_id": outcome["outcome"]["to_team"].item(),
                                             "team_name": format_teams(team=outcome["outcome"]["to_team"].item(),
                                                                       date=outcome_date, to_team=True)},
                                 "to_franchise": to_franchise, "date": outcome_date}
                    trade_tree.append(node_info)

            if not match:
                for orgnl in transactions_list:
                    if "transaction_id" in orgnl and orgnl["transaction_id"] == transaction_id:
                        match = True
                        connections.append(
                            {"from": len(trade_tree) + 1, "to": orgnl["node_id"], "label": "Tree continues"})

                        if type(outcome["outcome"]["to_franchise"].item()) == float:
                            to_franchise = ""
                        else:
                            to_franchise = outcome["outcome"]["to_franchise"].item()

                        node_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "retro_id": player_id,
                                     "name": format_names(retro_id=player_id), "traded_with": traded_with,
                                     "to_team": {"team_id": outcome["outcome"]["to_team"].item(),
                                                 "team_name": format_teams(team=outcome["outcome"]["to_team"].item(),
                                                                           date=outcome_date, to_team=True)},
                                     "to_franchise": to_franchise, "date": outcome_date}
                        trade_tree.append(node_info)

            if not match:
                if type(outcome["outcome"]["to_franchise"].item()) == float:
                    to_franchise = ""
                else:
                    to_franchise = outcome["outcome"]["to_franchise"].item()
                node_info = {"id": len(trade_tree) + 1, "parentId": parent_node, "retro_id": player_id,
                             "name": format_names(retro_id=player_id), "transaction_id": transaction_id,
                             "traded_with": traded_with, "trade_out_stats": trade_out_stats,
                             "trade_in_stats": trade_in_stats, "trade_totals": trade_totals,
                             "to_team": {"team_id": outcome["outcome"]["to_team"].item(),
                                         "team_name": format_teams(team=outcome["outcome"]["to_team"].item(),
                                                                   date=outcome_date, to_team=True)},
                             "to_franchise": to_franchise, "date": outcome_date}

                transaction_info = {"node_id": len(trade_tree) + 1, "transaction_id": transaction_id,
                                    "date": outcome_date, "traded_for": transaction.get_traded_for_ids_dict()}
                trade_tree.append(node_info)
                transactions_list.append(transaction_info)

    if len(transactions_list) > 0:
        get_outcome_data(connections, transactions_list, trade_tree, from_franch, parent_retro, parent_transaction)


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
        if type(total["pitching_other"]["ERA"]["in"]) == float:
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
        pitch["ERA_p_in"] = format(round(sum(era_p_in) / len(era_p_in), 2), '.2f')
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
    return world_series


"""sort fg(with stats) and T transactions by date, then get list of all retroids """
with open("create_data_output/PlayersToGenerate.json", "r") as file:
    retro_ids = json.load(file)

index = 0
all_data = []
ongoing_tree_players = []
player_search = []
all_parent_trees = []
all_parent_trees_no_detail_no_dupes = []

for player_transaction in retro_ids[index:]:
    print(index)
    print(player_transaction["player"])
    index += 1

    if " " not in player_transaction["player"]:

        all_comp_picks = []
        if player_transaction["type"] == "Fg":
            player_comp_picks = PICKS[PICKS["fa_retroid"] == player_transaction["player"]]
            player_comp_picks_year = player_comp_picks[
                player_comp_picks["year"] == int(str(player_transaction["primary_date"])[0:4]) + 1]
            all_comp_picks = player_comp_picks_year["signed_retroid"].tolist()
            if len(all_comp_picks) > 0:
                pass
            else:
                continue

        transac_id = player_transaction["transaction_ID"]
        from_team = player_transaction["from_team"]
        from_franch = player_transaction["from_franchise"]
        to_franchise = player_transaction["to_franchise"]
        transac_date = player_transaction["primary_date"]
        parent = player_transaction["player"]
        to_team = player_transaction["to_team"]
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

        trade_tree = []
        transactions_list = []
        connections = []
        # filters DB for player's trade
        if player_transaction["type"] == "Fg":
            gt(transac_id=transac_id, franch_id=from_franch, parent_retro=parent,
               parent_transaction=transac_id)
            stats = gs(transaction_id=transac_id, franch_choice=from_franch)

            # need to flip the trade stats because of it being a comp pick and the from team is the choice.
            trade_in_stats = stats.get_trade_out_stats()
            trade_totals = stats.get_comp_totals()

            # add comp pick transaction to tree

            tree_node = {"id": 1, "parentId": "", "retro_id": player_transaction["player"],
                         "name": name, "transaction_id": player_transaction["player"],
                         "info": "Compensation picks", "traded_with": {}, "trade_in_stats": trade_in_stats,
                         "trade_out_stats":[], "trade_totals": trade_totals, "date": transac_date}
            trade_tree.append(tree_node)

            # add trade to trans dict for searching
            transaction_info = {"node_id": 1, "parent": player_transaction["player"],
                                "date": transac_date, "from_team": from_team,
                                "from_franchise": from_franch, "retro_id": player_transaction["player"],
                                "traded_for": all_comp_picks}
            transactions_list.append(transaction_info)

        else:
            tree_data = gt(transac_id=transac_id, franch_id=from_franch, parent_retro=parent,
                           parent_transaction=transac_id)
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
            tree_node = {"id": 1, "parentId": "", "retro_id": player_transaction["player"], "name": name,
                         "transaction_id": transac_id, "date": transac_date,
                         "to_team": {"team_id": to_team,
                                     "team_name": format_teams(team=to_team, date=transac_date, to_team=True)},
                         "to_franch": to_franchise, "traded_with": traded_with_players,
                         "trade_in_stats": trade_in_stats, "trade_out_stats": trade_out_stats,
                         "trade_totals": trade_totals}
            trade_tree.append(tree_node)

            # add trade to trans dict for searching
            transaction_details = {"node_id": 1, "parent": player_transaction["player"],
                                   "retro_id": player_transaction["player"], "from_team": from_team,
                                   "from_franchise": from_franch, "to_team": to_team, "to_franch": to_franchise,
                                   "transaction_id": transac_id, "date": transac_date,
                                   "traded_with": traded_with_players,
                                   "traded_for": tree_data.get_traded_for_ids_dict()}
            transactions_list.append(transaction_details)

        # start the search loop
        get_outcome_data(connections=connections, transaction_list=transactions_list, trade_tree=trade_tree,
                         franchise_choice=from_franch, parent_retro=player_transaction["player"],
                         parent_transaction=transac_id)

        #  calculate totals for tree
        tree_totals = get_tree_totals(trade_tree=trade_tree)

        # get WS wins
        ws_wins = get_ws_wins(trade_tree=trade_tree)

        # get parent tree
        parent_trees = pd.read_csv("ParentTrees.csv")
        parent_row = parent_trees[
            (parent_trees["transaction_ID"] == transac_id) & (parent_trees["from_franch"] == from_franch)]
        parent_tree_retro = parent_row["parent_tree_retro"].item()
        parent_tree_transaction_id = parent_row["parent_tree_transaction_id"].item()
        if parent_tree_retro == player_transaction["player"] or \
                parent_tree_transaction_id == player_transaction["transaction_ID"]:
            parent_tree_retro = ""
            parent_tree_transaction_id = ""

        # check if ongoing, check for other stats
        ongoing = "No"
        total_transactions = 0
        traded_for = 0
        traded_away = 0
        earliest = 0
        latest = 0

        for node in trade_tree:
            if "outcome" in node:
                if node["outcome"] == "No further transactions, likely in organization":
                    ongoing = "Yes"

                    # get list of players that are in an ongoing tree to add to their player page
                    if " " in node["retro_id"]:
                        pass
                    else:
                        ongoing_player = node["retro_id"]
                        ongoing_tree_id = ""
                        if parent_tree_retro == "":
                            ongoing_tree_id = f"{player_transaction['player']}_{transac_id}"
                        else:
                            ongoing_tree_id = f"{parent_tree_retro}_{parent_tree_transaction_id}"
                        ongoing_tree_players.append({"retro_id": ongoing_player, "tree": ongoing_tree_id})

            if "transaction_id" in node:
                total_transactions += 1
                traded_for += 1

                if "traded_with" in node:
                    traded_away += len(node["traded_with"]) + 1
                else:
                    traded_away += 1

            if "transaction_id" or "outcome" in node:
                try:
                    date = int(str(node["date"])[0:4])
                    if earliest == 0:
                        earliest = date
                    elif latest == 0:
                        earliest = date

                    if date > latest:
                        latest = date
                    elif date < earliest:
                        earliest = date
                #         pass if never made MLB
                except KeyError:
                    pass
        trade_output = {
            "from_team": {"team_id": from_team, "team_name": format_teams(team=from_team, date=transac_date)},
            "from_franch": from_franch,
            "to_team": {"team_id": to_team, "team_name": format_teams(team=to_team, date=transac_date, to_team=True)},
            "date": transac_date,
            "transac_id": transac_id,
            "tree_id": f"{player_transaction['player']}_{transac_id}",
            "largest_tree_id": f"{parent_tree_retro}_{parent_tree_transaction_id}",
            "total_stats": tree_totals,
            "ws_wins": ws_wins,
            "total_transac": total_transactions,
            "p_traded_away": traded_away,
            "p_traded_for": traded_for,
            "total_players": traded_away + traded_for,
            "y_start": earliest,
            "y_last": latest,
            "year_span": latest - earliest,
            "ongoing": ongoing,
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
                "in_ongoing_trees": [],
                "trades": [trade_output]
            }
            all_data.append(output)

for data in all_data:
    for player in ongoing_tree_players:
        if player["retro_id"] == data["retro_id"]:
            if player["tree"] in data["in_ongoing_trees"]:
                pass
            else:
                data["in_ongoing_trees"].append(player["tree"])

for player in all_data:
    all_trees = []
    for trade in player["trades"]:
        all_trees.append(trade["tree_id"])
    player_search.append({"retro_id": player["retro_id"], "mlb_id": player["mlb_id"], "name": player["name"],
                          "HOF": player["HOF"], "debut_year": player["debut_year"], "last_year": player["last_year"],
                          "trees":all_trees})

    for trade in player["trades"]:
        if trade["largest_tree_id"] == "_":

            tree_transac = trade["tree_id"][9:14]
            total_transac = trade["total_transac"]
            transac_match = False
            if len(all_parent_trees_no_detail_no_dupes) == 0:
                no_details_tree = {key: value for (key, value) in trade.items() if key != "tree_details"}
                all_parent_trees_no_detail_no_dupes.append(no_details_tree)
            else:
                for tree in all_parent_trees_no_detail_no_dupes:
                    if tree_transac == tree["tree_id"][9:14] and total_transac == tree["total_transac"]:
                        transac_match = True
                if transac_match == False:
                    no_details_tree = {key: value for (key, value) in trade.items() if key != "tree_details"}
                    all_parent_trees_no_detail_no_dupes.append(no_details_tree)

            all_parent_trees.append(trade)

# Get non-traded player info
all_retro_ids = PLAYERS["PLAYERID"].to_list()
non_traded_players = []
for player in all_retro_ids:
    match = False
    for check_player in all_data:
        if player == check_player["retro_id"]:
            match = True
            break
    if not match:
        retrosheet_search = gt(retro_id=player, non_trade=True)
        player_retrosheet = retrosheet_search.get_non_traded_data()
        formatted_retrosheet = format_retrosheet(player_retrosheet)

        if len(player_retrosheet) > 0:
            player_name = format_names(retro_id=player)
            player_info = PLAYERS[PLAYERS["PLAYERID"] == player]
            if player_info.empty:
                break
            try:
                mlb_id = int(player_info["key_mlbam"].item())
            except ValueError:
                mlb_id = ""
            hof = player_info["HOF"].item()
            try:
                debut = int(player_info["mlb_played_first"].item())
            except ValueError:
                debut = ""
            end = player_info["mlb_played_last"].item()

            output = {"retro_id": player,
                      "mlb_id": mlb_id,
                      "name": player_name,
                      "HOF": hof,
                      "debut_year": debut,
                      "last_year": end,
                      "retrosheet_data": formatted_retrosheet}
            non_traded_players.append(output)
            player_search.append({"retro_id": player, "mlb_id": mlb_id, "name": player_name,
                                  "HOF": hof, "debut_year": debut,
                                  "last_year": end, "trees": ""})

with open("no_trades.json", "w") as file:
    json.dump(non_traded_players, file)

split = 4000
with open("all_data1.json", "w") as file1:
    json.dump(all_data[:split], file1)
with open("all_data2.json", "w") as file2:
    json.dump(all_data[split:], file2)

with open("all_parent_trees_no_details.json", "w") as file:
    json.dump(all_parent_trees_no_detail_no_dupes, file)

with open("all_parent_trees.json", "w") as file:
    json.dump(all_parent_trees, file)

with open("player_search.json", "w") as file:
    json.dump(player_search, file)
