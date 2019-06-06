import os
import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import norm
from math import sqrt
import sys

teamInfo = csvToDF('../data/teamInfo.csv')
goalieStatsDF = csvToDF('../data/game_goalie_stats.csv')
gamesDF = csvToDF('../data/game.csv')

print('\n\nTeam --- ID\n')
for index, team in enumerate(teamInfo['team_id']):
    print(teamInfo.iloc[index,2] + ' ' + teamInfo.iloc[index,3] + ' --- ' + team)

mainTeam = str(input('\nEnter the team ID to view a specific team chart: '))
abbrMainTeam = teamInfo.loc[teamInfo['team_id'] == mainTeam, 'abbreviation'].item()
shortNameMainTeam = teamInfo.loc[teamInfo['team_id'] == mainTeam, 'shortName'].item()
teamNameMainTeam = teamInfo.loc[teamInfo['team_id'] == mainTeam, 'teamName'].item()

goalieStatsDF.loc[:,'evenShotsAgainst'] = goalieStatsDF.evenShotsAgainst.astype(np.float)
goalieStatsDF.loc[:,'evenSaves'] = goalieStatsDF.evenSaves.astype(np.float)
goalieStatsDF.loc[:,'timeOnIce'] = goalieStatsDF.timeOnIce.astype(np.float)
goalieStatsDF.loc[:,'game_id'] = goalieStatsDF.game_id.astype(np.int)
goalieStatsDF = goalieStatsDF.sort_values(['game_id'], ascending=True)

teamGAA_df = pandas.DataFrame(np.array(goalieStatsDF['team_id']))
teamGAA_df.columns = ['team_id']

GAA = []
TOI = []
game_id = []
currTOI = defaultdict(int)
currShotsAgainst = defaultdict(int)
currSavesFor = defaultdict(int)

for index, team in enumerate(teamGAA_df['team_id']):
    currShotsAgainst[team] += goalieStatsDF.iloc[index, 13]
    currSavesFor[team] += goalieStatsDF.iloc[index, 11]
    currTOI[team] += goalieStatsDF.iloc[index, 3] / 3600
    GAA += [(currShotsAgainst[team] - currSavesFor[team]) / currTOI[team]]
    TOI += [currTOI[team]]
    gameID = goalieStatsDF.iloc[index, 0]
    game_id += [gameID]

teamGAA_df['game_id'] = game_id
teamGAA_df['GAA'] = GAA
teamGAA_df['TOI'] = TOI

masterTeam = teamGAA_df.loc[teamGAA_df['team_id'] == mainTeam]
lastDate = masterTeam.iloc[len(masterTeam['game_id'])-1, 3]
if lastDate > 500:
    lastDate = 500
ticks = [50,100,200,300,400,lastDate]
labels_ = []
for tick in ticks:
    for index, game in enumerate(masterTeam['game_id']):
        labelGame = masterTeam.iloc[index, 3]
        if abs(labelGame - tick) < 1 :
            labels_ += [gamesDF.loc[gamesDF['game_id'] == str(game), 'date_time'].item()]
            break

teamColors = {'1':'red', '4':'darkorange', '26':'black', '14':'blue', '6':'yellow',
            '3':'blue', '5':'yellow', '17':'red', '28':'darkcyan', '18':'yellow',
             '23':'blue', '16':'red', '9':'red', '8':'red', '30':'green',
              '15':'red', '19':'blue', '24':'orange', '27':'maroon', '2':'orange',
               '20':'red', '21':'maroon', '25':'green', '13':'red', '10':'blue',
                '29':'blue', '52':'blue', '54':'yellow', '12':'red', '7':'blue',
                 '22':'orange', '53':'maroon', '11':'blue'}

plt.plot('TOI', 'GAA', data=teamGAA_df.loc[teamGAA_df['team_id'] == mainTeam], label=abbrMainTeam, color=teamColors[mainTeam], zorder=30)
plt.legend()
for team in teamGAA_df['team_id'].unique():
    if team != mainTeam:
        plt.plot('TOI', 'GAA', data=teamGAA_df.loc[teamGAA_df['team_id'] == team], color='grey')

plt.ylim(1.4,2.4)
plt.xticks(ticks, labels_, fontsize=6)
plt.xlim(50, 550)
plt.ylabel('GAA')
plt.xlabel('Game Date')
plt.title('GAA vs. Time with focus on ' + shortNameMainTeam + ' ' + teamNameMainTeam + ' from 2013-2018')

checkAndMakeImgFolder()

if os.path.exists('../img/team-gaa-' + shortNameMainTeam):
    os.remove('../img/team-gaa-' + shortNameMainTeam)
plt.savefig('../img/team-gaa-' + shortNameMainTeam, bbox_inches='tight')

#
