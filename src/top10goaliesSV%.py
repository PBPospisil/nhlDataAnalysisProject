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


player_info = csvToDF("../player_info.csv")

goalie_stats_df = csvToDF('../game_goalie_stats.csv')
goalie_stats_df.loc[:,'game_id'] = goalie_stats_df.game_id.astype(np.int)
goalie_stats_df.loc[:,'timeOnIce'] = goalie_stats_df.timeOnIce.astype(np.float)
goalie_stats_df = goalie_stats_df.sort_values(['game_id'], ascending=True)

timeOnIce = []

entire_DS_goalieSV = pandas.DataFrame(np.array(goalie_stats_df['player_id'].unique()))
entire_DS_goalieSV.columns = ['player_id']
for player in entire_DS_goalieSV['player_id']:
    TOI = goalie_stats_df.loc[goalie_stats_df['player_id'] == player, 'timeOnIce'].sum()
    timeOnIce += [TOI]

entire_DS_goalieSV['timeOnIce'] = timeOnIce
entire_DS_goalieSV.loc[:,'timeOnIce'] = entire_DS_goalieSV.timeOnIce.astype(np.float)

sorted_by_TOI = entire_DS_goalieSV.sort_values(['timeOnIce'], ascending=False)
sorted_by_TOI.loc[:,'player_id'] = sorted_by_TOI.player_id.astype(np.float)

top10 = 0
playerID = []
accumTOI = []
accumSV = []

for player in sorted_by_TOI['player_id'][:10]:
    player = str(int(sorted_by_TOI.iloc[top10,0]))
    player_stats = goalie_stats_df.loc[goalie_stats_df['player_id'] == player]
    player_stats.loc[:,'shots'] = player_stats.shots.astype(np.float)
    player_stats.loc[:,'saves'] = player_stats.saves.astype(np.float)

    TOIsum = 0
    totalShots = 0
    totalSaves = 0
    for game in player_stats['game_id']:
        playerID += [player]
        TOIsum += player_stats.loc[player_stats['game_id'] == game, 'timeOnIce'].item()
        totalShots += player_stats.loc[player_stats['game_id'] == game, 'shots'].item()
        totalSaves += player_stats.loc[player_stats['game_id'] == game, 'saves'].item()

        accumTOI += [TOIsum/3600]
        accumSV += [totalSaves / totalShots]
    top10 += 1

top10_SV_over_TOI = pandas.DataFrame(np.array(playerID))
top10_SV_over_TOI.columns = ['player_id']
top10_SV_over_TOI['timeOnIce'] = accumTOI
top10_SV_over_TOI['savePercentage'] = accumSV

for player in top10_SV_over_TOI['player_id'].unique():
    name = player_info.loc[player_info['player_id'] == player, 'firstName'].item()+ ' ' + player_info.loc[player_info['player_id'] == player, 'lastName'].item()
    plt.plot('timeOnIce', 'savePercentage', data=top10_SV_over_TOI.loc[top10_SV_over_TOI['player_id'] == player], label=name)
    plt.ylim(0.88,0.95)

plt.xlabel('per 60 minutes')
plt.ylabel('Save Percentage')
plt.title('Save Percentage over Dataset for Top 10 player Goaltenders from 2012-2017')
plt.legend()
plt.show()




#
