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


playerInfo = csvToDF("../data/player_info.csv")
goalieStatsDF = csvToDF('../data/game_goalie_stats.csv')

goalieStatsDF.loc[:,'game_id'] = goalieStatsDF.game_id.astype(np.int)
goalieStatsDF.loc[:,'timeOnIce'] = goalieStatsDF.timeOnIce.astype(np.float)
goalieStatsDF = goalieStatsDF.sort_values(['game_id'], ascending=True)

timeOnIce = []

allGoaliesSV = pandas.DataFrame(np.array(goalieStatsDF['player_id'].unique()))
allGoaliesSV.columns = ['player_id']
for player in allGoaliesSV['player_id']:
    TOI = goalieStatsDF.loc[goalieStatsDF['player_id'] == player, 'timeOnIce'].sum()
    timeOnIce += [TOI]

allGoaliesSV['timeOnIce'] = timeOnIce
allGoaliesSV.loc[:,'timeOnIce'] = allGoaliesSV.timeOnIce.astype(np.float)

sortedByTOI = allGoaliesSV.sort_values(['timeOnIce'], ascending=False)
sortedByTOI.loc[:,'player_id'] = sortedByTOI.player_id.astype(np.float)

top10 = 0
playerID = []
accumTOI = []
accumSV = []

for player in sortedByTOI['player_id'][:10]:
    player = str(int(sortedByTOI.iloc[top10,0]))
    playerStats = goalieStatsDF.loc[goalieStatsDF['player_id'] == player].copy()
    playerStats.loc[:,'shots'] = playerStats.shots.astype(np.float)
    playerStats.loc[:,'saves'] = playerStats.saves.astype(np.float)

    TOIsum = 0
    totalShots = 0
    totalSaves = 0
    for game in playerStats['game_id']:
        playerID += [player]
        TOIsum += playerStats.loc[playerStats['game_id'] == game, 'timeOnIce'].item()
        totalShots += playerStats.loc[playerStats['game_id'] == game, 'shots'].item()
        totalSaves += playerStats.loc[playerStats['game_id'] == game, 'saves'].item()

        accumTOI += [TOIsum/3600]
        accumSV += [totalSaves / totalShots]
    top10 += 1

topTenToiWithAccumSvPercentage = pandas.DataFrame(np.array(playerID))
topTenToiWithAccumSvPercentage.columns = ['player_id']
topTenToiWithAccumSvPercentage['timeOnIce'] = accumTOI
topTenToiWithAccumSvPercentage['savePercentage'] = accumSV

plt.figure(figsize=(12, 9))
for player in topTenToiWithAccumSvPercentage['player_id'].unique():
    name = playerInfo.loc[playerInfo['player_id'] == player, 'firstName'].item()+ ' ' + playerInfo.loc[playerInfo['player_id'] == player, 'lastName'].item()
    plt.plot('timeOnIce', 'savePercentage', data=topTenToiWithAccumSvPercentage.loc[topTenToiWithAccumSvPercentage['player_id'] == player], label=name)
    plt.ylim(0.88,0.95)

plt.xlabel('time played')
plt.ylabel('save percentage')
plt.title('Save percentage over dataset for top 10 player goaltenders from 2010-2019')
plt.legend()

checkAndMakeImgFolder()

if os.path.exists('../img/lineplot-goalies-top10-minutes-save-percentage.png'):
    os.remove('../img/lineplot-goalies-top10-minutes-save-percentage.png')
plt.savefig('../img/lineplot-goalies-top10-minutes-save-percentage.png', bbox_inches='tight', dpi=300)
