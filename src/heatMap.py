import os
import pandas
import numpy as np
import csv
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt

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
    sns.jointplot(x='x', y='y', data=goalsDF.loc[goalsDF['secondaryType'] == goalType],
                  kind='kde', color='r', xlim=(-100,100), ylim=(-42.5,42.5))

    checkAndMakeImgFolder(heatmap=True)

    if os.path.exists('../img/heatmaps/jointplot-' + '-'.join(goalType.lower().split(' ')) + '-heatmap.png'):
        os.remove('../img/heatmaps/jointplot-' + '-'.join(goalType.lower().split(' ')) + '-heatmap.png')
    plt.savefig('../img/heatmaps/jointplot-' + '-'.join(goalType.lower().split(' ')) + '-heatmap.png', bbox_inches='tight')
