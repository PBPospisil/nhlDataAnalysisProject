import os
import pandas
import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from csv_to_df import csv_to_df
from csv_to_df import check_and_make_img_folder
from collections import defaultdict
from graph_data import GraphData


class GraphJointplot(GraphData):

    def __init__(self):
        GraphData.__init__(self)
        self.goals = self.initialize_root_dataframe()

    def initialize_root_dataframe(self):
        goals = self.get_column_types(self.drop_na_row(self.import_csv('../data/goals.csv')),
                              self.game_plays_dtypes)
        goals = goals.drop(goals.loc[goals['x'] == 'NA'].index)
        goals = goals.drop(goals.loc[goals['x'] == 'x'].index)
        goals = goals.drop(goals.loc[goals['secondaryType'] == 'x'].index)
        goals = goals.drop(goals.loc[goals['secondaryType'] == 'NA'].index)

        goals.loc[:,'x'] = goals.x.astype(np.float)
        goals.loc[:,'y'] = goals.y.astype(np.float)

        return goals

    def create_barplot(self, goal_type):
        ax = sns.jointplot(x='x', y='y', data=self.goals.loc[self.goals['secondaryType'] == goal_type],
                      kind='kde', color='r', xlim=(-100,100), ylim=(-42.5,42.5),
                      height=11.7)
        ax.set_axis_labels('x coordinate', 'y coordinate')
        ax.fig.suptitle('location of' + str(goal_type).lower() + 'goals scored',
                        x='0.5', y='1.0', fontsize='16')

    def save_plot(self, plot_file_name):
        check_and_make_img_folder(jointplot=True)
        if os.path.exists(plot_file_name):
            os.remove(plot_file_name)
        plt.savefig(plot_file_name, bbox_inches='tight', dpi=300)

    # make plot and save file
    def create_and_save_plot(self, goal_type):
        self.create_barplot(goal_type)
        self.save_plot('../img/joinplots/jointplot-' +
                       '-'.join(goal_type.lower().split(' ')) + '-joinplots.png')

    def create_all_plots(self):
        for goal_type in self.goals['secondaryType'].unique():
            self.create_and_save_plot(goal_type)
