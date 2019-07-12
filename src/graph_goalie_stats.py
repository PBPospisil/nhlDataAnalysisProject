import os
import pandas
import numpy as np
import csv
from csv_to_df import csv_to_df
from csv_to_df import check_and_make_img_folder
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from graph_data import GraphData


class GraphGoalieStats(GraphData):

    def __init__(self, mode='GAA', figure_name='../img/goalie-gaa-winpercentage-regplot.png'):
        GraphData.__init__(self)
        self.team_info = self.get_column_types(self.drop_na_row(self.import_csv('../data/team_info.csv')), self.team_info_dtypes)
        self.goalie_stats = self.get_column_types(self.drop_na_row(self.import_csv('../data/game_goalie_stats.csv')), self.goalie_stats_dtypes)
        self.game = self.get_column_types(self.drop_na_row(self.import_csv('../data/game.csv')), self.game_dtypes)
        self.team_stats = self.get_column_types(self.drop_na_row(self.import_csv('../data/game_teams_stats.csv')), self.team_stats_dtypes)
        self.goalie_season_id_dict = defaultdict(int)
        self.goalie_season = []
        self.mode = mode
        self.figure_name=figure_name

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

    def create_unique_goalie_season_identifier(self, dataframe):
        goalie_season_id_dict_list = []; id = 1
        for index, _ in enumerate(dataframe['game_id']):
            if self.goalie_season_id_dict[' '.join([dataframe.iloc[index, 1], dataframe.iloc[index, 19]])] == 0:
                self.goalie_season_id_dict[' '.join([dataframe.iloc[index, 1], dataframe.iloc[index, 19]])] = id
                goalie_season_id_dict_list.append(' '.join([dataframe.iloc[index, 1], dataframe.iloc[index, 19]]))
                id += 1
            else:
                goalie_season_id_dict_list.append(' '.join([dataframe.iloc[index, 1], dataframe.iloc[index, 19]]))
        dataframe['goalie_season_id_dict_list'] = goalie_season_id_dict_list

    def create_goalie_season(self):
        self.goalie_season = pandas.DataFrame(np.zeros(len(self.goalie_season_id_dict)))
        self.goalie_season['goalie_season_id_dict_list'] = self.goalie_season_id_dict.keys()
        self.goalie_season['wins'] = np.zeros(len(self.goalie_season))
        self.goalie_season['gamesPlayed'] = np.zeros(len(self.goalie_season))
        self.goalie_season['winPercentage'] = np.zeros(len(self.goalie_season))
        self.goalie_season['PPO'] = np.zeros(len(self.goalie_season))
        self.goalie_season['PPG'] = np.zeros(len(self.goalie_season))
        self.goalie_season['PKSaved'] = np.zeros(len(self.goalie_season))
        self.goalie_season['PKOPP'] = np.zeros(len(self.goalie_season))
        self.goalie_season['winPred'] = np.zeros(len(self.goalie_season))
        self.goalie_season['GF'] = np.zeros(len(self.goalie_season))
        self.goalie_season['GA'] = np.zeros(len(self.goalie_season))
        self.goalie_season['GAA'] = np.zeros(len(self.goalie_season))
        self.goalie_season['shots'] = np.zeros(len(self.goalie_season))
        self.goalie_season['saves'] = np.zeros(len(self.goalie_season))
        self.goalie_season['totalTOI'] = np.zeros(len(self.goalie_season))
        self.goalie_season['savePercentage'] = np.zeros(len(self.goalie_season))

        self.goalie_season.drop(0, axis=1, inplace=True)

    def goalie_stats_data_gather(self, goalie_season_id_index, goalie, season):
        goalie_stats_only_this_goalie = self.goalie_stats.loc[self.goalie_stats['player_id'] == goalie]
        for game_index, game in enumerate(goalie_stats_only_this_goalie['game_id']):
            if goalie_stats_only_this_goalie.iloc[game_index, 19] == season:
                # shots
                self.goalie_season.iloc[goalie_season_id_index, 12] += goalie_stats_only_this_goalie.iloc[game_index, 7]
                #saves
                self.goalie_season.iloc[goalie_season_id_index, 13] += goalie_stats_only_this_goalie.iloc[game_index, 8]
                #totalTOI
                self.goalie_season.iloc[goalie_season_id_index, 14] += goalie_stats_only_this_goalie.iloc[game_index, 3]
                #wins
                if goalie_stats_only_this_goalie.iloc[game_index, 15] == 'W':
                    self.goalie_season.iloc[goalie_season_id_index, 1] += 1
                self.goalie_season.iloc[goalie_season_id_index, 2] += 1
                # GA
                self.goalie_season.iloc[goalie_season_id_index, 10] += goalie_stats_only_this_goalie.iloc[game_index, 13] - goalie_stats_only_this_goalie.iloc[game_index, 11]
                # GF
                this_game = self.goalie_stats.loc[self.goalie_stats['game_id'] == game]
                this_game_other_goalie = this_game.loc[this_game['player_id'] != goalie]
                self.goalie_season.iloc[goalie_season_id_index, 9] += this_game_other_goalie['evenShotsAgainst'].sum() - this_game_other_goalie['evenSaves'].sum()

    def calculate_gaa(self, goalie_season_id_index):
        if self.goalie_season.iloc[goalie_season_id_index, 14]:
            self.goalie_season.iloc[goalie_season_id_index, 11] = ((self.goalie_season.iloc[goalie_season_id_index, 12] - self.goalie_season.iloc[goalie_season_id_index, 13]) * 3600) / self.goalie_season.iloc[goalie_season_id_index, 14]
        else:
            self.goalie_season.iloc[goalie_season_id_index, 11] = ((self.goalie_season.iloc[goalie_season_id_index, 12] - self.goalie_season.iloc[goalie_season_id_index, 13]) * 3600) / 1

    def calculate_save_percentage(self, goalie_season_id_index):
        self.goalie_season.iloc[goalie_season_id_index, 15] = self.goalie_season.iloc[goalie_season_id_index, 13] / self.goalie_season.iloc[goalie_season_id_index, 12]

    def calculate_win_stats(self, goalie_season_id_index):
        self.goalie_season.iloc[goalie_season_id_index, 3] = self.goalie_season.iloc[goalie_season_id_index, 1] / self.goalie_season.iloc[goalie_season_id_index, 2]

        self.calculate_gaa(goalie_season_id_index)

    def clean_up(self, season_column_list, goalie_column_list):
        self.goalie_season['season'] = season_column_list
        self.goalie_season['player_id'] = goalie_column_list
        self.goalie_season.loc[:,'season'] = self.goalie_season.season.astype(np.int)
        self.goalie_season.loc[:,'player_id'] = self.goalie_season.player_id.astype(np.int)
        self.goalie_season.loc[:,'totalTOI'] = self.goalie_season.totalTOI.astype(np.int)

    def fill_goalie_season(self):
        season_column_list = []; goalie_column_list = []
        for goalie_season_id_index, goalie_season_id in enumerate(self.goalie_season['goalie_season_id_dict_list']):
            [goalie, season] = str(goalie_season_id).split(' ')
            season_column_list.append(season); goalie_column_list.append(goalie)

            self.goalie_stats_data_gather(goalie_season_id_index, goalie, season)

            self.calculate_win_stats(goalie_season_id_index)

            self.calculate_save_percentage(goalie_season_id_index)

        self.clean_up(season_column_list, goalie_column_list)

    def graph_regplot(self):
        fig, ax = plt.subplots()
        sns.set(style="darkgrid")

        if self.mode == 'GAA':
            ax = sns.regplot(x='GAA', y='winPercentage',
                             data=self.goalie_season.loc[self.goalie_season['totalTOI'] > 3600*10],
                             marker='o', scatter_kws={'s': 13, 'alpha': 0.7, 'linewidths': 0.5},
                             line_kws={'lw': 1.4, 'color': '#4E73AE'})
            plt.annotate(('Correlation coeffiecient:' + '{0:.' + str(3)+ 'f}').format(self.goalie_season['winPercentage'].corr(self.goalie_season['GAA'])), (3.375,0.8), fontsize=7)
            plt.xlabel('GAA', fontsize=7);
            plt.xticks([1.6,2.0,2.4,2.8,3.2,3.6,4.0],
                       ['1.6','2.0','2.4','2.8','3.2','3.6','4.0'],
                       fontsize=6)
            plt.title('GAA vs. win percentage for every goaltender with over 10 hours played 2010-2019', fontsize=8)
        else:
            ax = sns.regplot(x='savePercentage', y='winPercentage',
                             data=self.goalie_season.loc[self.goalie_season['totalTOI'] > 3600*10],
                             marker='o', scatter_kws={'s': 13, 'alpha': 0.7, 'linewidths': 0.5},
                             line_kws={'lw': 1.4, 'color': '#4E73AE'})
            plt.xlabel('save percentage', fontsize=7);
            plt.xticks(fontsize=6)
            plt.annotate(('Correlation coeffiecient:' + '{0:.' + str(3)+ 'f}').format(self.goalie_season['winPercentage'].corr(self.goalie_season['savePercentage'])), (0.925,0.275), fontsize=7)
            plt.title('Save percentage vs. win percentage of each season for every goalie 2010-2019', fontsize=8)

        sns.set(style="darkgrid")
        plt.ylabel('win percentage', fontsize=7)
        plt.yticks(fontsize=6)
        self.check_dir_and_save(fig)

    def check_dir_and_save(self, fig):
        check_and_make_img_folder()
        if os.path.exists(self.figure_name):
            os.remove(self.figure_name)
        fig.savefig(self.figure_name, bbox_inches='tight', dpi=300)
