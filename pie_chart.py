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

game_plays_after_GA_df = csvToDF('../py_scripts/play_after_GA.csv')
game_plays_after_GA_df.loc[:,'game_id'] = game_plays_after_GA_df.game_id.astype(np.int)
game_plays_after_GA_df.loc[:,'play_num'] = game_plays_after_GA_df.play_num.astype(np.int)
game_plays_after_GA_df.loc[:,'period'] = game_plays_after_GA_df.period.astype(np.int)

event_after_giveaway_count = defaultdict(int)

for event in game_plays_after_GA_df['event']:
    event_after_giveaway_count[event] += 1

keys = np.array(list(event_after_giveaway_count.keys()))
vals = np.array(list(event_after_giveaway_count.values())).astype(float)
plt.xlabel('Type of play')
plt.ylabel('Count')
plt.title('Barplot of the next play after a Giveaway')
ax = sns.barplot(x=keys[:11], y=vals[:11])
plt.show()







#
