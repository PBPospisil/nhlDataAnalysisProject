import os
import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
from graph_data import GraphData


class GraphGoalies(GraphData):

    def __init__(self):
        GraphData.__init__(self)
        self.player_info, self.goalie_stats = self.initialize_root_dataframes()
        self.sorted_by_game_id = self.sort_by_game_id()
        self.sorted_by_toi = self.get_toi_for_each_player()
        self.create_plot()
        self.check_parent_folder_and_save_plot()

    # initialize graphing object and import csv to dataframe. Clean by removing rows
    # with na and converting column types to predefined from graph_data
    def initialize_root_dataframes(self):
        player_info = self.get_column_types(
                        self.drop_na_row(
                          self.import_csv('../data/player_info.csv')),
                        self.player_info_dtypes)
        goalie_stats = self.get_column_types(
                        self.drop_na_row(
                         self.import_csv('../data/game_goalie_stats.csv')),
                        self.goalie_stats_dtypes)

        goalie_stats.loc[:,'game_id'] = goalie_stats.game_id.astype(np.int)
        goalie_stats.loc[:,'timeOnIce'] = goalie_stats.timeOnIce.astype(np.float)

        return player_info, goalie_stats

    #goalies initially sorted by games played (later to be changed to sorted by DATE)
    def sort_by_game_id(self):
        self.goalie_stats.sort_values(['game_id'], ascending=True, inplace=True)
        sorted_by_game_id = pandas.DataFrame(np.array(
                                                       self.goalie_stats['player_id'].unique()),
                                                       columns=['player_id'])

        return sorted_by_game_id

    # get toi for  each player
    def get_toi_for_each_player(self):
        time_on_ice = []
        for player in self.sorted_by_game_id['player_id']:
            time_on_ice += [self.goalie_stats.loc[self.goalie_stats['player_id'] == player, 'timeOnIce'].sum()]
        self.sorted_by_game_id['time_on_ice'] = time_on_ice
        self.sorted_by_game_id.loc[:,'time_on_ice'] = self.sorted_by_game_id.time_on_ice.astype(np.float)

        # sort for top 10 by toi
        sorted_by_toi = self.sorted_by_game_id.sort_values(['time_on_ice'], ascending=False)
        sorted_by_toi.loc[:,'player_id'] = sorted_by_toi.player_id.astype(np.float)

        return sorted_by_toi

    def get_player_save_percentage(self, player_stats, player):
        toi_sum = total_shots = total_saves = 0
        player_id = []; accum_toi = []; accum_sv_percentage = []
        # get player sv%
        for game in player_stats['game_id']:
            player_id += [player]
            toi_sum += player_stats.loc[player_stats['game_id'] == game, 'timeOnIce'].item()
            total_shots += player_stats.loc[player_stats['game_id'] == game, 'shots'].item()
            total_saves += player_stats.loc[player_stats['game_id'] == game, 'saves'].item()

            accum_toi += [toi_sum/3600]
            accum_sv_percentage += [total_saves/total_shots]

        return [player_id, accum_toi, accum_sv_percentage]

    # get top 10 goalie save percentages
    def get_top_ten_goalie_save_percentage(self):
        player_id = []; accum_toi = []; accum_sv_percentage = []; top10 = 0
        for player in self.sorted_by_toi['player_id'][:10]:
            player = str(int(self.sorted_by_toi.iloc[top10,0]))
            player_stats = self.goalie_stats.loc[self.goalie_stats['player_id'] == player].copy()
            player_stats.loc[:,'shots'] = player_stats.shots.astype(np.float)
            player_stats.loc[:,'saves'] = player_stats.saves.astype(np.float)

            [single_player_id,
             single_player_toi,
             single_player_sv_percentage] =  self.get_player_save_percentage(player_stats, player)
            player_id += single_player_id;
            accum_toi += single_player_toi;
            accum_sv_percentage += single_player_sv_percentage
            top10 += 1
        return self.create_top10_by_toi_sv(player_id, accum_toi, accum_sv_percentage)

    def create_top10_by_toi_sv(self, player_id, accum_toi, accum_sv_percentage):
        top10_by_toi_sv = pandas.DataFrame(np.array(player_id), columns = ['player_id'])
        top10_by_toi_sv['time_on_ice'] = accum_toi
        top10_by_toi_sv['save_percentage'] = accum_sv_percentage
        return top10_by_toi_sv

    def create_plot(self):
        top10_by_toi_sv = self.get_top_ten_goalie_save_percentage()
        plt.figure(figsize=(12, 9))
        for player in self.sorted_by_toi['player_id'][:10]:
            name = self.player_info.loc[self.player_info['player_id'] == str(int(player)),
                                        'firstName'].item()+ ' ' + self.player_info.loc[self.player_info['player_id'] == str(int(player)),
                                        'lastName'].item()
            plt.plot('time_on_ice', 'save_percentage', data=top10_by_toi_sv[top10_by_toi_sv['player_id'] == str(int(player))], label=name)
            plt.ylim(0.88,0.95)

        plt.xlabel('hours played'); plt.ylabel('save percentage'); plt.legend()
        plt.title('lineplot of save percentage of top 10 Goaltenders by TOI from 2010-2019')

    # check if parent folder exists, else make one. Save plot as png
    def check_parent_folder_and_save_plot(self):
        checkAndMakeImgFolder()

        if os.path.exists('../img/lineplot-goalies-top10-minutes-save-percentage.png'):
            os.remove('../img/lineplot-goalies-top10-minutes-save-percentage.png')
        plt.savefig('../img/lineplot-goalies-top10-minutes-save-percentage.png', bbox_inches='tight', dpi=300)
