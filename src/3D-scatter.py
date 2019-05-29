import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt


goalieStatsDF = csvToDF('../game_goalie_stats.csv')
gameDF = csvToDF('../game.csv')
playersDF = csvToDF('../player_info.csv')

goalieStatsDF.loc[:,'timeOnIce'] = goalieStatsDF.timeOnIce.astype(np.int)

seasons = []
playerSeasonIdList = []
ID = 1
playerSeasonIdDict = defaultdict(int)

for game in goalieStatsDF['game_id']:
    seasons.append(gameDF.loc[gameDF['game_id'] == game, 'season'])

goalieStatsDF['season'] = seasons

for index, _ in enumerate(goalieStatsDF['game_id']):

    if playerSeasonIdDict[' '.join([goalieStatsDF.iloc[index, 1], goalieStatsDF.iloc[index, 19].item()])] == 0:
        playerSeasonIdDict[' '.join([goalieStatsDF.iloc[index, 1], goalieStatsDF.iloc[index, 19].item()])] = ID
        playerSeasonIdList.append(ID)
        ID += 1
    else:
        playerSeasonIdList.append(playerSeasonIdDict[' '.join([goalieStatsDF.iloc[index, 1], goalieStatsDF.iloc[index, 19].item()])])

goalieStatsDF['playerSeasonIdList'] = playerSeasonIdList

goalieStatsDF = goalieStatsDF.drop(goalieStatsDF.loc[goalieStatsDF['savePercentage'] == 'NA'].index)

goalieStatsDF.loc[:,'savePercentage'] = goalieStatsDF.savePercentage.astype(np.float)
goalieStatsDF.loc[:,'shots'] = goalieStatsDF.shots.astype(np.int)
goalieStatsDF.loc[:,'saves'] = goalieStatsDF.saves.astype(np.int)

oneSeasonEntire = pandas.DataFrame(np.zeros(len(playerSeasonIdDict)))

oneSeasonEntire['playerSeasonIdList'] = playerSeasonIdDict.keys()
oneSeasonEntire['totalTOI'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['wins'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['GAA'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['savePercentage'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['gamesPlayed'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['winPercentage'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['shots'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['saves'] = np.zeros(len(oneSeasonEntire))

oneSeasonEntire.drop(0, axis=1, inplace=True)

for outerIndex, playerSeason in enumerate(oneSeasonEntire['playerSeasonIdList']):
    [player, season] = str(playerSeason).split(' ')
    playerSpecific = goalieStatsDF.loc[goalieStatsDF['player_id'] == player]
    for innerIndex, _ in enumerate(playerSpecific['game_id']):
        if playerSpecific.iloc[innerIndex, 19].item() == season:
            # shots
            oneSeasonEntire.iloc[outerIndex, 7] += playerSpecific.iloc[innerIndex, 7]
            #saves
            oneSeasonEntire.iloc[outerIndex, 8] += playerSpecific.iloc[innerIndex, 8]
            #totalTOI
            oneSeasonEntire.iloc[outerIndex, 1] += playerSpecific.iloc[innerIndex, 3]
            #wins
            if playerSpecific.iloc[innerIndex, 15] == 'W':
                oneSeasonEntire.iloc[outerIndex, 2] += 1
            oneSeasonEntire.iloc[outerIndex, 5] += 1
    oneSeasonEntire.iloc[outerIndex, 3] = ((oneSeasonEntire.iloc[outerIndex, 7] - oneSeasonEntire.iloc[outerIndex, 8]) * 3600) / oneSeasonEntire.iloc[outerIndex, 1]
    if oneSeasonEntire.iloc[outerIndex, 7] != 0:
        oneSeasonEntire.iloc[outerIndex, 4] = int(oneSeasonEntire.iloc[outerIndex, 8]) / int(oneSeasonEntire.iloc[outerIndex, 7])
    oneSeasonEntire.iloc[outerIndex, 6] = oneSeasonEntire.iloc[outerIndex, 2] / oneSeasonEntire.iloc[outerIndex, 5]

oneSeasonEntire = oneSeasonEntire.drop(oneSeasonEntire.loc[oneSeasonEntire['gamesPlayed'] < 60].index)
oneSeasonEntire = oneSeasonEntire.reset_index(drop=True)
print(oneSeasonEntire.info())

plt.title('Win% vs. GAA for goalies with >60 GP from 2013-2017')
plt.annotate('Correlation coefficient: ' + str(oneSeasonEntire['GAA'].corr(oneSeasonEntire['winPercentage'])), xy=(0.65, 0.95), xycoords='axes fraction')
ax = sns.regplot(x="GAA", y="winPercentage", data=oneSeasonEntire)
#print('Correlation coefficient: ', oneSeasonEntire['GAA'].corr(oneSeasonEntire['winPercentage']))
plt.show()



##
