import pandas as pd
from transaction_wizard import TransactionWizard as tw
from flask import Flask, render_template, url_for, redirect
from flask_jsglue import JSGlue
import random

RANDOMS = pd.read_csv("data/random_ids.csv")
PLAYERS = pd.read_csv("data/players.csv")
TEAMS = pd.read_csv("data/teams.csv")
OUTCOME_KEYS = {"A " : "assigned from one team to another without compensation",
                "C " : "signed to another team on a conditional deal",
                "Cr" : "signed to another team on a conditional deal",
                "D " : "rule 5 draft pick",
                "Dr" : "returned to original team after draft selection",
                "F "  : "free agent signing",
                "Fg" : "became a free agent",
                "Hd"  : "declared ineligible",
                "Hf"  : "demoted to the minor league",
                "Hh"  : "held out",
                "Hm"  : "went into military service",
                "Hs"  : "suspended",
                "Hu"  : "unavailable but not on DL",
                "Hv"  : "voluntarity retired",
                "J " : "jumped teams",
                "L " : "loaned to another team",
                "Mr" : "rights returned when working agreement with minor league team ended",
                "P " : "purchased by another team",
                "R " : "released",
                "T " : "trade",
                "Tn" : "traded but refused to report",
                "U " : "unknown",
                "Vg" : "player assigned to league control",
                "W " : "picked off waivers",
                "Wf" : "first year waiver pick",
                "Wv" : "waiver pick voided",
                "X " : "lost in expansion draft",
                "Z " : "voluntarily retired",
                "Tr" : "returned to original team"
                }


def get_outcome_data(transaction_details, trade_tree, franchise_choice):
    """Takes a dictionary of transactions, and uses the player ID, date and team choice to get a list of outcomes
     for each player"""
    trade_tree = trade_tree

    # sort player's transactions by team choice and date and add 1 row outcome to list
    outcomes = []
    for tdict in transaction_details:
        date = tdict["date"]
        player_list = tdict["traded_for"]

        for player_id in player_list:
            if player_id == "PTBNL/Cash":
                pass
            else:
                player_search = tw(player=player_id)
                all_outcomes = player_search.all_trans[player_search.all_trans["from-franchise"] == franchise_choice]
                outcome = all_outcomes[all_outcomes["primary_date"] > date]

                if len(outcome.index) == 1:
                    outcomes.append(outcome)

                # Choose one if there are multiple transactions from a team- first after date
                if len(outcome.index) > 1:
                    sorted_by_dates = outcome.sort_values(by="primary_date")
                    player_outcomes = sorted_by_dates[sorted_by_dates["primary_date"] > date]

                    outcome = player_outcomes.head(1)
                    if outcome.empty:
                        pass
                    else:
                        outcomes.append(outcome)

                # if player is retired or a newer player, add to the dictionary- dates can be changed for more accuracy
                if outcome.empty:
                    sorted_trans = player_search.all_trans.sort_values(by="primary_date")
                    last_row = sorted_trans.tail(1)
                    last_date = last_row.primary_date.item()
                    if last_date <= 20130000:
                        transaction_info = {}
                        transaction_info["name"] = player_id
                        transaction_info["outcome"] = "No further transactions- likely retired"
                        transaction_info["date"] = last_date
                        trade_tree.append(transaction_info)

                    else:
                        transaction_info = {}
                        transaction_info["name"] = player_id
                        transaction_info["outcome"] = "No further transactions- likely in organization"
                        transaction_info["date"] = last_date
                        trade_tree.append(transaction_info)

    get_player_outcomes(outcomes, trade_tree, franchise_choice)


def get_player_outcomes(outcomes, trade_tree, franchise_choice):
    """Takes the list of outcomes to either find more transactions or end a player's line"""
    trade_tree = trade_tree

    # loop through outcomes- tree line ends or more trades to search and the tree grows
    transactions_list = []
    for outcome in outcomes:
        code = outcome.typeof.item()
        outcome_date = outcome.primary_date.item()
        player_id = outcome.player.item()

        # end line if player was not traded
        if code != "T ":
            transaction_info = {}
            transaction_info["name"] = player_id
            transaction_info["outcome"] = code
            transaction_info["date"] = outcome_date
            trade_tree.append(transaction_info)

        # get new transaction ids to search
        else:
            transaction = {}
            transaction["name"] = player_id
            transaction["id"] = outcome.transaction_id.item()
            transaction["to_team"] = outcome["to-team"].item()
            transaction["to_franchise"] = outcome["to-franchise"].item()
            transaction["date"] = outcome.primary_date.item()

            transactions_list.append(transaction)

    # continue loop if there are more trades
    if len(transactions_list) > 0:
        get_players_by_trans_id(transactions_list, trade_tree, franchise_choice)


def get_players_by_trans_id(transactions_list, trade_tree, franchise_choice):
    """Takes a list of transactions to get more players to search for"""
    trade_tree = trade_tree
    transaction_details = []
    traded_for_list = []

    for trans in transactions_list:
        transaction = tw(trans_id=trans["id"], choice=franchise_choice)
        transaction.get_trades()
        # add new player ids to dict to search
        traded_for = transaction.get_traded_ids_list()

        # in the rare occurrence a player was traded for himself in same transaction- Jeff Terpko- remove that player
        if trans["name"] in traded_for:
            traded_for.remove(trans["name"])

        # add transaction to trade tree and new ids to search on the next loop
        player_id = trans["name"]
        trans_date = trans["date"]
        to_team = trans["to_team"]

        add_to_tree_list = {}
        add_to_tree_list["name"] = player_id
        add_to_tree_list["traded_to"] = to_team
        add_to_tree_list["date"] = trans_date
        add_to_tree_list["traded_for"] = transaction.get_traded_ids_list()
        traded_with = transaction.get_traded_with_ids_list()
        if player_id in traded_with:
            traded_with.remove(player_id)
        add_to_tree_list["traded_with"] = traded_with

        trade_tree.append(add_to_tree_list)

        traded_for_list.append(transaction.get_traded_ids_list())
        transaction_details.append(add_to_tree_list)

    if len(traded_for_list) > 0:
        get_outcome_data(transaction_details=transaction_details, trade_tree=trade_tree,
                         franchise_choice=franchise_choice)


def delete_dupes(trade_tree):
    """Deletes any duplicate transactions or outcomes in the trade tree,
    if players were involved in the same transactions"""
    new_tree = [transaction for n, transaction in enumerate(trade_tree) if transaction not in trade_tree[n + 1:]]
    return new_tree


def format_tree(trade_tree):
    """Changes all abbreviations to full text"""
    # change all player_ids to name
    formatted_tree = []
    for trans_dict in trade_tree:

        player_name = ""
        traded_for = []
        traded_with = []
        team_name = ""
        outcome_text = ""
        date = ""

        # format player names
        if " " in trans_dict["name"]:
            player_name = trans_dict["name"]
        else:
            row_with_name = PLAYERS[PLAYERS.ID == trans_dict["name"]]
            player_name = f"{row_with_name.First.item()} {row_with_name.Last.item()}"

        # format traded_for names
        if "traded_for" in trans_dict:
            for player_received in trans_dict["traded_for"]:
                if player_received == "PTBNL/Cash":
                    player_traded = player_received
                elif " " in player_received:
                    player_traded = player_received
                else:
                    try:
                        row_with_name = PLAYERS[PLAYERS.ID == player_received]
                        player_traded = f"{row_with_name.First.item()} {row_with_name.Last.item()}"
                    except ValueError:
                        player_traded = player_received
                traded_for.append(player_traded)

        # change traded_with names
        if "traded_with" in trans_dict:
            for player_with in trans_dict["traded_with"]:
                if player_with == "PTBNL/Cash":
                    player_traded_with = player_with
                elif " " in player_with:
                    player_traded_with = player_with
                else:
                    try:
                        row_with_name = PLAYERS[PLAYERS.ID == player_with]
                        player_traded_with = f"{row_with_name.First.item()} {row_with_name.Last.item()}"
                    except ValueError:
                        player_traded_with = player_with
                traded_with.append(player_traded_with)


        # format traded_to team
        if "traded_to" in trans_dict:
            team_code = trans_dict["traded_to"]
            teamrow = TEAMS[TEAMS.TeamID == team_code]
            try:
                team_name = teamrow.CityName.item()
            except ValueError:
                team_name = trans_dict["traded_to"]

        # format outcomes
        if "outcome" in trans_dict:
            outcome_code = trans_dict["outcome"]
            if outcome_code in OUTCOME_KEYS:
                outcome_text = OUTCOME_KEYS[outcome_code]
            else:
                outcome_text = outcome_code

        # format date
        if "date" in trans_dict:
            yyyymmdd = str(trans_dict["date"])
            y = yyyymmdd[0:4]
            m = yyyymmdd[4:6]
            d = yyyymmdd[6:8]
            date = f"{y}-{m}-{d}"

        # create new dictionary with formatted values:
        if len(traded_with) > 0:
            formatted_trans = {}
            formatted_trans["name"] = player_name
            formatted_trans["traded_for"] = traded_for
            formatted_trans["traded_with"] = traded_with
            formatted_trans["traded_to"] = team_name
            formatted_trans["date"] = date
            formatted_tree.append(formatted_trans)
        elif outcome_text == "":
            formatted_trans = {}
            formatted_trans["name"] = player_name
            formatted_trans["traded_for"] = traded_for
            formatted_trans["traded_to"] = team_name
            formatted_trans["date"] = date
            formatted_tree.append(formatted_trans)
        else:
            formatted_trans = {}
            formatted_trans["name"] = player_name
            formatted_trans["outcome"] = outcome_text
            formatted_trans["date"] = date
            formatted_tree.append(formatted_trans)

    return formatted_tree


def check_for_double_names(formatted_tree):
    """If players are involved multiple times in one tree, the names to be adjusted to display in the OrgChart"""

    #  check if a player is in a traded for list, if so then change the traded for name and the next name match found
    maxlen = len(formatted_tree) - 1
    n = 0
    s = 1
    while n <= maxlen:
        name = ""
        for transac in formatted_tree[n:s]:
            name = transac["name"]
        count = n + 1
        for tdict in formatted_tree[n + 1:]:
            count += 1

            if "traded_for" in tdict:
                for player_n in tdict["traded_for"]:
                    match = False

                    if player_n == name:
                        tdict["traded_for"].remove(player_n)
                        tdict["traded_for"].append(f"{name} ")
                        match = True

                    while match:
                        for trdict in formatted_tree[count:]:

                            if "outcome" in trdict and trdict["name"] == name:
                                trdict["name"] = f"{name} "
                                match = False
                            elif "traded_for" in trdict and trdict["name"] == name:
                                trdict["name"] = f"{name} "
                                match = False
                            else:
                                match = False
        n += 1
        s += 1

    # if there is a player in a traded for then in another traded for before he is in name-->
    maxlen = len(formatted_tree) - 1
    n = 0
    s = 1
    while n <= maxlen:
        for transac in formatted_tree[n:]:

            if "traded_for" in transac:
                for pl in transac["traded_for"]:
                    name = pl
                    count = (n + 1)
                    times_matched = 0
                    for tdict in formatted_tree[n + 1:]:
                        count += 1
                        s += 1

                        if "traded_for" in tdict:
                            for player_n in tdict["traded_for"]:
                                match = False

                                if player_n == name:
                                    tdict["traded_for"].remove(player_n)
                                    tdict["traded_for"].append(f"{name} ")
                                    match = True

                                while match:
                                    for trdict in formatted_tree[count:s]:

                                        if trdict["name"] == name:
                                            times_matched += 1
                                        if times_matched == 2:
                                            trdict["name"] = f"{name} "
                                            match = False
                                            break
                                        else:
                                            match = False
            n += 1
            s += 1

    return formatted_tree


def format_for_google_chart(formatted_tree):
    """Changes the trade tree to display properly as a Google Orgchart"""

    tree = []
    for transaction in formatted_tree[0:1]:
        # add first node to tree
        if "traded_with" in transaction:
            traded_with = ', '.join(transaction["traded_with"])
            style_dict = {}
            style_dict["v"] = transaction["name"]
            style_dict["f"] = f"{transaction['name']}<br> <div style= 'color:CadetBlue; font-style:italic; font-size:small;'> " \
                              f"With: {traded_with}</div><div style='color:deepskyblue; font-style:italic; font-size:small;'>" \
                              f"To: {transaction['traded_to']}<br>{transaction['date']}</div>"
            tree.append([style_dict, transaction["name"], ""])
        else:
            style_dict = {}
            style_dict["v"] = transaction["name"]
            style_dict[
                "f"] = f"{transaction['name']}<div style='color:deepskyblue; font-style:italic; " \
                       f"font-size:small;'>To: {transaction['traded_to']}<br>" \
                       f"{transaction['date']}</div>"
            tree.append([style_dict, transaction["name"], ""])

        if "PTBNL/Cash" in transaction["traded_for"]:
            style_dict = {}
            style_dict["v"] = f"PTBNL/Cash"
            style_dict["f"] = "PTBNL/Cash<div style='color:Crimson; " \
                              f"font-style:italic'>From: {transaction['traded_to']}" \
                              f"<br>{transaction['date']}</div>"
            tree.append([style_dict, transaction["name"], ""])

    outcome_data = []
    trades_data = []
    outcome_names = []
    for transaction in formatted_tree[1:]:
        if "outcome" in transaction:
            # pass and keep info, and make node when found in traded_for
            outcome_data.append(transaction)
            outcome_names.append(transaction["name"])
        if "traded_for" in transaction:
            # add transaction to dict of trades
            trades_data.append(transaction)

    for transaction in formatted_tree:
        if "traded_for" in transaction:
            for player_traded_for in transaction["traded_for"]:

                if player_traded_for in outcome_names:
                    for transaction_data in outcome_data:

                        if transaction_data["name"] == player_traded_for:
                            style_dict = {}
                            style_dict["v"] = player_traded_for
                            style_dict["f"] = f"{player_traded_for}<div style='color:Crimson; " \
                                              f"font-style:italic'>{transaction_data['outcome']}" \
                                              f"<br>{transaction_data['date']}</div>"
                            tree.append([style_dict, transaction["name"], ""])

                            outcome_data.remove(transaction_data)
                            outcome_names.remove(player_traded_for)

    cash = 0
    for trade in trades_data:
        # change cash nodes so they show up in different transactions
        if "PTBNL/Cash" in trade["traded_for"]:
            cash += 1
            style_dict = {}
            style_dict["v"] = f"PTBNL/Cash{cash}"
            style_dict["f"] = "PTBNL/Cash<div style='color:Crimson; " \
                              f"font-style:italic'>From: {trade['traded_to']}" \
                              f"<br>{trade['date']}</div>"
            tree.append([style_dict, trade["name"], ""])

        if "traded_with" in trade:
            parent = ""
            while parent == "":
                for transaction in formatted_tree:
                    if "traded_for" in transaction:
                        for player_traded_for in transaction["traded_for"]:
                            if player_traded_for == trade["name"]:
                                parent = transaction["name"]
            traded_with = ', '.join(trade["traded_with"])

            style_dict = {}
            style_dict["v"] = trade["name"]
            style_dict["f"] = f"{trade['name']}<br> <div style= 'color:CadetBlue; font-style:italic; font-size:small;'> " \
                              f"With: {traded_with}</div><div style='color:deepskyblue; font-style:italic; font-size:small;'>" \
                              f"To: {trade['traded_to']}<br>{trade['date']}</div>"
            tree.append([style_dict, parent, ""])

        else:
            parent = ""
            while parent == "":
                for transaction in formatted_tree:
                    if "traded_for" in transaction:
                        for player_traded_for in transaction["traded_for"]:
                            if player_traded_for == trade["name"]:
                                parent = transaction["name"]
            style_dict = {}
            style_dict["v"] = trade["name"]
            style_dict["f"] = f"{trade['name']}<div style='color:deepskyblue; font-style:italic; " \
                              f"font-size:small;'>To: {trade['traded_to']}<br>" \
                              f"{trade['date']}</div>"
            tree.append([style_dict, parent, ""])
    return tree


app = Flask(__name__)
jsglue = JSGlue(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/random')
def random():
    random_row = RANDOMS.sample(1)
    random_id = random_row.player_id.item()
    return redirect(url_for(".player", users_player_id=random_id))


@app.route('/player/<users_player_id>')
def player(users_player_id):
    # searches for player's trades in DB
    trade_data = tw(player=users_player_id)
    trade_data.get_trades()
    trades = trade_data.trades

    all_trade_trees = []
    # goes through each trade to make a tree
    for index, row in trades.iterrows():
        trans_id = row["transaction_id"]
        team_choice = row["from-team"]
        franchise_choice = row["from-franchise"]
        first_date = row["primary_date"]
        parent = row["player"]
        to_team = row["to-team"]

        trade_tree = []
        # search DB for player's trade
        tree_data = tw(trans_id=trans_id, choice=franchise_choice)
        tree_data.get_trades()
        with_list = tree_data.get_traded_with_ids_list()
        if users_player_id in with_list:
            with_list.remove(users_player_id)

        transaction_list = []
        # save initial trade to tree
        transaction_info = {}
        transaction_info["name"] = parent
        transaction_info["traded_to"] = to_team
        transaction_info["date"]= first_date
        transaction_info["traded_for"]= tree_data.get_traded_ids_list()
        transaction_info["traded_with"]= with_list
        trade_tree.append(transaction_info)
        # add trade to trans dict for searching
        transaction_list.append(transaction_info)

        # start the search loop
        get_outcome_data(transaction_details=transaction_list, trade_tree=trade_tree, franchise_choice=franchise_choice)

        # delete any duplicate transaction entries
        trade_tree = delete_dupes(trade_tree=trade_tree)

        # format the trade tree to full text
        formatted_tree_with_doubles = format_tree(trade_tree=trade_tree)

        # edit players that appear multiple times in a tree so they display properly in the orgchart
        formatted_tree = check_for_double_names(formatted_tree=formatted_tree_with_doubles)

        # formatting for google orgchart
        org_tree = format_for_google_chart(formatted_tree=formatted_tree)

        # check if player was traded many times from one team- yet to come across a player being traded 3x from one team
        for team_tree in all_trade_trees:
            for k, v in team_tree.items():
                if team_choice == k:
                    team_choice = f"{team_choice}2"

        tree_with_team_name = {}
        tree_with_team_name[team_choice] = org_tree
        all_trade_trees.append(tree_with_team_name)

    # get name of player to add to his page
    row_with_name = PLAYERS[PLAYERS.ID == users_player_id]
    player_name = f"{row_with_name.First.item()} {row_with_name.Last.item()}"

    if len(all_trade_trees) > 0:
        return render_template("player_page.html", trees=all_trade_trees, name=player_name)
    else:
        return render_template("player_not_traded.html", name=player_name)


@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run()
