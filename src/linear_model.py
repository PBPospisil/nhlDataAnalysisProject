import os
import pandas
import numpy as np
import csv
from csv_to_df import csv_to_df
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import norm
import sys
import time
from graph_data import GraphData
import seaborn as sns; sns.set()


class LinearModel(GraphData):

    def __init__(self, dataframe):
        GraphData.__init__(self)
        self.beta_, self.alpha_ = self.regression_line_calc(dataframe)
        self.gameID = []; self.cummgamesPlayed = []; self.cummWins = []; self.cummGF = []; self.cummGA = [];
        self.predWinPercentage = []; self.actualWinPercentage = [];
        self.absolute_error = []; self.average_error = []
        self.predWinPercentage_gfga = [];
        self.prevGame = self.GAsum = self.GFsum = self.GPsum = self.gamesWinSum = 0
        self.goalie_by_season = []; self.gfga = []


    def regression_line_calc(cls, dataframe):
        meanWinPred = dataframe['winPred'].mean()
        meanWinPercentage = dataframe['winPercentage'].mean()
        stdWinPred = dataframe['winPred'].std()
        stdWinPercentage = dataframe['winPercentage'].std()
        n = dataframe['winPred'].count()
        sum_xy = 0

        for index, x in enumerate(dataframe['winPred']):
            sum_xy += (x * dataframe.iloc[index, 3])
        beta = (sum_xy - n * meanWinPred * meanWinPercentage) / ((n-1) * stdWinPred**2)
        alpha = meanWinPercentage - beta * meanWinPred
        return beta, alpha


    def sum_gf_ga_wins(self, game, index, team_of_interest):
        teamsInGame = []
        for team in self.goalie_by_season.loc[self.goalie_by_season['game_id'] == game, 'team_id']:
            if team == team_of_interest and self.goalie_by_season.iloc[index, 15] == 'W' and team not in teamsInGame:
                self.gamesWinSum += 1
            elif team == team_of_interest and team not in teamsInGame:
                self.GAsum += (self.goalie_by_season.iloc[index, 13] - self.goalie_by_season.iloc[index, 11])
            elif team == team_of_interest and team in teamsInGame:
                self.GAsum += (self.goalie_by_season.iloc[index, 13] - self.goalie_by_season.iloc[index, 11])
            elif team != team_of_interest:
                self.GFsum += (self.goalie_by_season.iloc[index, 13] - self.goalie_by_season.iloc[index, 11])
            teamsInGame.append(team)

    def make_interval_calculations(self, current_alpha, team_of_interest, season):
        self.cummGA.append(self.GAsum); self.cummGF.append(self.GFsum)
        self.cummWins.append(self.gamesWinSum); self.cummgamesPlayed.append(self.GPsum)
        self.GAsum = self.GAsum or 1
        self.actualWinPercentage.append(self.gamesWinSum / self.GPsum)
        self.predWinPercentage.append(self.alpha_ + self.beta_ * (self.GFsum / self.GAsum)*current_alpha)
        self.predWinPercentage_gfga.append(self.alpha_ + self.beta_ * (self.GFsum / self.GAsum)*0.8)
        self.absolute_error.append(abs(self.predWinPercentage[-1] - self.actualWinPercentage[-1]))
        self.average_error.append(sum(self.absolute_error) / len(self.absolute_error))
        self.gfga.append(self.GFsum/self.GAsum)

        self.gameID.append(self.GPsum)


    def sse_calc(self, sse, absolute_error_):
        if len(self.actualWinPercentage) != 0 and len(self.predWinPercentage) != 0:
            sse += (self.predWinPercentage[-1]-self.actualWinPercentage[-1])**2
            absolute_error_.append(self.predWinPercentage[-1]-self.actualWinPercentage[-1])
        return [sse, absolute_error_]


    def create_win_prediction_model(self):
        win_prediction_model = pandas.DataFrame(np.array(self.gameID), columns=['game_id'])
        win_prediction_model['predWinPercentage'] = self.predWinPercentage
        win_prediction_model['predWinPercentage_gfga'] = self.predWinPercentage_gfga
        win_prediction_model['actualWinPercentage'] = self.actualWinPercentage
        win_prediction_model['absolute_error'] = self.absolute_error
        win_prediction_model['average_error'] = self.average_error
        win_prediction_model['gfga'] = self.gfga
        return win_prediction_model


    def team_prediction_lineplot(self, goalie_stats, team_of_interest, absolute_error_, sse, current_alpha, season=20152016):

        self.goalie_by_season = goalie_stats.loc[goalie_stats['season'] == season].copy()
        self.goalie_by_season.loc[:,'game_id'] = self.goalie_by_season.game_id.astype(np.int)
        self.goalie_by_season = self.goalie_by_season.sort_values('game_id', ascending=True, inplace=False)

        for index, game in enumerate(self.goalie_by_season.loc[self.goalie_by_season['team_id'] == team_of_interest, 'game_id'].unique()):
            self.GPsum += 1
            self.sum_gf_ga_wins(game, index, team_of_interest)
            self.make_interval_calculations(current_alpha, team_of_interest, season)
            if self.GPsum > 40:
                [sse, absolute_error_] = self.sse_calc(sse, absolute_error_)

        return self.create_win_prediction_model(), [sse, absolute_error_], self.GPsum
