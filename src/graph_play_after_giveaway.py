import os
import pandas
import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict
from graph_data import GraphData


class GraphPlayAfterGiveaway(GraphData):

    def __init__(self):
        GraphData.__init__(self)
        self.game_play_after_giveaway = self.initialize_root_dataframes()

    def initialize_root_dataframes(self):
        game_play_after_giveaway = self.get_column_types(self.drop_na_row(self.import_csv('../data/play_after_GA.csv')),
                              self.game_plays_dtypes)

        return game_play_after_giveaway

    def get_event_frequency(self):
        event_after_giveaway_count = defaultdict(int)
        for event in self.game_play_after_giveaway['event']:
            event_after_giveaway_count[event] += 1
        return event_after_giveaway_count

    def create_barplot(self):
        plt.figure(figsize=(12, 9)); plt.xlabel('type of play'); plt.ylabel('count')
        plt.title('Barplot of the next play after a giveaway')

        event_after_giveaway_count = self.get_event_frequency()
        sns.barplot(x=np.array(list(event_after_giveaway_count.keys()))[:11],
                    y=np.array(list(event_after_giveaway_count.values())).astype(float)[:11])

    def save_plot(self, plot_file_name):
        checkAndMakeImgFolder()
        if os.path.exists(plot_file_name):
            os.remove(plot_file_name)
        plt.savefig(plot_file_name, bbox_inches='tight', dpi=300)

    # make plot and save file
    def create_and_save_plot(self):
        self.create_barplot()
        self.save_plot('../img/next-play-after-giveaway-barplot.png')
