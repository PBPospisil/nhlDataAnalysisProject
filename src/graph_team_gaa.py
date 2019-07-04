import os
import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from graph_data import GraphData


class GraphTeamGaa(GraphData):

    def __init__(self):
        GraphData.__init__(self)
        self.team_colors = {'1':'red', '4':'darkorange', '26':'black', '14':'blue', '6':'gold',
                    '3':'blue', '5':'gold', '17':'red', '28':'darkcyan', '18':'gold',
                     '23':'blue', '16':'red', '9':'red', '8':'red', '30':'green',
                      '15':'red', '19':'blue', '24':'orange', '27':'maroon', '2':'orange',
                       '20':'red', '21':'maroon', '25':'green', '13':'red', '10':'blue',
                        '29':'blue', '52':'blue', '54':'gold', '12':'red', '7':'blue',
                         '22':'orange', '53':'maroon', '11':'blue'}

        self.team_info, self.goalie_stats, self.games = self.initialize_root_dataframes()
        self.main_team = ''; self.abbreviation_main_team = ''; self.short_name_main_team = ''
        self.team_name_main_team = ''

    def initialize_root_dataframes(self):
        team_info = self.get_column_types(self.drop_na_row(self.import_csv('../data/team_info.csv')),
                              self.team_info_dtypes)
        goalie_stats = self.get_column_types(self.drop_na_row(self.import_csv('../data/game_goalie_stats.csv')),
                              self.goalie_stats_dtypes)
        games = self.get_column_types(self.drop_na_row(self.import_csv('../data/game.csv')),
                              self.game_dtypes)

        return team_info, goalie_stats, games

    def get_team_from_user(self, chosen_team):
        self.abbreviation_main_team = self.team_info.loc[self.team_info['team_id'] == chosen_team[2], 'abbreviation'].item()
        self.short_name_main_team = chosen_team[0].lower()
        self.team_name_main_team = chosen_team[1]
        self.main_team = chosen_team[2]

    def sort_goalie_stats_by_game_id(self):
        self.goalie_stats.loc[:,'game_id'] = self.goalie_stats.game_id.astype(np.int)
        self.goalie_stats.sort_values(['game_id'], ascending=True, inplace=True)

    def add_gaa_toi_columns(self):
        gaa = []; toi = []; game_id = []
        current_toi = defaultdict(int); current_shots_against = defaultdict(int);
        current_saves_for = defaultdict(int)

        for index, team in enumerate(self.goalie_stats['team_id']):
            current_shots_against[team] += self.goalie_stats.iloc[index, 13]
            current_saves_for[team] += self.goalie_stats.iloc[index, 11]
            current_toi[team] += self.goalie_stats.iloc[index, 3] / 3600
            gaa += [(current_shots_against[team] - current_saves_for[team]) / current_toi[team]]
            toi += [current_toi[team]]
            game_id += [self.goalie_stats.iloc[index, 0]]

        self.goalie_stats['gaa'] = gaa
        self.goalie_stats['toi'] = toi

    def get_ticks(self):
        main_team_goalie_stats = self.goalie_stats.loc[self.goalie_stats['team_id'] == self.main_team]
        last_date = len(main_team_goalie_stats['game_id'].unique())
        if last_date > 500:
            last_date = 500
        return [50,100,200,300,400,last_date]

    def get_date_tick_labels(self):
        main_team_goalie_stats = self.goalie_stats.loc[self.goalie_stats['team_id'] == self.main_team]
        tick_labels = []; games_played = 0; ticks = self.get_ticks()

        for index, game in enumerate(main_team_goalie_stats['game_id'].unique()):
            games_played += 1
            if games_played == ticks[0]:
                tick_labels += [self.games.loc[self.games['game_id'] == str(game), 'date_time'].item()]
                ticks = ticks[1:]

        return tick_labels

    def create_team_gaa_lineplot(self):
        plt.figure(figsize=(12, 9))
        plt.plot('toi', 'gaa', data=self.goalie_stats.loc[self.goalie_stats['team_id'] == self.main_team], label=self.abbreviation_main_team, color=self.team_colors[self.main_team], linewidth=2.0, zorder=30)
        plt.legend()
        for team in self.goalie_stats['team_id'].unique():
            if team != self.main_team:
                plt.plot('toi', 'gaa', data=self.goalie_stats.loc[self.goalie_stats['team_id'] == team], color='grey')
        plt.xticks(self.get_ticks(), self.get_date_tick_labels(), fontsize=6)
        plt.ylim(1.3,2.7); plt.xlim(50, 550)
        plt.ylabel('GAA'); plt.xlabel('game date')
        plt.title('GAA vs. time with focus on ' + self.short_name_main_team + ' ' + self.team_name_main_team + ' from 2010-2019')

    def save_plot(self):
        checkAndMakeImgFolder()
        if os.path.exists('../img/team-gaa-' + '-'.join(self.short_name_main_team.split(' ')) + '.png'):
            os.remove('../img/team-gaa-' + '-'.join(self.short_name_main_team.split(' ')) + '.png')
        plt.savefig('../img/team-gaa-' + '-'.join(self.short_name_main_team.split(' ')) + '.png', bbox_inches='tight', dpi=300)

    def create_plot_and_save(self):
        self.create_team_gaa_lineplot()
        self.save_plot()
