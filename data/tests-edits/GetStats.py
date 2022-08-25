import pandas as pd
transactions = pd.read_json("stats_transactions_25082022.json")


class GetStats:

    def __init__(self, transaction_id, franch_choice):
        self.transaction_id = transaction_id
        self.franc_choice = franch_choice
        self.transaction = None
        self.trade_out_stats = None
        self.trade_in_stats = None
        self.transaction_total = None
        self.get_transaction()

    def get_transaction(self):
        self.transaction = transactions[transactions["transaction_ID"] == self.transaction_id]

    def get_trade_out_stats(self):
        trade_out = self.transaction[self.transaction["from_franchise"] == self.franc_choice]
        if trade_out.empty:
            return []
        else:
            self.trade_out_stats = trade_out["stats"].tolist()
            return self.trade_out_stats

    def get_trade_in_stats(self):
        trade_in = self.transaction[self.transaction["to_franchise"] == self.franc_choice]
        self.trade_in_stats = trade_in["stats"].tolist()
        return self.trade_in_stats

    def get_trade_totals(self):
        self.transaction_total = {"batting_stats":{ "G":0, "AB":0, "R":0, "H":0, "2B":0, "3B":0, "HR":0, "RBI":0, "SB":0,
                                               "BB":0, "SO":0, "IBB":0, "HBP":0},
                             "pitching_stats":{ "W":0, "L":0, "G":0, "GS":0, "CG":0, "SHO":0, "SV":0, "IPouts":0, "H":0,
                                                "ER":0, "HR":0, "BB":0, "SO":0, "HBP":0},
                             "pitching_other":{"BAOpp":{"in":[],"out":[]}, "ERA":{"in":[],"out":[]}},
                             "other_stats":{"WAR":0, "salary":0, "allstars":0} }
        for stats in self.trade_out_stats:
            if "batting_stats" in stats and len(stats["batting_stats"]) > 0:
                for statline in stats["batting_stats"]:
                    self.transaction_total["batting_stats"]["G"] -= int(statline["G"])
                    self.transaction_total["batting_stats"]["AB"] -= int(statline["AB"])
                    self.transaction_total["batting_stats"]["R"] -= int(statline["R"])
                    self.transaction_total["batting_stats"]["H"] -= int(statline["H"])
                    self.transaction_total["batting_stats"]["2B"] -= int(statline["2B"])
                    self.transaction_total["batting_stats"]["3B"] -= int(statline["3B"])
                    self.transaction_total["batting_stats"]["HR"] -= int(statline["HR"])
                    self.transaction_total["batting_stats"]["RBI"] -= int(statline["RBI"])
                    self.transaction_total["batting_stats"]["SB"] -= int(statline["SB"])
                    self.transaction_total["batting_stats"]["BB"] -= int(statline["BB"])
                    self.transaction_total["batting_stats"]["SO"] -= int(statline["SO"])
                    self.transaction_total["batting_stats"]["IBB"] -= int(statline["IBB"])
                    self.transaction_total["batting_stats"]["HBP"] -= int(statline["HBP"])
            if "pitching_stats" in stats and len(stats["pitching_stats"]) > 0:
                for statline in stats["pitching_stats"]:
                    self.transaction_total["pitching_stats"]["W"] -= int(statline["W"])
                    self.transaction_total["pitching_stats"]["L"] -= int(statline["L"])
                    self.transaction_total["pitching_stats"]["G"] -= int(statline["G"])
                    self.transaction_total["pitching_stats"]["GS"] -= int(statline["GS"])
                    self.transaction_total["pitching_stats"]["CG"] -= int(statline["CG"])
                    self.transaction_total["pitching_stats"]["SHO"] -= int(statline["SHO"])
                    self.transaction_total["pitching_stats"]["SV"] -= int(statline["SV"])
                    self.transaction_total["pitching_stats"]["IPouts"] -= statline["IPouts"]
                    self.transaction_total["pitching_stats"]["H"] -= int(statline["H"])
                    self.transaction_total["pitching_stats"]["ER"] -= int(statline["ER"])
                    self.transaction_total["pitching_stats"]["HR"] -= int(statline["HR"])
                    self.transaction_total["pitching_stats"]["BB"] -= int(statline["BB"])
                    self.transaction_total["pitching_stats"]["SO"] -= int(statline["SO"])
                    self.transaction_total["pitching_stats"]["HBP"] -= int(statline["HBP"])

                    self.transaction_total["pitching_other"]["BAOpp"]["out"].append(statline["BAOpp"])
                    self.transaction_total["pitching_other"]["ERA"]["out"].append(statline["ERA"])

            if "pwar_salary" in stats and len("pwar_salary") > 0:
                for statline in stats["pwar_salary"]:
                    self.transaction_total["other_stats"]["WAR"] -= round(statline["WAR"], 2)
                    self.transaction_total["other_stats"]["salary"] -= statline["salary"]
            if "bwar_salary" in stats and len("bwar_salary") > 0:
                for statline in stats["bwar_salary"]:
                    self.transaction_total["other_stats"]["WAR"] -= round(statline["WAR"], 2)
                    self.transaction_total["other_stats"]["salary"] -= statline["salary"]
            if "allstar" in stats:
                self.transaction_total["other_stats"]["allstars"] -= len(stats["allstar"])

        for stats in self.trade_in_stats:
            if "batting_stats" in stats and len(stats["batting_stats"]) > 0:
                for statline in stats["batting_stats"]:
                    self.transaction_total["batting_stats"]["G"] += int(statline["G"])
                    self.transaction_total["batting_stats"]["AB"] += int(statline["AB"])
                    self.transaction_total["batting_stats"]["R"] += int(statline["R"])
                    self.transaction_total["batting_stats"]["H"] += int(statline["H"])
                    self.transaction_total["batting_stats"]["2B"] += int(statline["2B"])
                    self.transaction_total["batting_stats"]["3B"] += int(statline["3B"])
                    self.transaction_total["batting_stats"]["HR"] += int(statline["HR"])
                    self.transaction_total["batting_stats"]["RBI"] += int(statline["RBI"])
                    self.transaction_total["batting_stats"]["SB"] += int(statline["SB"])
                    self.transaction_total["batting_stats"]["BB"] += int(statline["BB"])
                    self.transaction_total["batting_stats"]["SO"] += int(statline["SO"])
                    self.transaction_total["batting_stats"]["IBB"] += int(statline["IBB"])
                    self.transaction_total["batting_stats"]["HBP"] += int(statline["HBP"])
            if "pitching_stats" in stats and len(stats["pitching_stats"]) > 0:
                for statline in stats["pitching_stats"]:
                    self.transaction_total["pitching_stats"]["W"] += int(statline["W"])
                    self.transaction_total["pitching_stats"]["L"] += int(statline["L"])
                    self.transaction_total["pitching_stats"]["G"] += int(statline["G"])
                    self.transaction_total["pitching_stats"]["GS"] += int(statline["GS"])
                    self.transaction_total["pitching_stats"]["CG"] += int(statline["CG"])
                    self.transaction_total["pitching_stats"]["SHO"] += int(statline["SHO"])
                    self.transaction_total["pitching_stats"]["SV"] += int(statline["SV"])
                    self.transaction_total["pitching_stats"]["IPouts"] += statline["IPouts"]
                    self.transaction_total["pitching_stats"]["H"] += int(statline["H"])
                    self.transaction_total["pitching_stats"]["ER"] += int(statline["ER"])
                    self.transaction_total["pitching_stats"]["HR"] += int(statline["HR"])
                    self.transaction_total["pitching_stats"]["BB"] += int(statline["BB"])
                    self.transaction_total["pitching_stats"]["SO"] += int(statline["SO"])

                    self.transaction_total["pitching_other"]["BAOpp"]["in"].append(statline["BAOpp"])
                    self.transaction_total["pitching_other"]["ERA"]["in"].append(statline["ERA"])
                    self.transaction_total["pitching_stats"]["HBP"] += int(statline["HBP"])
            if "pwar_salary" in stats and len("pwar_salary") > 0:
                for statline in stats["pwar_salary"]:
                    self.transaction_total["other_stats"]["WAR"] += statline["WAR"]
                    self.transaction_total["other_stats"]["salary"] += statline["salary"]
            if "bwar_salary" in stats and len("bwar_salary") > 0:
                for statline in stats["bwar_salary"]:
                    self.transaction_total["other_stats"]["WAR"] += statline["WAR"]
                    self.transaction_total["other_stats"]["salary"] += statline["salary"]
            if "allstar" in stats:
                self.transaction_total["other_stats"]["allstars"] += len(stats["allstar"])

        if len(self.transaction_total["pitching_other"]["BAOpp"]["in"]) > 0:
            self.transaction_total["pitching_other"]["BAOpp"]["in"] = \
                sum(self.transaction_total["pitching_other"]["BAOpp"]["in"]) / len(self.transaction_total["pitching_other"]["BAOpp"]["in"])
            self.transaction_total["pitching_other"]["ERA"]["in"] = \
                sum(self.transaction_total["pitching_other"]["ERA"]["in"]) / len(
                    self.transaction_total["pitching_other"]["ERA"]["in"])

        if len(self.transaction_total["pitching_other"]["BAOpp"]["out"]) > 0:
            self.transaction_total["pitching_other"]["BAOpp"]["out"] = \
                sum(self.transaction_total["pitching_other"]["BAOpp"]["out"]) / len(self.transaction_total["pitching_other"]["BAOpp"]["out"])
            self.transaction_total["pitching_other"]["ERA"]["out"] = \
                sum(self.transaction_total["pitching_other"]["ERA"]["out"]) / len(self.transaction_total["pitching_other"]["ERA"]["out"])

        self.transaction_total["other_stats"]["WAR"] = round(self.transaction_total["other_stats"]["WAR"], 2)

        return self.transaction_total
