import os
import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'
from mpl_toolkits.mplot3d import Axes3D
import math
from matplotlib import animation
from graph_goals_after_giveaway_density import GraphGiveawayGoals


class GraphTimeDistanceGiveawayGoalsTrisurface(GraphGiveawayGoals):

    def __init__(self, subset='../data/extract_goals_with_giveaway.csv'):
        GraphGiveawayGoals.__init__(self)
        self.goals_and_giveaways = self.initialize_root_dataframe(subset)
        self.only_giveaway_goals = []
        self.writer = ''
        self.anim = ''

    def initialize_root_dataframe(self, subset):
        goals_and_giveaways = self.drop_na_row(self.import_csv(subset))
        goals_and_giveaways.columns = list(csv.reader(open('../data/goals_after_giveaway.csv')))[0]
        goals_and_giveaways = self.get_column_types(goals_and_giveaways, self.game_plays_dtypes)
        goals_and_giveaways = goals_and_giveaways.drop(goals_and_giveaways.loc[goals_and_giveaways['x'] == 'NA'].index)
        goals_and_giveaways = goals_and_giveaways.drop(goals_and_giveaways.loc[goals_and_giveaways['x'] == 'x'].index)

        goals_and_giveaways.loc[:,'x'] = goals_and_giveaways.x.astype(np.int)
        goals_and_giveaways.loc[:,'y'] = goals_and_giveaways.y.astype(np.int)
        goals_and_giveaways.loc[:,'st_x'] = goals_and_giveaways.st_x.astype(np.int)
        goals_and_giveaways.loc[:,'st_y'] = goals_and_giveaways.st_y.astype(np.int)
        goals_and_giveaways.loc[:,'periodTime'] = goals_and_giveaways.periodTime.astype(np.int)

        return goals_and_giveaways

    def get_sorted_only_giveaway_goals(self, distance_from_giveaway, time_from_giveaway):
        self.only_giveaway_goals = self.goals_and_giveaways.loc[self.goals_and_giveaways['event'] == 'Goal'].copy()
        self.only_giveaway_goals['distance_to_goal'] = distance_from_giveaway
        self.only_giveaway_goals['time_from_giveaway'] = time_from_giveaway

        self.only_giveaway_goals = self.only_giveaway_goals.loc[self.only_giveaway_goals['time_from_giveaway'] < 60]
        self.only_giveaway_goals.sort_values(by=['time_from_giveaway', 'distance_to_goal'], ascending=True, inplace=True)


    def get_time_and_distance(self, max_time=60):
        distance_from_giveaway = []; time_from_giveaway = []

        for index, _ in enumerate(self.goals_and_giveaways['play_id']):
            if self.goals_and_giveaways.iloc[index, 5] == 'Goal':
                distance_from_giveaway += [math.sqrt((-100 - self.goals_and_giveaways.iloc[index-1, 17])**2 +
                                                     (self.goals_and_giveaways.iloc[index-1, 18])**2)]

                if self.goals_and_giveaways.iloc[index, 11] - self.goals_and_giveaways.iloc[index-1, 11] > 0:
                    time_difference = self.goals_and_giveaways.iloc[index, 11] - self.goals_and_giveaways.iloc[index-1, 11]
                else:
                    time_difference = 0
                time_from_giveaway += [time_difference]

        self.get_sorted_only_giveaway_goals(distance_from_giveaway, time_from_giveaway)

        return self.only_giveaway_goals

    def get_time_distance_count(self):
        time_distance_count = defaultdict(int)
        for index, time in enumerate(self.only_giveaway_goals['time_from_giveaway']):
            distance = self.only_giveaway_goals.iloc[index, 20]
            box_number=0
            while(distance > box_number):
                box_number += 10
            if box_number == 10:
                time_distance_count[' '.join([str(time), '0'])] = 0
            time_distance_count[' '.join([str(round(time)), str(round(box_number))])] += 1

        return time_distance_count

    def fill_dimensional_arrays(self):
        time_distance_count_array = []; distance_array = []; time_array = []
        time_distance_count = self.get_time_distance_count()
        for key in time_distance_count.keys():
            [time, distance] = key.split(' ')
            time_array += [round(float(time))]
            distance_array += [round(float(distance))]
            time_distance_count_array += [time_distance_count[key]]

        return [time_array, distance_array, time_distance_count_array]

    def create_density_plot(self, xlabel, ylabel, title):
        fig = plt.figure(dpi=300); ax = fig.gca(projection='3d'); i=0
        self.writer = animation.FFMpegFileWriter()
        [time_array,
         distance_array,
         time_distance_count_array] = self.fill_dimensional_arrays()

        def init():
            ax.plot_trisurf(time_array,
                            distance_array,
                            time_distance_count_array, cmap=plt.cm.jet, linewidth=0.01)
            return fig,
        def animate(i):
            ax.view_init(elev=10., azim=i)
            return fig,

        plt.xlabel(xlabel); plt.ylabel(ylabel)
        plt.title(title)

        # Animate
        self.anim = animation.FuncAnimation(fig, animate, init_func=init,
                                       frames=360, interval=20, blit=True)

    def save_plot(self, plot_file_name):
        checkAndMakeImgFolder()
        if os.path.exists(plot_file_name):
            os.remove(plot_file_name)
        self.anim.save(plot_file_name, writer=self.writer)

    # make plot and save file
    def create_and_save_plot(self, xlabel, ylabel, title, plot_file_name):
        self.create_density_plot(xlabel, ylabel, title)
        self.save_plot(plot_file_name)
