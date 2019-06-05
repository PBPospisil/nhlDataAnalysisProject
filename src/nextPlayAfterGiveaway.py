import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


#lines = csvToDF_largeFile('../game_plays.csv')
#print(lines)

playAfterGiveaway = csvToDF('../data/play_after_GA.csv')
eventAfterGiveawayCount = defaultdict(int)

playAfterGiveaway.loc[:,'game_id'] = playAfterGiveaway.game_id.astype(np.int)
playAfterGiveaway.loc[:,'play_num'] = playAfterGiveaway.play_num.astype(np.int)
playAfterGiveaway.loc[:,'period'] = playAfterGiveaway.period.astype(np.int)

for event in playAfterGiveaway['event']:
    eventAfterGiveawayCount[event] += 1

keys = np.array(list(eventAfterGiveawayCount.keys()))
vals = np.array(list(eventAfterGiveawayCount.values())).astype(float)

plt.xlabel('Type of play')
plt.ylabel('Count')
plt.title('Barplot of the next play after a Giveaway')

ax = sns.barplot(x=keys[:11], y=vals[:11])

checkAndMakeImgFolder()

os.remove('../img/barplot-next-play-after-giveaway.png')
plt.savefig('../img/barplot-next-play-after-giveaway.png', bbox_inches='tight')
