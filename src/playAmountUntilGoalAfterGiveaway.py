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


goalsInBetweenGAandStoppage = csvToDF('../data/goalsAfterGA.csv')

goalsInBetweenGAandStoppage.loc[:,'game_id'] = goalsInBetweenGAandStoppage.game_id.astype(np.int)
goalsInBetweenGAandStoppage.loc[:,'play_num'] = goalsInBetweenGAandStoppage.play_num.astype(np.int)
goalsInBetweenGAandStoppage.loc[:,'period'] = goalsInBetweenGAandStoppage.period.astype(np.int)

sortedByPlayID = goalsInBetweenGAandStoppage.sort_values(['game_id', 'play_num'])

prevIsGA = False
goalsAfterGiveawayCount = []
period = 0
gameID = 0
playNum = 0
teamGainingPossession = 0
for index, _ in enumerate(sortedByPlayID['game_id']):
    if sortedByPlayID.iloc[index,5] == 'Giveaway':
        prevIsGA = True
        period = sortedByPlayID.iloc[index,9]
        gameID = sortedByPlayID.iloc[index,1]
        playNum = sortedByPlayID.iloc[index,2]
        teamGainingPossession = sortedByPlayID.iloc[index,4]
    elif sortedByPlayID.iloc[index,5] == 'Stoppage':
        prevIsGA = False
    elif (sortedByPlayID.iloc[index,5] == 'Goal' and prevIsGA is True
        and period == sortedByPlayID.iloc[index,9] and gameID == sortedByPlayID.iloc[index,1]
        and sortedByPlayID.iloc[index,3] == teamGainingPossession):
        goalsAfterGiveawayCount += [int(sortedByPlayID.iloc[index,2]) - int(playNum)]

plt.figure(figsize=(12, 9))
ax = sns.distplot(a=goalsAfterGiveawayCount, hist=True, kde=True,
                  color='darkblue', hist_kws={'edgecolor':'black'},
                  kde_kws={'linewidth': 4})
plt.xlabel('plays after giveaway')
plt.ylabel('density')
plt.title('Density plot and histogram of plays until goal scored after giveaway')

checkAndMakeImgFolder()

if os.path.exists('../img/density-plot-plays-unitl-goal-after-giveaway.png'):
    os.remove('../img/density-plot-plays-unitl-goal-after-giveaway.png')
plt.savefig('../img/density-plot-plays-unitl-goal-after-giveaway.png', bbox_inches='tight', dpi=300)
