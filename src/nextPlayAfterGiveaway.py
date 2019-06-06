import os
import pandas
import numpy as np
import csv
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams

from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder

from collections import defaultdict


playAfterGiveaway = csvToDF('../data/play_after_GA.csv')
eventAfterGiveawayCount = defaultdict(int)

playAfterGiveaway.loc[:,'game_id'] = playAfterGiveaway.game_id.astype(np.int)
playAfterGiveaway.loc[:,'play_num'] = playAfterGiveaway.play_num.astype(np.int)
playAfterGiveaway.loc[:,'period'] = playAfterGiveaway.period.astype(np.int)

for event in playAfterGiveaway['event']:
    eventAfterGiveawayCount[event] += 1

keys = np.array(list(eventAfterGiveawayCount.keys()))
vals = np.array(list(eventAfterGiveawayCount.values())).astype(float)

plt.figure(figsize=(12, 9))
plt.xlabel('Type of play')
plt.ylabel('Count')
plt.title('Barplot of the next play after a Giveaway')

ax = sns.barplot(x=keys[:11], y=vals[:11])

checkAndMakeImgFolder()

if os.path.exists('../img/barplot-next-play-after-giveaway.png'):
    os.remove('../img/barplot-next-play-after-giveaway.png')
plt.savefig('../img/barplot-next-play-after-giveaway.png', bbox_inches='tight')
