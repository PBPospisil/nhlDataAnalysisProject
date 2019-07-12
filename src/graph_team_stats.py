`import os
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
import seaborn as sns; sns.set()
from linear_model import LinearModel
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
from graph_model import GraphModel


class GraphTeamStats(GraphModel):
    def __init__(self):
        GraphModel.__init__(self)

    def create_team_stats_regplot(self):
        plt.figure(figsize=(12, 9))
        plt.title('Win% vs. GAA for goalies with > 60 GP from 2010-2019')
        plt.annotate('Correlation coefficient: ' + ('{0:.' + str(3) + 'f}').format(self.team_season['GAA'].corr(self.team_season['winPercentage'])), xy=(0.65, 0.95), xycoords='axes fraction')
        sns.regplot(x="GAA", y="winPercentage", data=self.team_season)
        plt.xlabel('GAA'); plt.ylabel("win percentage")

    def save_plot(self):
        check_and_make_img_folder()
        if os.path.exists('../img/gaa-win-percentage-regplot.png'):
            os.remove('../img/gaa-win-percentage-regplot.png')
        plt.savefig('../img/gaa-win-percentage-regplot.png', bbox_inches='tight', dpi=300)

    def create_plot_and_save(self):
        self.create_team_stats_regplot()
        self.save_plot()

    def games_played_minimum(self, min_games):
        self.team_season = self.team_season.drop(self.team_season.loc[self.team_season['gamesPlayed'] < min_games].index)
