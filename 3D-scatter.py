import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt


goalie_stats_df = csvToDF('../game_goalie_stats.csv')
game_df = csvToDF('../game.csv')
players_df = csvToDF('../player_info.csv')

goalie_stats_df.loc[:,'timeOnIce'] = goalie_stats_df.timeOnIce.astype(np.int)

seasons = []
player_season_id = []
ID = 1
playerSeasonID = defaultdict(int)

for game in goalie_stats_df['game_id']:
    seasons.append(game_df.loc[game_df['game_id'] == game, 'season'])

goalie_stats_df['season'] = seasons

for index, _ in enumerate(goalie_stats_df['game_id']):

    if playerSeasonID[' '.join([goalie_stats_df.iloc[index, 1], goalie_stats_df.iloc[index, 19].item()])] == 0:
        playerSeasonID[' '.join([goalie_stats_df.iloc[index, 1], goalie_stats_df.iloc[index, 19].item()])] = ID
        player_season_id.append(ID)
        ID += 1
    else:
        player_season_id.append(playerSeasonID[' '.join([goalie_stats_df.iloc[index, 1], goalie_stats_df.iloc[index, 19].item()])])

goalie_stats_df['player_season_id'] = player_season_id

goalie_stats_df = goalie_stats_df.drop(goalie_stats_df.loc[goalie_stats_df['savePercentage'] == 'NA'].index)

goalie_stats_df.loc[:,'savePercentage'] = goalie_stats_df.savePercentage.astype(np.float)
goalie_stats_df.loc[:,'shots'] = goalie_stats_df.shots.astype(np.int)
goalie_stats_df.loc[:,'saves'] = goalie_stats_df.saves.astype(np.int)

one_season_entire = pandas.DataFrame(np.zeros(len(playerSeasonID)))

one_season_entire['player_season_id'] = playerSeasonID.keys()
one_season_entire['totalTOI'] = np.zeros(len(one_season_entire))
one_season_entire['wins'] = np.zeros(len(one_season_entire))
one_season_entire['GAA'] = np.zeros(len(one_season_entire))
one_season_entire['savePercentage'] = np.zeros(len(one_season_entire))
one_season_entire['gamesPlayed'] = np.zeros(len(one_season_entire))
one_season_entire['winPercentage'] = np.zeros(len(one_season_entire))
one_season_entire['shots'] = np.zeros(len(one_season_entire))
one_season_entire['saves'] = np.zeros(len(one_season_entire))

one_season_entire.drop(0, axis=1, inplace=True)

for outerIndex, playerSeason in enumerate(one_season_entire['player_season_id']):
    [player, season] = str(playerSeason).split(' ')
    player_specific = goalie_stats_df.loc[goalie_stats_df['player_id'] == player]
    for innerIndex, _ in enumerate(player_specific['game_id']):
        if player_specific.iloc[innerIndex, 19].item() == season:
            # shots
            one_season_entire.iloc[outerIndex, 7] += player_specific.iloc[innerIndex, 7]
            #saves
            one_season_entire.iloc[outerIndex, 8] += player_specific.iloc[innerIndex, 8]
            #totalTOI
            one_season_entire.iloc[outerIndex, 1] += player_specific.iloc[innerIndex, 3]
            #wins
            if player_specific.iloc[innerIndex, 15] == 'W':
                one_season_entire.iloc[outerIndex, 2] += 1
            one_season_entire.iloc[outerIndex, 5] += 1
    one_season_entire.iloc[outerIndex, 3] = ((one_season_entire.iloc[outerIndex, 7] - one_season_entire.iloc[outerIndex, 8]) * 3600) / one_season_entire.iloc[outerIndex, 1]
    if one_season_entire.iloc[outerIndex, 7] != 0:
        one_season_entire.iloc[outerIndex, 4] = int(one_season_entire.iloc[outerIndex, 8]) / int(one_season_entire.iloc[outerIndex, 7])
    one_season_entire.iloc[outerIndex, 6] = one_season_entire.iloc[outerIndex, 2] / one_season_entire.iloc[outerIndex, 5]

one_season_entire = one_season_entire.drop(one_season_entire.loc[one_season_entire['gamesPlayed'] < 60].index)
one_season_entire = one_season_entire.reset_index(drop=True)
print(one_season_entire.info())

plt.title('Win% vs. GAA for goalies with >60 GP from 2013-2017')
plt.annotate('Correlation coefficient: ' + str(one_season_entire['GAA'].corr(one_season_entire['winPercentage'])), xy=(0.65, 0.95), xycoords='axes fraction')
ax = sns.regplot(x="GAA", y="winPercentage", data=one_season_entire)
#print('Correlation coefficient: ', one_season_entire['GAA'].corr(one_season_entire['winPercentage']))
plt.show()



##
