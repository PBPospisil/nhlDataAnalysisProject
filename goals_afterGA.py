import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF_largeFile import csvToDF_largeFile
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#lines = csvToDF_largeFile('../game_plays.csv')

#print(lines)

goals_inBetween_GAandStoppage = csvToDF('../py_scripts/num_shots_after_GA.csv')

goals_inBetween_GAandStoppage.loc[:,'game_id'] = goals_inBetween_GAandStoppage.game_id.astype(np.int)
goals_inBetween_GAandStoppage.loc[:,'play_num'] = goals_inBetween_GAandStoppage.play_num.astype(np.int)
goals_inBetween_GAandStoppage.loc[:,'period'] = goals_inBetween_GAandStoppage.period.astype(np.int)

sorted_byPlayID = goals_inBetween_GAandStoppage.sort_values(['game_id', 'play_num'])

prevIsGA = False
goals_after_GA_count = []
period = 0
gameID = 0
playNum = 0
team_gaining_possession = 0
for index, _ in enumerate(sorted_byPlayID['game_id']):
    if sorted_byPlayID.iloc[index,5] == 'Giveaway':
        prevIsGA = True
        period = sorted_byPlayID.iloc[index,9]
        gameID = sorted_byPlayID.iloc[index,1]
        playNum = sorted_byPlayID.iloc[index,2]
        team_gaining_possession = sorted_byPlayID.iloc[index,4]
    elif sorted_byPlayID.iloc[index,5] == 'Stoppage':
        prevIsGA = False
    elif (sorted_byPlayID.iloc[index,5] == 'Goal' and prevIsGA is True
        and period == sorted_byPlayID.iloc[index,9] and gameID == sorted_byPlayID.iloc[index,1]
        and sorted_byPlayID.iloc[index,3] == team_gaining_possession):
        goals_after_GA_count += [int(sorted_byPlayID.iloc[index,2]) - int(playNum)]

ax = sns.distplot(a=goals_after_GA_count, hist=True, kde=True,
                  color='darkblue', hist_kws={'edgecolor':'black'},
                  kde_kws={'linewidth': 4})
plt.xlabel('Plays after Giveaway')
plt.ylabel('Density')
plt.title('Density Plot and Histogram of number of Plays until a Goal is scored after a Giveaway')

plt.legend()
plt.show()
