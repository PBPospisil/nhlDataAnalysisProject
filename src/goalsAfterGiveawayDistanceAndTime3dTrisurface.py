import os
import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/usr/local/bin/ffmpeg'
from mpl_toolkits.mplot3d import Axes3D
import math
from scipy.stats import norm
from matplotlib import animation


playsAfterGiveawayDF = csvToDF('../data/extractGoalsWithGA.csv')

csvfileFile = open('../data/goalsAfterGA.csv'); csvReader = csv.reader(csvfileFile)

playsAfterGiveawayDF.columns = list(csvReader)[0]

playsAfterGiveawayDF = playsAfterGiveawayDF.drop(playsAfterGiveawayDF.loc[playsAfterGiveawayDF['x'] == 'NA'].index)
playsAfterGiveawayDF = playsAfterGiveawayDF.drop(playsAfterGiveawayDF.loc[playsAfterGiveawayDF['x'] == 'x'].index)

playsAfterGiveawayDF.loc[:,'x'] = playsAfterGiveawayDF.x.astype(np.int)
playsAfterGiveawayDF.loc[:,'y'] = playsAfterGiveawayDF.y.astype(np.int)
playsAfterGiveawayDF.loc[:,'st_x'] = playsAfterGiveawayDF.st_x.astype(np.int)
playsAfterGiveawayDF.loc[:,'st_y'] = playsAfterGiveawayDF.st_y.astype(np.int)
playsAfterGiveawayDF.loc[:,'periodTime'] = playsAfterGiveawayDF.periodTime.astype(np.int)

playsAfterGiveawayOnlyGoalsDF = playsAfterGiveawayDF.loc[playsAfterGiveawayDF['event'] == 'Goal'].copy()

distanceFromGA = []
timeFromGA = []

for index, _ in enumerate(playsAfterGiveawayDF['play_id']):
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

playsAfterGiveawayOnlyGoalsDF = playsAfterGiveawayOnlyGoalsDF.loc[playsAfterGiveawayOnlyGoalsDF['time_from_ga'] < 60]

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
        timeDistancePermutationsRounded[' '.join([str(time), '0'])] = 0
    timeDistancePermutationsRounded[' '.join([str(round(time)), str(round(j))])] += 1

i = 0
for key in timeDistancePermutationsRounded.keys():
    [time, distance] = key.split(' ')
    xValues += [round(float(time))]
    yValues += [round(float(distance))]
    zValues += [timeDistancePermutationsRounded[key]]

fig = plt.figure(dpi=300)
ax = fig.gca(projection='3d')
writer = animation.FFMpegFileWriter()

def init():
    ax.plot_trisurf(xValues, yValues, zValues, cmap=plt.cm.jet, linewidth=0.01)
    return fig,

def animate(i):
    ax.view_init(elev=10., azim=i)
    return fig,

plt.xlabel('time')
plt.ylabel('distance')
plt.title('Time and distance distribution for goals scored < 60 sec after giveaway')

# Animate
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=360, interval=20, blit=True)
checkAndMakeImgFolder()

if os.path.exists('../img/less-than-60sec.mp4'):
    os.remove('../img/less-than-60sec.mp4')
anim.save('../img/less-than-60sec.mp4', writer=writer)
