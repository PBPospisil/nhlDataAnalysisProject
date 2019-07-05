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


class GraphData(object):

    def __init__(self):

        self.team_info_dtypes = {'team_id':'str', 'franchiseId':'str',
                                 'shortName':'str', 'teamName':'str',
                                 'abbreviation':'str', 'link':'str'}

        self.goalie_stats_dtypes = {'game_id':'str', 'player_id':'str',
                                    'team_id':'str', 'timeOnIce':'int',
                                    'assists':'int', 'goals':'int',
                                    'pim':'int', 'shots':'int', 'saves':'int',
                                    'powerPlaySaves':'int', 'shortHandedSaves':'int',
                                    'evenSaves':'int', 'shortHandedShotsAgainst':'int',
                                    'evenShotsAgainst':'int', 'powerPlayShotsAgainst':'int',
                                    'decision':'str', 'savePercentage':'float',
                                    'powerPlaySavePercentage':'float',
                                    'evenStrengthSavePercentage':'float'}

        self.game_dtypes = {'game_id':'str', 'season':'str', 'type':'str', 'date_time':'str',
                            'away_team_id':'str', 'home_team_id':'str', 'away_goals':'int',
                            'home_goals':'int', 'outcome':'str', 'home_rink_side_start':'str',
                            'venue':'str', 'venue_link':'str', 'venue_time_zone_id':'str',
                            'venue_time_zone_offset':'str', 'venue_time_zone_tz':'str'}

        self.team_stats_dtypes = {'game_id':'str', 'team_id':'str', 'HoA':'str', 'won':'str',
                                  'settled_in':'str', 'head_coach':'str', 'goals':'int',
                                  'shots':'int', 'hits':'int', 'pim':'int',
                                  'powerPlayOpportunities':'int', 'powerPlayGoals':'int',
                                  'faceOffWinPercentage':'float', 'giveaways':'int',
                                  'takeaways':'int'}

        self.player_info_dtypes = {'player_id':'str', 'firstName':'str', 'lastName':'str', 'nationality':'str',
                                  'birthCity':'str', 'primaryPosition':'str', 'birthDate':'str',
                                  'link':'str'}

        self.game_plays_dtypes = {'play_id':'str', 'game_id':'str', 'play_num':'int',
                                  'team_id_for':'str', 'team_id_against':'str',
                                  'event':'str', 'secondaryType':'str', 'x':'str', 'y':'str',
                                  'period':'int', 'periodType':'str', 'periodTime':'int',
                                  'periodTimeRemaining':'int', 'dateTime':'str', 'goals_away':'int',
                                  'goals_home':'int', 'description':'str', 'st_x':'str', 'st_y':'str',
                                  'rink_side':'str'}

    def import_csv(self, csv_name):
        return csv_to_df(csv_name)

    def drop_na_row(self, dataframe):
        for column in dataframe.columns.values[17:19]:
            dataframe.drop(dataframe.loc[dataframe[column] == 'NA'].index, inplace=True)
        return dataframe

    def get_column_types(self, dataframe, csv_dtypes):
        return dataframe.astype(csv_dtypes)
