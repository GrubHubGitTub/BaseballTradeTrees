import pandas as pd
transactions = pd.read_csv("data/transac2021cleaned.csv")


class TransactionWizard:

    def __init__(self, trans_id=None, player=None, choice=None):
        self.player = player
        self.trans_id = trans_id
        self.choice = choice
        self.all_trans = None
        self.trades = None
        self.traded_from_franchise_list = []
        self.traded_for_ids_list = []
        self.traded_with_ids_list= []
        self.get_transactions()

    def get_transactions(self):
        if self.player is not None:
            self.all_trans = transactions[transactions.player == self.player]
        elif self.trans_id is not None:
            self.all_trans = transactions[transactions.transaction_id == self.trans_id]

    def get_trades(self):
        self.trades = self.all_trans[self.all_trans.typeof == "T "]
        self.traded_from_franchise_list = self.trades["from-franchise"].tolist()

    def get_traded_ids_list(self):
        traded_to_user_choice = self.trades[self.trades["to-franchise"] == self.choice]
        self.traded_for_ids_list = traded_to_user_choice["player"].tolist()
        return self.traded_for_ids_list

    def get_traded_with_ids_list(self):
        traded_to_user_choice = self.trades[self.trades["from-franchise"] == self.choice]
        self.traded_with_ids_list = traded_to_user_choice["player"].tolist()
        return self.traded_with_ids_list










