import pandas as pd
from transaction_wizard import TransactionWizard as tw
from stats_wizard import StatsWizard as sw

ALL_TRADED_PLAYERS = pd.read_csv("../traded_players_2022.csv")
PLAYERS = pd.read_csv("../Players2022.csv")
PICKS = pd.read_csv("../comp_picks_retroid.csv")
TEAMS = pd.read_csv("../teams.csv")
OUTCOME_KEYS = {"A ": "assigned from one team to another without compensation",
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


def get_outcome_data(transaction_details, trade_tree, franchise_choice):
    """Takes a dictionary of transactions, and uses the player ID, date and team choice to get a list of outcomes
     for each player"""
    trade_tree = trade_tree

    # sort player's transactions by team choice and date and add 1 row outcome to list
    outcomes = []
    for tdict in transaction_details:
        date = tdict["date"]
        transaction_id = tdict["transaction_id"]
        player_list = tdict["traded_for"]

        for player_id in player_list:
            if player_id == "PTBNL/Cash":
                pass
            else:
                player_search = tw(player=player_id)
                # check if a player was re signed
                sorted = player_search.all_trans.sort_values(["primary_date"], ascending=True)

                sorted["typeof_next_row"] = sorted["typeof"].shift(-1)
                sorted["to-franchise_next_row"] = sorted["to-franchise"].shift(-1)
                resigned1 = sorted[(sorted["typeof"] == "Fg") & (sorted["typeof_next_row"] == "R ") &
                                   (sorted["to-franchise_next_row"] == sorted["from-franchise"])]
                resigned2 = sorted[(sorted["typeof"] == "Fg") & (sorted["typeof_next_row"] == "F ") &
                                   (sorted["to-franchise_next_row"] == sorted["from-franchise"])]

                no_released = pd.concat([sorted, resigned1, resigned2]).drop_duplicates(keep=False)
                all_outcomes = no_released[no_released["from-franchise"] == franchise_choice]
                outcome = all_outcomes[
                    (all_outcomes["primary_date"] >= date) & (all_outcomes["transaction_id"] != transaction_id)]

                if len(outcome.index) == 1:
                    outcomes.append(outcome)

                # Choose one if there are multiple transactions from a team- first after date
                elif len(outcome.index) > 1:
                    sorted_by_dates = outcome.sort_values(by="primary_date")
                    player_outcomes = sorted_by_dates[sorted_by_dates["primary_date"] >= date]

                    outcome = player_outcomes.head(1)
                    if outcome.empty:
                        pass
                    else:
                        outcomes.append(outcome)

                # if player is retired or a newer player, add to the dictionary- dates can be changed for more accuracy
                elif outcome.empty:
                    sorted_trans = player_search.all_trans.sort_values(by="primary_date")
                    to_choice = sorted_trans[sorted["to-franchise"] == franchise_choice]

                    if to_choice.empty and " " in player_id:
                        transaction_info = {}
                        transaction_info["name"] = player_id
                        transaction_info["retro_id"] = player_id
                        transaction_info["outcome"] = "Did not play in MLB"
                        transaction_info["date"] = date
                        trade_tree.append(transaction_info)

                    else:
                        last_row = sorted_trans.tail(1)
                        last_date = last_row.primary_date.item()
                        if last_date <= 20130000:
                            transaction_info = {}
                            transaction_info["name"] = player_id
                            transaction_info["retro_id"] = player_id
                            transaction_info["outcome"] = "No further transactions- likely retired"
                            transaction_info["date"] = last_date
                            trade_tree.append(transaction_info)

                        else:
                            transaction_info = {}
                            transaction_info["name"] = player_id
                            transaction_info["retro_id"] = player_id
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
        year = int(str(outcome_date)[0:4]) + 1
        player_id = outcome.player.item()

        # end line if player was not traded
        if code == "Fg":
            player_comp_picks = PICKS[PICKS["fa_retroid"] == player_id]
            player_comp_picks_year = player_comp_picks[player_comp_picks["year"] == year]
            all_comp_picks = player_comp_picks_year["signed_retroid"].tolist()
            if len(all_comp_picks) > 0:
                comp_picks_dict = {}
                for id in all_comp_picks:
                    comp_picks_dict[id] = id

                transaction = {}
                transaction["name"] = player_id
                transaction["transaction_id"] = "Compensation Picks"
                transaction["signed"] = comp_picks_dict
                transaction["date"] = outcome.primary_date.item()

                transactions_list.append(transaction)

            else:
                transaction_info = {}
                transaction_info["name"] = player_id
                transaction_info["retro_id"] = player_id
                transaction_info["outcome"] = code
                transaction_info["date"] = outcome_date
                trade_tree.append(transaction_info)


        elif code != "T ":
            transaction_info = {}
            transaction_info["name"] = player_id
            transaction_info["retro_id"] = player_id
            transaction_info["outcome"] = code
            transaction_info["date"] = outcome_date
            trade_tree.append(transaction_info)

        # get new transaction ids to search
        else:
            transaction = {}
            transaction["name"] = player_id
            transaction["transaction_id"] = outcome.transaction_id.item()
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
        if trans["transaction_id"] == "Compensation Picks":
            # add picks to trade tree and new ids to search on the next loop
            player_id = trans["name"]
            transaction_id = trans["transaction_id"]
            signed = trans["signed"]
            trans_date = trans["date"]

            add_to_tree_list = {}
            add_to_tree_list["name"] = player_id
            add_to_tree_list["retro_id"] = player_id
            add_to_tree_list["transaction_id"] = transaction_id
            add_to_tree_list["date"] = trans_date
            add_to_tree_list["traded_for"] = signed

            traded_for_list.append(signed)

            trade_tree.append(add_to_tree_list)
            transaction_details.append(add_to_tree_list)

        else:
            transaction = tw(trans_id=trans["transaction_id"], choice=franchise_choice)
            transaction.get_trades()
            # add new player ids to dict to search
            traded_for = transaction.get_traded_ids_dict()

            # in the rare occurrence a player was traded for himself in same transaction- Jeff Terpko- remove that player
            if trans["name"] in traded_for:
                traded_for.pop(trans["name"])

            # add transaction to trade tree and new ids to search on the next loop
            player_id = trans["name"]
            transaction_id = trans["transaction_id"]
            trans_date = trans["date"]
            to_team = trans["to_team"]
            to_franchise = trans["to_franchise"]

            add_to_tree_list = {}
            add_to_tree_list["name"] = player_id
            add_to_tree_list["retro_id"] = player_id
            add_to_tree_list["transaction_id"] = transaction_id
            add_to_tree_list["traded_to_id"] = to_team
            add_to_tree_list["traded_to"] = to_team
            add_to_tree_list["traded_to_franchise"] = to_franchise
            add_to_tree_list["date"] = trans_date
            add_to_tree_list["traded_for"] = transaction.get_traded_ids_dict()
            traded_with = transaction.get_traded_with_ids_dict()
            if player_id in traded_with:
                traded_with.pop(player_id)
            add_to_tree_list["traded_with"] = traded_with

            trade_tree.append(add_to_tree_list)

            traded_for_list.append(transaction.get_traded_ids_dict())
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
    for trans_dict in trade_tree[0:1]:
        team_code = trans_dict["choice_team_id"]
        teamrow = TEAMS[TEAMS.TeamID == team_code]
        try:
            trans_dict["choice_team"] = teamrow.CityName.item()
        except ValueError:
            pass

    for trans_dict in trade_tree:
        # format player names
        if "name" in trans_dict:
            if " " in trans_dict["name"]:
                pass
            else:
                try:
                    row_with_name = PLAYERS[PLAYERS.ID == trans_dict["name"]]
                    trans_dict["name"] = f"{row_with_name.nickname.item()} {row_with_name.Last.item()}"
                except ValueError:
                    pass

        # format traded_for names
        if "traded_for" in trans_dict:
            for id, name in trans_dict["traded_for"].items():
                if id == "PTBNL/Cash":
                    pass
                elif " " in id:
                    pass
                else:
                    try:
                        row_with_name = PLAYERS[PLAYERS.ID == id]
                        trans_dict["traded_for"][id] = f"{row_with_name.nickname.item()} {row_with_name.Last.item()}"
                    except ValueError:
                        pass

        # change traded_with names
        if "traded_with" in trans_dict:
            if len(trans_dict["traded_with"]) > 0:
                for id, player in trans_dict["traded_with"].items():
                    if id == "PTBNL/Cash":
                        pass
                    elif " " in id:
                        pass
                    else:
                        try:
                            row_with_name = PLAYERS[PLAYERS.ID == id]
                            trans_dict["traded_with"][
                                id] = f"{row_with_name.nickname.item()} {row_with_name.Last.item()}"
                        except ValueError:
                            pass
            else:
                trans_dict.pop("traded_with")

        # format traded_to team
        if "traded_to" in trans_dict:
            team_code = trans_dict["traded_to"]
            teamrow = TEAMS[TEAMS.TeamID == team_code]
            try:
                trans_dict["traded_to"] = teamrow.CityName.item()
            except ValueError:
                pass

        # format outcomes
        if "outcome" in trans_dict:
            outcome_code = trans_dict["outcome"]
            if outcome_code in OUTCOME_KEYS:
                trans_dict["outcome"] = OUTCOME_KEYS[outcome_code]
            else:
                pass

        # format date
        if "date" in trans_dict:
            yyyymmdd = str(trans_dict["date"])
            y = yyyymmdd[0:4]
            m = yyyymmdd[4:6]
            d = yyyymmdd[6:8]
            trans_dict["date"] = f"{y}-{m}-{d}"
    return trade_tree


def calculate_stats(trade_tree):
    """gets the WAR for every player involved in the trade"""
    trade_tree = trade_tree
    choice_team = trade_tree[0]["choice_team_id"]
    choice_franchise = trade_tree[0]["choice_franchise"]
    for trans in trade_tree:
        stats_start_date = int(str(trans["date"])[0:4])

        WAR_out = 0
        G_out = 0
        PA_out = 0
        IP_out = 0
        salary_out = 0
        all_player_stats = {}
        trade_stats = {}
        if "outcome" not in trans:
            if trans["transaction_id"] != "Compensation Picks":
                traded_to_franchise = trans["traded_to_franchise"]
                retro_id = trans["retro_id"]
                name = trans["name"]
                player_stats = sw(retro_id, stats_start_date, from_franchise=choice_franchise,
                                  to_franchise=traded_to_franchise)
                player_stats.get_stats()
                player_stats.get_salary_from()

                WAR_out += player_stats.WAR_on_team
                G_out += player_stats.G_on_team
                PA_out += player_stats.PA_on_team
                IP_out += player_stats.IPouts_on_team
                salary_out += player_stats.trade_year_salary

                player_stats = {"id": retro_id, "name": name, "stats": {"WAR out": player_stats.WAR_on_team,
                                                                        "G out": player_stats.G_on_team,
                                                                        "PA out": player_stats.PA_on_team,
                                                                        "IP out": player_stats.IPouts_on_team,
                                                                        "salary out": salary_out}}
                all_player_stats[retro_id] = player_stats
                if "traded_with" in trans and len("traded_with") > 0:
                    for id, name in trans["traded_with"].items():
                        if id == "PTBNL/Cash":
                            pass
                        else:
                            retro_id = id
                            name = name
                            player_stats = sw(retro_id, stats_start_date, from_franchise=choice_franchise,
                                              to_franchise=traded_to_franchise)
                            player_stats.get_stats()
                            player_stats.get_salary_from()
                            WAR_out += player_stats.WAR_on_team
                            G_out += player_stats.G_on_team
                            PA_out += player_stats.PA_on_team
                            IP_out += player_stats.IPouts_on_team
                            salary_out += player_stats.trade_year_salary

                            stats = {"id": retro_id, "name": name, "stats": {"WAR out": player_stats.WAR_on_team,
                                                                             "G out": player_stats.G_on_team,
                                                                             "PA out": player_stats.PA_on_team,
                                                                             "IP out": player_stats.IPouts_on_team},
                                     "salary out": salary_out}
                            all_player_stats[id] = stats

                trans["player_stats"] = all_player_stats
                trans["trade_stats"] = trade_stats

            WAR_in = 0
            G_in = 0
            PA_in = 0
            IP_in = 0
            salary_in = 0
            trade_stats = {}
            if "traded_for" in trans:
                for id, name in trans["traded_for"].items():
                    if id == "PTBNL/Cash":
                        pass
                        continue
                    retro_id = id
                    stats_end_date = 0
                    for transac in trade_tree[1:]:
                        if retro_id == transac["retro_id"]:
                            stats_end_date = int(str(transac["date"])[0:4])
                    player_stats = sw(retro_id, stats_start_date, to_franchise=choice_franchise,
                                      from_franchise=None, stats_end_date=stats_end_date)
                    player_stats.get_stats()
                    player_stats.get_salary_to()
                    WAR_in += player_stats.WAR_on_team
                    G_in += player_stats.G_on_team
                    PA_in += player_stats.PA_on_team
                    IP_in += player_stats.IPouts_on_team
                    salary_in += player_stats.trade_year_salary
                    stats = {"id": retro_id, "name": name, "stats": {"WAR in": player_stats.WAR_on_team,
                                                                     "G in": player_stats.G_on_team,
                                                                     "PA in": player_stats.PA_on_team,
                                                                     "IP in": player_stats.IPouts_on_team,
                                                                     "Salary in": salary_in}}
                    all_player_stats[id] = stats
                    trans["player_stats"] = all_player_stats

            # calculate total for transaction
            trade_stats["WAR out"] = round(WAR_out, 2)
            trade_stats["WAR in"] = round(WAR_in, 2)
            trade_stats["WAR value"] = round(WAR_in - WAR_out, 2)
            trade_stats["G out"] = round(G_out, 2)
            trade_stats["G in"] = round(G_in, 2)
            trade_stats["G value"] = round(G_in - G_out, 2)
            trade_stats["PA out"] = round(PA_out, 2)
            trade_stats["PA in"] = round(PA_in, 2)
            trade_stats["PA value"] = round(PA_in - PA_out, 2)
            trade_stats["IP out"] = round(IP_out, 2)
            trade_stats["IP in"] = round(IP_in, 2)
            trade_stats["IP value"] = round(IP_in - IP_out, 2)
            trade_stats["Salary out"] = round(salary_out, 2)
            trade_stats["Salary in"] = round(salary_in, 2)
            trade_stats["Salary value"] = round(salary_in - salary_out, 2)

            trans["trade_stats"] = trade_stats

    return trade_tree


def get_whole_tree_value(trade_tree):
    # calculate totals for entire tree
    WAR_out = 0
    WAR_in = 0
    G_out = 0
    G_in = 0
    PA_out = 0
    PA_in = 0
    IP_out = 0
    IP_in = 0
    salary_in = 0
    salary_out = 0
    for trans in trade_tree:
        if "trade_stats" in trans:
            WAR_out += trans["trade_stats"]["WAR out"]
            WAR_in += trans["trade_stats"]["WAR in"]
            G_out += trans["trade_stats"]["G out"]
            G_in += trans["trade_stats"]["G in"]
            PA_out += trans["trade_stats"]["PA out"]
            PA_in += trans["trade_stats"]["PA in"]
            IP_out += trans["trade_stats"]["IP out"]
            IP_in += trans["trade_stats"]["IP in"]
            salary_out += trans["trade_stats"]["Salary out"]
            salary_in += trans["trade_stats"]["Salary in"]

    WAR_value = round(WAR_in - WAR_out, 2)
    G_value = round(G_in - G_out, 2)
    PA_value = round(PA_in - PA_out, 2)
    IP_value = round(IP_in - IP_out, 2)
    salary_value = round(salary_in - salary_out, 2)

    totals = {"WAR": {}, "G": {}, "PA": {}, "IP": {}, "Salary": {}}
    totals["WAR"]["total_WAR_out"] = round(WAR_out, 2)
    totals["WAR"]["total_WAR_in"] = round(WAR_in, 2)
    totals["WAR"]["WAR_total"] = WAR_value
    if WAR_value > 0:
        totals["WAR"]["value"] = "pos"
    else:
        totals["WAR"]["value"] = "neg"

    totals["G"]["total_G_out"] = round(G_out, 2)
    totals["G"]["total_G_in"] = round(G_in, 2)
    totals["G"]["G_total"] = round(G_value, 2)
    if G_value > 0:
        totals["G"]["value"] = "pos"
    else:
        totals["G"]["value"] = "neg"

    totals["PA"]["total_PA_out"] = int(PA_out)
    totals["PA"]["total_PA_in"] = int(PA_in)
    totals["PA"]["PA_total"] = int(PA_value)
    if PA_value > 0:
        totals["PA"]["value"] = "pos"
    else:
        totals["PA"]["value"] = "neg"

    totals["IP"]["total_IP_out"] = round(IP_out, 2)
    totals["IP"]["total_IP_in"] = round(IP_in, 2)
    totals["IP"]["IP_total"] = round(IP_value, 2)
    if IP_value > 0:
        totals["IP"]["value"] = "pos"
    else:
        totals["IP"]["value"] = "neg"

    totals["Salary"]["total_salary_out"] = round(salary_out, 2)
    totals["Salary"]["salary_out_cash"] = "${:,.2f}".format(totals["Salary"]["total_salary_out"])
    totals["Salary"]["total_salary_in"] = round(salary_in, 2)
    totals["Salary"]["salary_in_cash"] = "${:,.2f}".format(totals["Salary"]["total_salary_in"])
    totals["Salary"]["salary_total"] = round(salary_value, 2)
    totals["Salary"]["salary_total_cash"] = "${:,.2f}".format(totals["Salary"]["salary_total"])
    if IP_value > 0:
        totals["IP"]["value"] = "neg"
    else:
        totals["IP"]["value"] = "pos"

    return totals


trades = pd.read_csv("to_generate.csv")
all_trades = trades["trans_id"].tolist()

all_data = []
done = 5000
for player in all_trades[5000:]:
    # searches for player's trades in DB
    trade_data = tw(player=player)
    trade_data.get_trades()
    trades = trade_data.trades

    # goes through each trade to make a tree
    for index, row in trades.iterrows():
        player_output = {}
        trans_id = row["transaction_id"]
        team_choice = row["from-team"]
        franchise_choice = row["from-franchise"]
        first_date = row["primary_date"]
        parent = row["player"]
        to_team = row["to-team"]
        to_franchise = row["to-franchise"]

        trade_tree = []
        # search DB for player's trade
        tree_data = tw(trans_id=trans_id, choice=franchise_choice)
        tree_data.get_trades()
        with_dict = tree_data.get_traded_with_ids_dict()
        if player in with_dict:
            with_dict.pop(player)

        transaction_list = []
        # save initial trade to tree
        transaction_info = {}
        transaction_info["choice_team_id"] = team_choice
        transaction_info["choice_team"] = team_choice
        transaction_info["choice_franchise"] = franchise_choice
        transaction_info["name"] = parent
        transaction_info["retro_id"] = parent
        transaction_info["traded_to_id"] = to_team
        transaction_info["traded_to"] = to_team
        transaction_info["traded_to_franchise"] = to_franchise
        transaction_info["transaction_id"] = trans_id
        transaction_info["date"] = first_date
        transaction_info["traded_for"] = tree_data.get_traded_ids_dict()
        transaction_info["traded_with"] = with_dict
        trade_tree.append(transaction_info)
        # add trade to trans dict for searching
        transaction_list.append(transaction_info)

        # start the search loop
        get_outcome_data(transaction_details=transaction_list, trade_tree=trade_tree, franchise_choice=franchise_choice)

        # delete any duplicate transaction entries
        no_dupes_trade_tree = delete_dupes(trade_tree=trade_tree)

        # format the trade tree to full text
        formatted_tree = format_tree(trade_tree=no_dupes_trade_tree)

        # Stats for each trade
        tree_with_stats = calculate_stats(trade_tree=formatted_tree)
        # Stats total for entire tree
        total_tree_value = get_whole_tree_value(trade_tree=tree_with_stats)

        # get the full name of choice team to display
        team_name = formatted_tree[0]["choice_team"]

        # get name of player to add to his page
        player_name = formatted_tree[0]["name"]

        player_output["name"] = player_name
        player_output["id"] = parent
        player_output["trades"] = formatted_tree
        player_output["tree_value"] = total_tree_value

        total_transactions = 0
        traded_for = 0
        traded_away = 0
        earliest = 0
        latest = 0
        comp_picks = 0
        ongoing = "No"

        for trade in player_output["trades"]:
            if "transaction_id" in trade:
                total_transactions += 1
                traded_for += len(trade["traded_for"])

                if "traded_with" in trade:
                    traded_away += len(trade["traded_with"]) + 1
                else:
                    traded_away += 1

                if trade["transaction_id"] == "Compensation Picks":
                    comp_picks += len(trade["traded_for"])

            if "transaction_id" or "outcome" in trade:
                date = int(trade["date"][0:4])
                if earliest == 0:
                    earliest = date
                elif latest == 0:
                    earliest = date

                if date > latest:
                    latest = date
                elif date < earliest:
                    earliest = date

            if "outcome" in trade:
                if trade["outcome"] == "No further transactions- likely in organization":
                    ongoing = "Yes"
                    print(player_output["id"])
                    print(ongoing)

        tree_csv = {"Player ID": player_output["id"],
                    "Link": f"<a href=/player/{player_output['id']}>{player_output['id']}</a>",
                    "Name": player_output["name"],
                    "From-Team": player_output["trades"][0]["choice_team"],
                    "From-Franchise":player_output["trades"][0]["choice_franchise"],
                    "# Transactions": total_transactions,
                    "# Players Traded Away": traded_away,
                    "# Players Traded For": traded_for,
                    "# Players Total": traded_away + traded_for,
                    "First Year": earliest, "Last Year": latest, "Year Span": latest - earliest, "Ongoing": ongoing,
                    "Comp Picks": comp_picks}

        stats1 = player_output["tree_value"]["WAR"]
        stats2 = player_output["tree_value"]["G"]
        stats3 = player_output["tree_value"]["PA"]
        stats4 = player_output["tree_value"]["IP"]
        stats5 = player_output["tree_value"]["Salary"]

        df1 = pd.DataFrame(tree_csv, index=[0])
        df2 = pd.DataFrame(stats1, index=[0])
        df3 = pd.DataFrame(stats2, index=[0])
        df4 = pd.DataFrame(stats3, index=[0])
        df5 = pd.DataFrame(stats4, index=[0])
        df6 = pd.DataFrame(stats5, index=[0])
        result = pd.concat([df1, df2, df3, df4, df5, df6], axis=1)
        all_data.append(result)
    print(done)
    done +=1

all_trees = pd.concat(all_data, ignore_index=True)
# 0:5000
# all_trees.to_csv("test1.csv", index=False)
# 5000:
all_trees.to_csv("test2.csv", index=False)

df1 = pd.read_csv("test1.csv")
df2 = pd.read_csv("test2.csv")

tree_info = pd.concat([df1, df2])
tree_info = tree_info[["Link","Name","From-Team","From-Franchise","# Transactions","# Players Traded Away",
                       "# Players Traded For","# Players Total","First Year","Last Year","Year Span","Ongoing",
                       "Comp Picks","total_WAR_out","total_WAR_in","WAR_total","total_G_out","total_G_in",
                       "G_total","total_PA_out","total_PA_in","PA_total","total_IP_out","total_IP_in","IP_total",
                       "total_salary_out","total_salary_in","salary_total"]]

tree_info.to_csv("all_tree_info.csv", index=False)




