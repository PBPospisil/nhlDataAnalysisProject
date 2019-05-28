import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF_largeFile import csvToDF_largeFile
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'
from mpl_toolkits.mplot3d import Axes3D
import math
from scipy.stats import norm
from matplotlib import animation


#lines = csvToDF_largeFile('../game_plays.csv')

game_plays_after_GA_df = csvToDF('../py_scripts/goals_to_extract_withGA.csv')
giveaways_plays_after_GA_df = csvToDF('../py_scripts/goals_to_extract_withGA.csv')

for index, value in enumerate(game_plays_after_GA_df['x']):
    if (value == 'NA'):
        print(value)

game_plays_after_GA_df.loc[:,'x'] = game_plays_after_GA_df.x.astype(np.int)
game_plays_after_GA_df.loc[:,'y'] = game_plays_after_GA_df.y.astype(np.int)
game_plays_after_GA_df.loc[:,'x_'] = game_plays_after_GA_df.x_.astype(np.int)
game_plays_after_GA_df.loc[:,'y_'] = game_plays_after_GA_df.y_.astype(np.int)
game_plays_after_GA_df.loc[:,'period_time'] = game_plays_after_GA_df.period_time.astype(np.int)

game_plays_after_GA_only_goals_df = game_plays_after_GA_df.loc[game_plays_after_GA_df['5'] == 'Goal']

distanceFromGA = []
timeFromGA = []

for index, _ in enumerate(game_plays_after_GA_df['0']):
    if game_plays_after_GA_df.iloc[index, 5] == 'Goal':
        distance_ga_net = math.sqrt((-100 - game_plays_after_GA_df.iloc[index-1, 17])**2 + (game_plays_after_GA_df.iloc[index-1, 18])**2)
        distanceFromGA += [distance_ga_net]

        if game_plays_after_GA_df.iloc[index, 11] - game_plays_after_GA_df.iloc[index-1, 11] > 0:
            timediff = game_plays_after_GA_df.iloc[index, 11] - game_plays_after_GA_df.iloc[index-1, 11]
        else:
            timediff = 0
        timeFromGA += [timediff]


game_plays_after_GA_only_goals_df['distance_to_goal'] = distanceFromGA
game_plays_after_GA_only_goals_df['time_from_ga'] = timeFromGA

game_plays_after_GA_only_goals_df = game_plays_after_GA_only_goals_df.loc[game_plays_after_GA_only_goals_df['time_from_ga'] < 100]

style = dict(size=8, color='black')

sortedByTimeDistance = game_plays_after_GA_only_goals_df.sort_values(by=['time_from_ga', 'distance_to_goal'], ascending=True)

zValues = []
yValues = []
xValues = []
timeDistancePermutations = defaultdict(int)
timeDistancePermutationsRounded = defaultdict(int)


for index, time in enumerate(sortedByTimeDistance['time_from_ga']):
    distance = sortedByTimeDistance.iloc[index, 20]
    timeDistancePermutations[' '.join([str(time), str(distance)])] += 1
    j=0
    while(distance > j):
        j += 10
    if j == 10:
        timeDistancePermutationsRounded[' '.join([str(time), str(0)])] = 0
    timeDistancePermutationsRounded[' '.join([str(round(time)), str(round(j))])] += 1


i = 0
for key in timeDistancePermutationsRounded.keys():
    [time, distance] = key.split(' ')
    xValues += [round(float(time))]
    yValues += [round(float(distance))]
    zValues += [timeDistancePermutationsRounded[key]]

topPercentage = 0
for key in sorted(timeDistancePermutationsRounded, key=timeDistancePermutationsRounded.get, reverse=True):
    if i < 20:
        topPercentage += timeDistancePermutationsRounded[key]/len(game_plays_after_GA_only_goals_df['0'])
        print(key, timeDistancePermutationsRounded[key], timeDistancePermutationsRounded[key]/len(game_plays_after_GA_only_goals_df['0']))
    i += 1

print(topPercentage, len(timeDistancePermutationsRounded.keys()))

fig = plt.figure()
ax = fig.gca(projection='3d')
writer = animation.FFMpegFileWriter()

def init():
    ax.plot_trisurf(xValues, yValues, zValues, cmap=plt.cm.jet, linewidth=0.01)
    return fig,

def animate(i):
    ax.view_init(elev=10., azim=i)
    return fig,

plt.xlabel('Time')
plt.ylabel('Distance')
plt.title('Time and Distance count for goals < 10 sec after GA')

# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=20, blit=True)
# Save
anim.save('less-than-60sec.mp4', writer=writer)

plt.show()
