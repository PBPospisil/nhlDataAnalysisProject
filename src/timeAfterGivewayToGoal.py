import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os


goalsInBetweenGAandStoppage = csvToDF('../data/goalsAfterGA.csv')

goalsInBetweenGAandStoppage.loc[:,'game_id'] = goalsInBetweenGAandStoppage.game_id.astype(np.int)
goalsInBetweenGAandStoppage.loc[:,'play_num'] = goalsInBetweenGAandStoppage.play_num.astype(np.int)
goalsInBetweenGAandStoppage.loc[:,'period'] = goalsInBetweenGAandStoppage.period.astype(np.int)

sortedByPlayID = goalsInBetweenGAandStoppage.sort_values(['game_id', 'play_num'])

prevIsGA = False
goalsAfterGiveawayCount = []
timeDifferencesList = []
timeDifference = 0
period = 0
gameID = 0
playNum = 0
teamGainingPossession = 0
playIdToExtract = []
GAindex = 0
allGiveaways = []

for index, _ in enumerate(sortedByPlayID['game_id']):
    if sortedByPlayID.iloc[index,5] == 'Giveaway':
        GAindex = index
        prevIsGA = True
        period = sortedByPlayID.iloc[index,9]
        gameID = sortedByPlayID.iloc[index,1]
        timeDifference = sortedByPlayID.iloc[index,11]
        playNum = sortedByPlayID.iloc[index,2]
        teamGainingPossession = sortedByPlayID.iloc[index,4]
        allGiveaways += [sortedByPlayID.iloc[index,:]]
    elif sortedByPlayID.iloc[index,5] == 'Stoppage':
        prevIsGA = False
    elif (sortedByPlayID.iloc[index,5] == 'Goal' and prevIsGA is True
        and period == sortedByPlayID.iloc[index,9] and gameID == sortedByPlayID.iloc[index,1]
        and sortedByPlayID.iloc[index,3] == teamGainingPossession):
        goalsAfterGiveawayCount += [int(sortedByPlayID.iloc[index,2]) - int(playNum)]
        timeDiff = int(sortedByPlayID.iloc[index,11]) - int(timeDifference)
        timeDifferencesList += [timeDiff]
        prevIsGA = False
        playIdToExtract +=[sortedByPlayID.iloc[GAindex,:]]
        playIdToExtract +=[sortedByPlayID.iloc[index,:]]

if os.path.exists('../data/extractGoalsWithGA.csv'):
        os.remove('../data/extractGoalsWithGA.csv')

csvAllDF = pandas.DataFrame(np.array(playIdToExtract))
csvAllDF.to_csv('../data/extractGoalsWithGA.csv', index=False, sep=',', encoding='utf-8', mode='a')
csvAllDF.columns = goalsInBetweenGAandStoppage.columns

plt.figure(figsize=(12, 9))
ax = sns.distplot(a=timeDifferencesList, hist=True, kde=True,
                  color='darkblue', hist_kws={'edgecolor':'black'},
                  kde_kws={'linewidth': 4})
plt.xlabel('tsime (min)')
plt.ylabel('density')
plt.title('Density plot and histogram of time to score after giveaway')

checkAndMakeImgFolder()

if os.path.exists('../img/density-plot-time-to-score-after-giveaway.png'):
    os.remove('../img/density-plot-time-to-score-after-giveaway.png')
plt.savefig('../img/density-plot-time-to-score-after-giveaway.png', bbox_inches='tight', dpi=300)

#
