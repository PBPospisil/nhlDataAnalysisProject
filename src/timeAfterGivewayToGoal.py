import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os


#lines = csvToDF_largeFile('../game_plays.csv')

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
playIdToExtractFromGAA_Under1 = []
playIdToExtractFromGAA_Under3 = []
playIdToExtractFromGAA_Under10 = []
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
        if timeDiff < 10:
            playIdToExtractFromGAA_Under10 += [sortedByPlayID.iloc[GAindex,:]]
            playIdToExtractFromGAA_Under10 += [sortedByPlayID.iloc[index,:]]
            if timeDiff < 3:
                playIdToExtractFromGAA_Under3 += [sortedByPlayID.iloc[GAindex,:]]
                playIdToExtractFromGAA_Under3 += [sortedByPlayID.iloc[index,:]]
                if timeDiff < 1:
                    playIdToExtractFromGAA_Under1 += [sortedByPlayID.iloc[GAindex,:]]
                    playIdToExtractFromGAA_Under1 += [sortedByPlayID.iloc[index,:]]

os.remove('../data/extractGoalsWithGA.csv')
csvAllDF = pandas.DataFrame(np.array(playIdToExtract))
csvAllDF = csvAllDF.drop(csvAllDF.index[0])
csvAllDF.to_csv('../data/extractGoalsWithGA.csv', index=False, sep=',', encoding='utf-8', mode='a')

#csvAllDF = pandas.DataFrame(np.array(allGiveaways))
#csvAllDF = csvAllDF.drop(csvAllDF.index[0])
#csvAllDF.to_csv('giveaways_to_extract_withGA.csv', index=False, sep=',', encoding='utf-8', mode='a')

# csvUnder10DF = pandas.DataFrame(np.array(playIdToExtractFromGAA_Under10))
# csvUnder10DF = csvUnder10DF.drop(csvUnder10DF.index[0])
# csvUnder10DF.to_csv('goals_to_extract_fromGAA_10sec_withGA.csv', index=False, sep=',', encoding='utf-8', mode='a')
#
# csvUnder3DF = pandas.DataFrame(np.array(playIdToExtractFromGAA_Under3))
# csvUnder3DF = csvUnder3DF.drop(csvUnder3DF.index[0])
# csvUnder3DF.to_csv('goals_to_extract_fromGAA_3sec_withGA.csv', index=False, sep=',', encoding='utf-8', mode='a')
#
# csvUnder1DF = pandas.DataFrame(np.array(playIdToExtractFromGAA_Under1))
# csvUnder1DF = csvUnder1DF.drop(csvUnder1DF.index[0])
# csvUnder1DF.to_csv('goals_to_extract_fromGAA_1sec_withGA.csv', index=False, sep=',', encoding='utf-8', mode='a')

ax = sns.distplot(a=timeDifferencesList, hist=True, kde=True,
                  color='darkblue', hist_kws={'edgecolor':'black'},
                  kde_kws={'linewidth': 4})
plt.xlabel('Time (min)')
plt.ylabel('Density')
plt.title('Density Plot and Histogram of time to score after giveaway')

checkAndMakeImgFolder()

os.remove('../img/density-plot-time-to-score-after-giveaway.png')
plt.savefig('../img/density-plot-time-to-score-after-giveaway.png', bbox_inches='tight')

#
