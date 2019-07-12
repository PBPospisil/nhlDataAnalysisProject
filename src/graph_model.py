import os
import pandas
import numpy as np
import csv
from csv_to_df import csv_to_df
from csv_to_df import check_and_make_img_folder
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import norm
import sys
import time
from graph_data import GraphData
import seaborn as sns; sns.set()
from linear_model import LinearModel
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation


class GraphModel(GraphData):

    def __init__(self):
        GraphData.__init__(self)
        self.goalie_stats_dtypes = {'timeOnIce':'int',
                                    'shots':'int', 'saves':'int',
                                    'evenSaves':'int',
                                    'evenShotsAgainst':'int',
                                    'decision':'str'
                                    }

        self.team_info = self.get_column_types(self.import_csv('../data/team_info.csv'), self.team_info_dtypes)
        self.goalie_stats = self.get_column_types(self.import_csv('../data/game_goalie_stats.csv'), self.goalie_stats_dtypes)
        self.game = self.get_column_types(self.import_csv('../data/game.csv'), self.game_dtypes)
        self.team_stats = self.get_column_types(self.import_csv('../data/game_teams_stats.csv'), self.team_stats_dtypes)
        self.team_season_id_dict = defaultdict(int)
        self.team_season = []
        self.epsilon = 0
        self.delta = 0
        self.mse = 0; self.absolute_error_ = []; self.sse = self.time_initial = 0
        self.mse_op = 1;
        self.op_alpha = 0
        self.current_alpha = 0.75
        self.winning = []; self.team = []; self.df_alpha = []; self.season_ = []; self.time = [];

    def only_regular_season(self, dataframe):
        for game in dataframe['game_id'].unique():
            if len(self.game.loc[self.game['game_id'] == game, 'type']) < 1:
                self.game.drop(self.game.loc[self.game['game_id'] == game].index, inplace=True)
                dataframe.drop(dataframe.loc[dataframe['game_id'] == game].index, inplace=True)
                continue
            if self.game.loc[self.game['game_id'] == game, 'type'].item() == 'P':
                dataframe.drop(dataframe.loc[dataframe['game_id'] == game].index, inplace=True)

    def get_seasons(self, dataframe):
        seasons = []
        for game in dataframe['game_id']:
            seasons.append(self.game.loc[self.game['game_id'] == game, 'season'].item())
        dataframe['season'] = seasons
        dataframe.loc[:,'season'] = dataframe.season.astype(str)

    def create_unique_team_season_identifier(self, dataframe):
        team_season_id_dict_list = []; id = 1
        for index, _ in enumerate(dataframe['game_id']):
            if self.team_season_id_dict[' '.join([dataframe.iloc[index, 2], dataframe.iloc[index, 19]])] == 0:
                self.team_season_id_dict[' '.join([dataframe.iloc[index, 2], dataframe.iloc[index, 19]])] = id
                team_season_id_dict_list.append(' '.join([dataframe.iloc[index, 2], dataframe.iloc[index, 19]]))
                id += 1
            else:
                team_season_id_dict_list.append(' '.join([dataframe.iloc[index, 2], dataframe.iloc[index, 19]]))
        dataframe['team_season_id_dict_list'] = team_season_id_dict_list

    def create_team_season(self):
        self.team_season = pandas.DataFrame(np.zeros(len(self.team_season_id_dict)))
        self.team_season['team_season_id_dict_list'] = self.team_season_id_dict.keys()
        self.team_season['wins'] = np.zeros(len(self.team_season))
        self.team_season['gamesPlayed'] = np.zeros(len(self.team_season))
        self.team_season['winPercentage'] = np.zeros(len(self.team_season))
        self.team_season['PPO'] = np.zeros(len(self.team_season))
        self.team_season['PPG'] = np.zeros(len(self.team_season))
        self.team_season['PKSaved'] = np.zeros(len(self.team_season))
        self.team_season['PKOPP'] = np.zeros(len(self.team_season))
        self.team_season['winPred'] = np.zeros(len(self.team_season))
        self.team_season['GF'] = np.zeros(len(self.team_season))
        self.team_season['GA'] = np.zeros(len(self.team_season))
        self.team_season['GAA'] = np.zeros(len(self.team_season))
        self.team_season['shots'] = np.zeros(len(self.team_season))
        self.team_season['saves'] = np.zeros(len(self.team_season))
        self.team_season['totalTOI'] = np.zeros(len(self.team_season))

        self.team_season.drop(0, axis=1, inplace=True)

    def team_stats_data_gather(self, team_season_id_index, team, season):
        team_stats_only_this_team = self.team_stats.loc[self.team_stats['team_id'] == team]
        team_stats_only_this_team_opponent = self.team_stats.loc[self.team_stats['team_id'] != team]
        for game_index, game in enumerate(team_stats_only_this_team['game_id']):
            if team_stats_only_this_team.iloc[game_index, 15] == season:
                self.team_season.iloc[team_season_id_index, 4] += team_stats_only_this_team.iloc[game_index, 10]
                self.team_season.iloc[team_season_id_index, 5] += team_stats_only_this_team.iloc[game_index, 11]
                self.team_season.iloc[team_season_id_index, 6] += team_stats_only_this_team_opponent.iloc[game_index, 10]-team_stats_only_this_team_opponent.iloc[game_index, 11]
                self.team_season.iloc[team_season_id_index, 7] += team_stats_only_this_team_opponent.iloc[game_index, 10]
                self.team_season.iloc[team_season_id_index, 9] += team_stats_only_this_team.iloc[game_index, 6] - team_stats_only_this_team.iloc[game_index, 11]

    def goalie_stats_data_gather(self, team_season_id_index, team, season):
        goalie_stats_only_this_team = self.goalie_stats.loc[self.goalie_stats['team_id'] == team]
        for game_index, game in enumerate(goalie_stats_only_this_team['game_id']):
            if goalie_stats_only_this_team.iloc[game_index, 19] == season:
                # shots
                self.team_season.iloc[team_season_id_index, 12] += goalie_stats_only_this_team.iloc[game_index, 7]
                #saves
                self.team_season.iloc[team_season_id_index, 13] += goalie_stats_only_this_team.iloc[game_index, 8]
                #totalTOI
                self.team_season.iloc[team_season_id_index, 14] += goalie_stats_only_this_team.iloc[game_index, 3]
                #wins
                if goalie_stats_only_this_team.iloc[game_index, 15] == 'W':
                    self.team_season.iloc[team_season_id_index, 1] += 1
                self.team_season.iloc[team_season_id_index, 2] += 1
                # GA
                self.team_season.iloc[team_season_id_index, 10] += goalie_stats_only_this_team.iloc[game_index, 13] - goalie_stats_only_this_team.iloc[game_index, 11]

    def calculate_gaa(self, team_season_id_index):
        if self.team_season.iloc[team_season_id_index, 14]:
            self.team_season.iloc[team_season_id_index, 11] = ((self.team_season.iloc[team_season_id_index, 12] - self.team_season.iloc[team_season_id_index, 13]) * 3600) / self.team_season.iloc[team_season_id_index, 14]
        else:
            self.team_season.iloc[team_season_id_index, 11] = ((self.team_season.iloc[team_season_id_index, 12] - self.team_season.iloc[team_season_id_index, 13]) * 3600) / 1

    def calculate_win_stats(self, team_season_id_index):
        self.team_season.iloc[team_season_id_index, 3] = self.team_season.iloc[team_season_id_index, 1] / self.team_season.iloc[team_season_id_index, 2]

        self.team_season.iloc[team_season_id_index, 8] = (self.team_season.iloc[team_season_id_index, 9] / self.team_season.iloc[team_season_id_index, 10])

        # self.team_season.iloc[team_season_id_index, 8] = ((self.team_season.iloc[team_season_id_index, 9] / self.team_season.iloc[team_season_id_index, 10]) +
        #                                         ((self.team_season.iloc[team_season_id_index, 5] / self.team_season.iloc[team_season_id_index, 4]) *
        #                                          (self.team_season.iloc[team_season_id_index, 6] / self.team_season.iloc[team_season_id_index, 7])))
        self.calculate_gaa(team_season_id_index)

    def clean_up(self, season_column_list, team_column_list):
        self.team_season['season'] = season_column_list
        self.team_season['team_id'] = team_column_list
        self.team_season.loc[:,'season'] = self.team_season.season.astype(np.int)
        self.team_season.loc[:,'team_id'] = self.team_season.team_id.astype(np.int)

    def fill_team_season(self):
        season_column_list = []; team_column_list = []
        for team_season_id_index, team_season_id in enumerate(self.team_season['team_season_id_dict_list']):
            [team, season] = str(team_season_id).split(' ')
            season_column_list.append(season); team_column_list.append(team)

            self.team_stats_data_gather(team_season_id_index, team, season)

            self.goalie_stats_data_gather(team_season_id_index, team, season)

            self.calculate_win_stats(team_season_id_index)

        self.clean_up(season_column_list, team_column_list)

    def get_alpha(self):
        self.time_initial = time.time()
        for season in self.goalie_stats['season'].unique():
            self.find_op_alpha(season)
            self.absolute_error_ = []; self.mse = self.sse = self.op_alpha = 0
            self.mse_op = 1; self.current_alpha = 0.75

    def get_alpha_scatterplot(self, gfga_season_alpha):
        fig4, ax4 = plt.subplots()

        plt.scatter('time', 'alpha', data=gfga_season_alpha.loc[gfga_season_alpha['season'] == '20122013'], label='20122013', alpha=0.8, c='cyan', linewidth=0.2, edgecolors='black', s=50, marker='.')
        plt.scatter('time', 'alpha', data=gfga_season_alpha.loc[gfga_season_alpha['season'] == '20132014'], label='20132014', alpha=0.8, c='green', linewidth=0.2, edgecolors='black', s=50, marker='.')
        plt.scatter('time', 'alpha', data=gfga_season_alpha.loc[gfga_season_alpha['season'] == '20142015'], label='20142015', alpha=0.8, c='orangered', linewidth=0.2, edgecolors='black', s=50, marker='.')
        plt.scatter('time', 'alpha', data=gfga_season_alpha.loc[gfga_season_alpha['season'] == '20152016'], label='20152016', alpha=0.8, c='blue', linewidth=0.2, edgecolors='black', s=50, marker='.')
        plt.scatter('time', 'alpha', data=gfga_season_alpha.loc[gfga_season_alpha['season'] == '20162017'], label='20162017', alpha=0.8, c='coral', linewidth=0.2, edgecolors='black', s=50, marker='.')
        plt.scatter('time', 'alpha', data=gfga_season_alpha.loc[gfga_season_alpha['season'] == '20172018'], label='20172018', alpha=0.8, c='limegreen', linewidth=0.2, edgecolors='black', s=50, marker='.')

        plt.xlabel('time', fontsize=7); plt.ylabel('alpha coeffiecient', fontsize=7); plt.legend(fontsize=6)
        plt.yticks(fontsize=6), plt.xticks(fontsize=6)
        plt.title('alpha coefficient optimization over time for each season 2010-2019', fontsize=8)
        self.check_dir_and_save(fig4, '../img/win-prediction-winpercentage-scatterplot-alpha-separate.png')


    def season_op_alpha(self, season=False):
        alpha = []; seasons = []; gfga = []
        self.goalie_stats = self.goalie_stats.sort_values('game_id', ascending=True, inplace=False)

        self.get_alpha()

        gfga_season_alpha = pandas.DataFrame(self.season_, columns=['season'])
        gfga_season_alpha['alpha'] = self.df_alpha
        gfga_season_alpha['time'] = self.time

        self.get_alpha_scatterplot(gfga_season_alpha)


    def check_new_op(self):
        if self.mse < self.mse_op and self.mse != 0:
            self.mse_op = self.mse
            self.op_alpha = self.current_alpha

    def choose_minimizing_direction(self, upper, lower):
        if len(self.absolute_error_) != 0:
            if sum(self.absolute_error_)/len(self.absolute_error_) > 0:
                upper = self.current_alpha
                self.current_alpha = (upper+lower)/2
            else:
                lower = self.current_alpha
                self.current_alpha = (upper+lower)/2
        return upper, lower

    def calculate_mse(self, total_games):
        if self.sse != 0:
            if total_games == 0:
                self.mse = self.sse / 1
            else:
                self.mse = self.sse / total_games

    def find_op_alpha(self, season=False):
        phi = 0.0001;upper=1.2;lower=epoch=sse=total_games=0
        while abs(self.current_alpha-self.op_alpha) >= phi and epoch<50:
            self.check_new_op()
            upper, lower = self.choose_minimizing_direction(upper, lower)
            self.calculate_mse(total_games)
            self.sse = 0; self.absolute_error_ = []; epoch+=1
            total_games += self.graph_all_teams_for_epsilon(season)


    def get_stats_for_alpha(self, season):
        total_games = gfga_sum = gfga_count = 0
        for season_ in self.goalie_stats['season'].unique():
            if season_ == season:
                for team in self.team_stats['team_id'].unique():
                    winning,[self.sse, self.absolute_error_], GPsum = LinearModel(self.team_season).team_prediction_lineplot(self.goalie_stats, team, self.absolute_error_, self.sse, self.current_alpha, season_)
                    gfga_sum += winning['gfga'].sum()
                    gfga_count += winning['gfga'].count()
                    total_games += GPsum
                #self.winning.append(gfga_sum/gfga_count)
                self.df_alpha.append(self.current_alpha)
                self.season_.append(season)
                self.time.append(time.time() - self.time_initial)


    def graph_all_teams_for_epsilon(self, season=False):
        total_games = 0;
        if season:
            self.get_stats_for_alpha(season)
        else:
            for season_ in self.goalie_stats['season'].unique():
                for team in self.team_stats['team_id'].unique():
                    _,[self.sse, self.absolute_error_], GPsum = LinearModel(self.team_season).team_prediction_lineplot(self.goalie_stats, team, self.absolute_error_, self.sse, self.current_alpha, season_)
                    total_games += GPsum
        return total_games

    def compose_model_plot(self, chosen_team, win_prediction_model):
        short_name_main_team = chosen_team[0]; team_name_main_team = chosen_team[1]

        fig1, ax1 = plt.subplots()
        plt.plot(win_prediction_model['game_id'], win_prediction_model['predWinPercentage'], label='pred-corr win %', linestyle='-', color='#4E73AE', alpha=0.7, linewidth=0.5)
        #plt.plot(win_prediction_model['game_id'], win_prediction_model['predWinPercentage_gfga'], label='pred-0.8 win % error', linestyle='-', color='#ff0000', alpha=0.6, linewidth=0.5)
        #plt.plot(win_prediction_model['game_id'], win_prediction_model['actualWinPercentage'], label='actual win %', linestyle='-', color='#4E73B6', alpha=0.7, linewidth=0.5)
        plt.plot(win_prediction_model['game_id'], win_prediction_model['average_error'], label='average error', linestyle='-', color='000000', alpha=0.6, linewidth=0.5)

        plt.fill_between(win_prediction_model['game_id'], win_prediction_model['predWinPercentage']-win_prediction_model['absolute_error'], win_prediction_model['predWinPercentage']+win_prediction_model['absolute_error'], alpha=0.5, edgecolor='#597BB2', facecolor='#6C8BBB')
        plt.legend(fontsize=6); plt.xlabel('game', fontsize=7); plt.ylabel('win prediction', fontsize=7)
        plt.yticks([0.0,0.2,0.4,0.6,0.8,1.0],['0.0','0.2','0.4','0.6','0.8','1.0'], fontsize=6)
        plt.xticks(fontsize=6)
        plt.title('Predicted win percentage of the ' + short_name_main_team + ' ' + team_name_main_team + ' in the 2017-2018 season', fontsize=8)

        self.check_dir_and_save(plt, '../img/win-prediction-winpercentage-error.png')

    def graph_model_error(self, chosen_team):
        short_name_main_team = chosen_team[0]; team_name_main_team = chosen_team[1]
        team_of_interest = chosen_team[2]

        win_prediction_model,_,_ = LinearModel(self.team_season).team_prediction_lineplot(self.goalie_stats, team_of_interest, self.absolute_error_, self.mse, self.current_alpha, season='20172018')
        self.compose_model_plot(chosen_team, win_prediction_model)

    def graph_model_regplot(self):
        fig2, ax2 = plt.subplots()
        ax2 = sns.regplot(x='winPred', y='winPercentage', data=self.team_season,
                          marker='o', scatter_kws={'s': 13, 'alpha': 0.7, 'linewidths': 0.5},
                          line_kws={'lw': 1.4, 'color': '#4E73AE'})
        plt.xlabel('win prediction', fontsize=7); plt.ylabel('win percentage', fontsize=7)
        plt.yticks(fontsize=6), plt.xticks(fontsize=6)
        plt.title('Win percentage vs. win prediction of each season for every team 2010-2019', fontsize=8)
        
        self.check_dir_and_save(fig2, '../img/win-prediction-winpercentage-regplot.png')

    def graph_model_scatterplot(self):
        fig3, ax3 = plt.subplots()
        ax3 = plt.scatter(x='winPred', y='winPercentage', data=self.team_season, alpha=0.7, c='#4E73AE', linewidth=0.2, edgecolors='#4E73AE', s=50, marker='.')
        plt.xlabel('win prediction', fontsize=7); plt.ylabel('win percentage', fontsize=7)
        plt.yticks(fontsize=6), plt.xticks(fontsize=6)
        plt.title('win percentage vs. win prediction of each season for every team 2010-2019', fontsize=8)
        plt.annotate(('Correlation coeffiecient:' + '{0:.' + str(3)+ 'f}').format(self.team_season['winPercentage'].corr(self.team_season['winPred'])), (1.425,0.3), fontsize=7)
        self.check_dir_and_save(fig3, '../img/win-prediction-winpercentage-scatterplot.png')

    def check_dir_and_save(cls, fig, figure_name):
        check_and_make_img_folder()
        if os.path.exists(figure_name):
            os.remove(figure_name)
        fig.savefig(figure_name, bbox_inches='tight', dpi=300)
