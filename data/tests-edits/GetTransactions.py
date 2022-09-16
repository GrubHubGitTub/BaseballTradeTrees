import pandas as pd
import csv
transactions = pd.read_csv("stats_transactions_06092022.csv")


class GetTransactions:

    def __init__(self, transac_id=None, retro_id=None, franch_id=None, parent_retro=None, parent_transaction=None):
        self.player = retro_id
        self.transac_id = transac_id
        self.franch_id = franch_id
        self.parent_retro = parent_retro
        self.parent_transaction = parent_transaction
        self.all_transac = None
        self.trades = None
        self.traded_from_franchise_list = []
        self.traded_for_ids_dict = {}
        self.traded_with_ids_list = []
        if self.parent_transaction is not None:
            self.write_parent_tree()
        else:
            self.get_transactions()

    def write_parent_tree(self):
        parents = pd.read_csv("ParentTrees.csv")
        try:
            parent_row = parents[(parents["transaction_ID"] == self.transac_id) & (parents["from_franch"] == self.franch_id)]
        except ValueError:
            row = [self.transac_id, self.franch_id, self.parent_retro, self.parent_transaction]
            with open("ParentTrees.csv", "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
        else:
            if parent_row.empty:
                row = [self.transac_id, self.franch_id, self.parent_retro, self.parent_transaction]
                with open("ParentTrees.csv", "a", newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(row)
            else:
                pass
        self.get_transactions()

    def get_transactions(self):
        if self.player is not None:
            self.all_transac = transactions[transactions.player == self.player]
        elif self.transac_id is not None:
            self.all_transac = transactions[transactions.transaction_ID == self.transac_id]

    def get_trades(self):
        self.trades = self.all_transac[self.all_transac.type == "T "]
        self.traded_from_franchise_list = self.trades["from_franchise"].tolist()

    def get_traded_for_ids_dict(self):
        traded_to_user_choice = self.trades[self.trades["to_franchise"] == self.franch_id]
        traded_for_ids_list = traded_to_user_choice["player"].tolist()
        for retro_id in traded_for_ids_list:
            self.traded_for_ids_dict[retro_id] = retro_id
        return self.traded_for_ids_dict

    def get_traded_with_ids_list(self):
        traded_to_user_choice = self.trades[self.trades["from_franchise"] == self.franch_id]
        self.traded_with_ids_list = traded_to_user_choice["player"].tolist()
        return self.traded_with_ids_list

    def get_ptbnl_info(self):
        ptbnl = self.all_transac[self.all_transac["player"] == "PTBNL/Cash"]
        info = ptbnl["info"].tolist()
        return info










