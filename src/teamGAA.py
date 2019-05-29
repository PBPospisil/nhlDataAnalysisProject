import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF_largeFile import csvToDF_largeFile
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from get_goalie_to_subtractGAA_from_csv import extractFromCsv
from scipy.stats import norm
from math import sqrt
import sys

team_info = csvToDF('../team_info.csv')
goalie_stats_df = csvToDF('../game_goalie_stats.csv')
games_df = csvToDF('../game.csv')

print('\n\nTeam --- ID\n')
for index, team in enumerate(team_info['team_id']):
    print(team_info.iloc[index,2] + ' ' + team_info.iloc[index,3] + ' --- ' + team)

main_team = str(input('\nEnter the team ID to view a specific team chart: '))
abbr_main_team = team_info.loc[team_info['team_id'] == main_team, 'abbreviation'].item()
short_name_main_team = team_info.loc[team_info['team_id'] == main_team, 'shortName'].item()
team_name_main_team = team_info.loc[team_info['team_id'] == main_team, 'teamName'].item()

goalie_stats_df.loc[:,'evenShotsAgainst'] = goalie_stats_df.evenShotsAgainst.astype(np.float)
goalie_stats_df.loc[:,'evenSaves'] = goalie_stats_df.evenSaves.astype(np.float)
goalie_stats_df.loc[:,'timeOnIce'] = goalie_stats_df.timeOnIce.astype(np.float)
goalie_stats_df.loc[:,'game_id'] = goalie_stats_df.game_id.astype(np.int)
goalie_stats_df = goalie_stats_df.sort_values(['game_id'], ascending=True)

teamGAA_df = pandas.DataFrame(np.array(goalie_stats_df['team_id']))
teamGAA_df.columns = ['team_id']

GAA = []
TOI = []
game_id = []
currTOI = defaultdict(int)
currShotsAgainst = defaultdict(int)
currSavesFor = defaultdict(int)

for index, team in enumerate(teamGAA_df['team_id']):
    currShotsAgainst[team] += goalie_stats_df.iloc[index, 13]
    currSavesFor[team] += goalie_stats_df.iloc[index, 11]
    currTOI[team] += goalie_stats_df.iloc[index, 3] / 3600
    GAA += [(currShotsAgainst[team] - currSavesFor[team]) / currTOI[team]]
    TOI += [currTOI[team]]
    gameID = goalie_stats_df.iloc[index, 0]
    game_id += [gameID]

teamGAA_df['game_id'] = game_id
teamGAA_df['GAA'] = GAA
teamGAA_df['TOI'] = TOI

masterTeam = teamGAA_df.loc[teamGAA_df['team_id'] == main_team]
lastDate = masterTeam.iloc[len(masterTeam['game_id'])-1, 3]
if lastDate > 500:
    lastDate = 500
ticks = [50,100,200,300,400,lastDate]
labels_ = []
for tick in ticks:
    for index, game in enumerate(masterTeam['game_id']):
        labelGame = masterTeam.iloc[index, 3]
        if abs(labelGame - tick) < 1 :
            labels_ += [games_df.loc[games_df['game_id'] == str(game), 'date_time'].item()]
            break

teamColors = {'1':'red', '4':'darkorange', '26':'black', '14':'blue', '6':'yellow',
            '3':'blue', '5':'yellow', '17':'red', '28':'darkcyan', '18':'yellow',
             '23':'blue', '16':'red', '9':'red', '8':'red', '30':'green',
              '15':'red', '19':'blue', '24':'orange', '27':'maroon', '2':'orange',
               '20':'red', '21':'maroon', '25':'green', '13':'red', '10':'blue',
                '29':'blue', '52':'blue', '54':'yellow', '12':'red', '7':'blue',
                 '22':'orange', '53':'maroon', '11':'blue'}

plt.plot('TOI', 'GAA', data=teamGAA_df.loc[teamGAA_df['team_id'] == main_team], label=abbr_main_team, color=teamColors[main_team], zorder=30)
plt.legend()
for team in teamGAA_df['team_id'].unique():
    if team != main_team:
        plt.plot('TOI', 'GAA', data=teamGAA_df.loc[teamGAA_df['team_id'] == team], color='grey')

plt.ylim(1.4,2.4)
plt.xticks(ticks, labels_, fontsize=6)
plt.xlim(50, 550)
plt.ylabel('GAA')
plt.xlabel('Game Date')
plt.title('GAA vs. Time with focus on ' + short_name_main_team + ' ' + team_name_main_team + ' from 2013-2018')
plt.show()

#
