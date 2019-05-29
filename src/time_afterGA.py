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

goals_inBetween_GAandStoppage = csvToDF('../py_scripts/num_shots_after_GA.csv')

goals_inBetween_GAandStoppage.loc[:,'game_id'] = goals_inBetween_GAandStoppage.game_id.astype(np.int)
goals_inBetween_GAandStoppage.loc[:,'play_num'] = goals_inBetween_GAandStoppage.play_num.astype(np.int)
goals_inBetween_GAandStoppage.loc[:,'period'] = goals_inBetween_GAandStoppage.period.astype(np.int)

sorted_byPlayID = goals_inBetween_GAandStoppage.sort_values(['game_id', 'play_num'])

prevIsGA = False
goals_after_GA_count = []
time_differences = []
timeDifference = 0
period = 0
gameID = 0
playNum = 0
team_gaining_possession = 0
playID_to_extract = []
playID_to_extract_fromGAA_under1 = []
playID_to_extract_fromGAA_under3 = []
playID_to_extract_fromGAA_under10 = []
GAindex = 0
allGiveaways = []

for index, _ in enumerate(sorted_byPlayID['game_id']):
    if sorted_byPlayID.iloc[index,5] == 'Giveaway':
        GAindex = index
        prevIsGA = True
        period = sorted_byPlayID.iloc[index,9]
        gameID = sorted_byPlayID.iloc[index,1]
        timeDifference = sorted_byPlayID.iloc[index,11]
        playNum = sorted_byPlayID.iloc[index,2]
        team_gaining_possession = sorted_byPlayID.iloc[index,4]
        allGiveaways += [sorted_byPlayID.iloc[index,:]]
    elif sorted_byPlayID.iloc[index,5] == 'Stoppage':
        prevIsGA = False
    elif (sorted_byPlayID.iloc[index,5] == 'Goal' and prevIsGA is True
        and period == sorted_byPlayID.iloc[index,9] and gameID == sorted_byPlayID.iloc[index,1]
        and sorted_byPlayID.iloc[index,3] == team_gaining_possession):
        goals_after_GA_count += [int(sorted_byPlayID.iloc[index,2]) - int(playNum)]
        timeDiff = int(sorted_byPlayID.iloc[index,11]) - int(timeDifference)
        time_differences += [timeDiff]
        prevIsGA = False
        playID_to_extract +=[sorted_byPlayID.iloc[GAindex,:]]
        playID_to_extract +=[sorted_byPlayID.iloc[index,:]]
        if timeDiff < 10:
            playID_to_extract_fromGAA_under10 += [sorted_byPlayID.iloc[GAindex,:]]
            playID_to_extract_fromGAA_under10 += [sorted_byPlayID.iloc[index,:]]
            if timeDiff < 3:
                playID_to_extract_fromGAA_under3 += [sorted_byPlayID.iloc[GAindex,:]]
                playID_to_extract_fromGAA_under3 += [sorted_byPlayID.iloc[index,:]]
                if timeDiff < 1:
                    playID_to_extract_fromGAA_under1 += [sorted_byPlayID.iloc[GAindex,:]]
                    playID_to_extract_fromGAA_under1 += [sorted_byPlayID.iloc[index,:]]


# csv_all_df = pandas.DataFrame(np.array(playID_to_extract))
# csv_all_df = csv_all_df.drop(csv_all_df.index[0])
# csv_all_df.to_csv('goals_to_extract_withGA.csv', index=False, sep=',', encoding='utf-8', mode='a')

#csv_all_df = pandas.DataFrame(np.array(allGiveaways))
#csv_all_df = csv_all_df.drop(csv_all_df.index[0])
#csv_all_df.to_csv('giveaways_to_extract_withGA.csv', index=False, sep=',', encoding='utf-8', mode='a')

# csv_under10_df = pandas.DataFrame(np.array(playID_to_extract_fromGAA_under10))
# csv_under10_df = csv_under10_df.drop(csv_under10_df.index[0])
# csv_under10_df.to_csv('goals_to_extract_fromGAA_10sec_withGA.csv', index=False, sep=',', encoding='utf-8', mode='a')
#
# csv_under3_df = pandas.DataFrame(np.array(playID_to_extract_fromGAA_under3))
# csv_under3_df = csv_under3_df.drop(csv_under3_df.index[0])
# csv_under3_df.to_csv('goals_to_extract_fromGAA_3sec_withGA.csv', index=False, sep=',', encoding='utf-8', mode='a')
#
# csv_under1_df = pandas.DataFrame(np.array(playID_to_extract_fromGAA_under1))
# csv_under1_df = csv_under1_df.drop(csv_under1_df.index[0])
# csv_under1_df.to_csv('goals_to_extract_fromGAA_1sec_withGA.csv', index=False, sep=',', encoding='utf-8', mode='a')

ax = sns.distplot(a=time_differences, hist=True, kde=True,
                  color='darkblue', hist_kws={'edgecolor':'black'},
                  kde_kws={'linewidth': 4})
plt.xlabel('Time (min)')
plt.ylabel('Density')
plt.title('Density Plot and Histogram of Goals scored after Giveaways')
plt.show()

#
