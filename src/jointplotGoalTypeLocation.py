import os
import pandas
import numpy as np
import csv
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from matplotlib import rcParams

from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict


goalsDF = csvToDF('../data/goals.csv')

goalsDF = goalsDF.drop(goalsDF.loc[goalsDF['x'] == 'NA'].index)
goalsDF = goalsDF.drop(goalsDF.loc[goalsDF['x'] == 'x'].index)
goalsDF = goalsDF.drop(goalsDF.loc[goalsDF['secondaryType'] == 'x'].index)
goalsDF = goalsDF.drop(goalsDF.loc[goalsDF['secondaryType'] == 'NA'].index)

goalsDF.loc[:,'x'] = goalsDF.x.astype(np.float)
goalsDF.loc[:,'y'] = goalsDF.y.astype(np.float)

for index, goalType in enumerate(goalsDF['secondaryType'].unique()):
    ax = sns.jointplot(x='x', y='y', data=goalsDF.loc[goalsDF['secondaryType'] == goalType],
                  kind='kde', color='r', xlim=(-100,100), ylim=(-42.5,42.5),
                  height=11.7)
    ax.set_axis_labels('x coordinate', 'y coordinate')
    ax.fig.suptitle('Jointplot of location of goals scored of type: ' + str(goalType),
                    x='0.5', y='1.0', fontsize='16')

    checkAndMakeImgFolder(jointplot=True)

    if os.path.exists('../img/joinplots/jointplot-' + '-'.join(goalType.lower().split(' ')) + '-joinplots.png'):
        os.remove('../img/joinplots/jointplot-' + '-'.join(goalType.lower().split(' ')) + '-joinplots.png')
    plt.savefig('../img/joinplots/jointplot-' + '-'.join(goalType.lower().split(' ')) + '-joinplots.png', bbox_inches='tight')
