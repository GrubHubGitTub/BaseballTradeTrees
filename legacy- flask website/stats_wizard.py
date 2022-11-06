import pandas as pd
stats = pd.read_csv("data/stats/StatsSalaryCombinedIDs.csv")


class StatsWizard:

    def __init__(self, retro_id, stats_start_date, from_franchise, to_franchise, stats_end_date=None, ):
        self.retro_id = retro_id
        self.stats_start_date = stats_start_date
        self.stats_end_date = stats_end_date
        self.from_franchise = from_franchise
        self.to_franchise = to_franchise
        self.all_player_stats = None
        self.team_stats = None
        self.from_team_stats = None
        self.year_on_team_stats = None
        self.WAR_on_team = None
        self.G_on_team = None
        self.PA_on_team = None
        self.IPouts_on_team = None
        self.trade_year_salary = None

    def get_stats(self):
        self.all_player_stats = stats[stats.retroID == self.retro_id]
        self.team_stats = self.all_player_stats[self.all_player_stats.Franchise == self.to_franchise]
        if self.stats_end_date is not None:
            self.year_on_team_stats = self.team_stats[(self.team_stats.year_ID >= self.stats_start_date) &
                                                      (self.team_stats.year_ID <= self.stats_end_date)]
        else:
            self.year_on_team_stats = self.team_stats[self.team_stats.year_ID >= self.stats_start_date]
        self.get_WAR()
        self.get_Gs()
        self.get_PAs()
        self.get_IPouts()

    def get_WAR(self):
        self.WAR_on_team = round(self.year_on_team_stats["WAR"].sum(), 2)

    def get_Gs(self):
        self.G_on_team = round(self.year_on_team_stats["G"].sum(), 2)

    def get_PAs(self):
        self.PA_on_team = round(self.year_on_team_stats["PA"].sum(), 2)

    def get_IPouts(self):
        self.IPouts_on_team = round(self.year_on_team_stats["IPouts"].sum(), 2)

    def get_salary_from(self):
        self.team_stats = self.all_player_stats[self.all_player_stats.Franchise == self.from_franchise]
        trade_year = self.team_stats[self.team_stats["year_ID"] == self.stats_start_date]
        if len(trade_year.index) > 1:
            trade_year = trade_year.head(1)
        self.trade_year_salary = float(trade_year["salary"].sum())


    def get_salary_to(self):
        self.team_stats = self.all_player_stats[self.all_player_stats.Franchise == self.from_franchise]
        trade_year = self.team_stats[self.team_stats["year_ID"] == self.stats_start_date]
        if len(trade_year.index) > 1:
            trade_year = trade_year.head(1)
        self.trade_year_salary = float(trade_year["salary"].sum())


