import pandas
import numpy as np
import csv
from csv_to_df import csv_to_df
from csv_to_df import check_and_make_img_folder
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import os
from graph_data import GraphData

class GraphGiveawayGoals(GraphData):

    def __init__(self, subset='../data/goals_after_giveaway.csv'):
        GraphData.__init__(self)
        self.sorted_by_play_id = self.initialize_root_dataframe(subset)
        self.giveaway_index = self.period = self.game_id = self.time_of_giveaway = 0
        self.play_num = self.team_gaining_possession = 0
        self.goals_after_giveaway_count = []; self.time_differences_list = [];
        self.play_id_to_extract = []
        self.previous_is_giveaway = False

    def initialize_root_dataframe(self, subset):
        goals_after_giveaway = self.get_column_types(self.drop_na_row(self.import_csv(subset)),
                              self.game_plays_dtypes)
        goals_after_giveaway.loc[:,'game_id'] = goals_after_giveaway.game_id.astype(np.int)
        sorted_by_play_id = goals_after_giveaway.sort_values(['game_id', 'play_num'])

        return sorted_by_play_id

    def is_giveaway(self, index):
        self.giveaway_index = index; self.previous_is_giveaway = True
        self.period = self.sorted_by_play_id.iloc[index,9];
        self.game_id = self.sorted_by_play_id.iloc[index,1]
        self.time_of_giveaway = int(self.sorted_by_play_id.iloc[index,11]);
        self.play_num = int(self.sorted_by_play_id.iloc[index,2])
        self.team_gaining_possession = self.sorted_by_play_id.iloc[index,4]

    def is_goal(self, index):
        self.goals_after_giveaway_count += [int(self.sorted_by_play_id.iloc[index,2]) - self.play_num]
        self.time_differences_list += [int(self.sorted_by_play_id.iloc[index,11]) - self.time_of_giveaway]
        self.previous_is_giveaway = False
        self.play_id_to_extract +=[self.sorted_by_play_id.iloc[self.giveaway_index,:]]
        self.play_id_to_extract +=[self.sorted_by_play_id.iloc[index,:]]

    def is_this_goal_after_giveaway(self, index):
        return (self.sorted_by_play_id.iloc[index,5] == 'Goal'
                and self.previous_is_giveaway is True
                and self.period == self.sorted_by_play_id.iloc[index,9]
                and self.game_id == self.sorted_by_play_id.iloc[index,1]
                and self.sorted_by_play_id.iloc[index,3] == self.team_gaining_possession)

    # get count, time after and play of goal scored after giveaway
    def get_giveaway_stats(self):
        for index, _ in enumerate(self.sorted_by_play_id['game_id']):
            if self.sorted_by_play_id.iloc[index,5] == 'Giveaway':
                self.is_giveaway(index)
            elif self.sorted_by_play_id.iloc[index,5] == 'Stoppage':
                self.previous_is_giveaway = False
            elif self.is_this_goal_after_giveaway(index):
                self.is_goal(index)

    # save all goals after giveaway
    def save_giveaway_goal_csv(self):
        if os.path.exists('../data/extract_goals_with_giveaway.csv'):
            os.remove('../data/extract_goals_with_giveaway.csv')
        goals_and_giveaways = pandas.DataFrame(np.array(self.play_id_to_extract))
        goals_and_giveaways.to_csv('../data/extract_goals_with_giveaway.csv', index=False, sep=',', encoding='utf-8', mode='a')
        goals_and_giveaways.columns = self.sorted_by_play_id.columns

    def create_density_plot(self, xlabel, ylabel, title, mode='time'):
        if mode == 'time':
            a = self.time_differences_list
        elif mode == 'count':
            a = self.goals_after_giveaway_count

        plt.figure(figsize=(12, 9))
        ax = sns.distplot(a=a, hist=True, kde=True,
                          color='darkblue', hist_kws={'edgecolor':'black'},
                          kde_kws={'linewidth': 4})
        plt.xlabel(xlabel); plt.ylabel(ylabel)
        plt.title(title)

    def save_plot(self, plot_file_name):
        check_and_make_img_folder()
        if os.path.exists(plot_file_name):
            os.remove(plot_file_name)
        plt.savefig(plot_file_name, bbox_inches='tight', dpi=300)

    # make plot and save file
    def create_and_save_plot(self, xlabel, ylabel, title, plot_file_name, mode):
        self.create_density_plot(xlabel, ylabel, title, mode)
        self.save_plot(plot_file_name)
