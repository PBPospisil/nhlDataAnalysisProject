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

playsAfterGiveawayDF = csvToDF('../py_scripts/goals_to_extract_withGA.csv')

for index, value in enumerate(playsAfterGiveawayDF['x']):
    if (value == 'NA'):
        print(value)

playsAfterGiveawayDF.loc[:,'x'] = playsAfterGiveawayDF.x.astype(np.int)
playsAfterGiveawayDF.loc[:,'y'] = playsAfterGiveawayDF.y.astype(np.int)
playsAfterGiveawayDF.loc[:,'x_'] = playsAfterGiveawayDF.x_.astype(np.int)
playsAfterGiveawayDF.loc[:,'y_'] = playsAfterGiveawayDF.y_.astype(np.int)
playsAfterGiveawayDF.loc[:,'period_time'] = playsAfterGiveawayDF.period_time.astype(np.int)

playsAfterGiveawayOnlyGoalsDF = playsAfterGiveawayDF.loc[playsAfterGiveawayDF['5'] == 'Goal']

distanceFromGA = []
timeFromGA = []

for index, _ in enumerate(playsAfterGiveawayDF['0']):
    if playsAfterGiveawayDF.iloc[index, 5] == 'Goal':
        distanceFromGiveawayToNet = math.sqrt((-100 - playsAfterGiveawayDF.iloc[index-1, 17])**2 + (playsAfterGiveawayDF.iloc[index-1, 18])**2)
        distanceFromGA += [distanceFromGiveawayToNet]

        if playsAfterGiveawayDF.iloc[index, 11] - playsAfterGiveawayDF.iloc[index-1, 11] > 0:
            timediff = playsAfterGiveawayDF.iloc[index, 11] - playsAfterGiveawayDF.iloc[index-1, 11]
        else:
            timediff = 0
        timeFromGA += [timediff]


playsAfterGiveawayOnlyGoalsDF['distance_to_goal'] = distanceFromGA
playsAfterGiveawayOnlyGoalsDF['time_from_ga'] = timeFromGA

playsAfterGiveawayOnlyGoalsDF = playsAfterGiveawayOnlyGoalsDF.loc[playsAfterGiveawayOnlyGoalsDF['time_from_ga'] < 100]

style = dict(size=8, color='black')

sortedByTimeDistance = playsAfterGiveawayOnlyGoalsDF.sort_values(by=['time_from_ga', 'distance_to_goal'], ascending=True)

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
        topPercentage += timeDistancePermutationsRounded[key]/len(playsAfterGiveawayOnlyGoalsDF['0'])
        print(key, timeDistancePermutationsRounded[key], timeDistancePermutationsRounded[key]/len(playsAfterGiveawayOnlyGoalsDF['0']))
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
