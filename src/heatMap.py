import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt


goalsDF = csvToDF('../data/goals.csv')

goalsDF = goalsDF.drop(goalsDF.loc[goalsDF['x'] == 'NA'].index)
goalsDF = goalsDF.drop(goalsDF.loc[goalsDF['x'] == 'x'].index)
goalsDF = goalsDF.drop(goalsDF.loc[goalsDF['secondaryType'] == 'x'].index)

goalsDF.loc[:,'x'] = goalsDF.x.astype(np.float)
goalsDF.loc[:,'y'] = goalsDF.y.astype(np.float)

for goalType in (goalsDF['secondaryType'].unique()):
    goalsDF = goalsDF.loc[goalsDF['secondaryType'] == goalType]

    heatmapGoalsDF = pandas.DataFrame(np.array([]))
    heatmapGoalsDF['x'] = goalsDF['x']
    heatmapGoalsDF['y'] = goalsDF['y']
    heatmapGoalsDF = heatmapGoalsDF.drop(0, axis=1)

    sns.jointplot(x='x', y='y', data=heatmapGoalsDF, kind='kde', color='r', xlim=(-100,100), ylim=(-42.5,42.5))

    checkAndMakeImgFolder(heatmap=True)

    os.remove('../img/heatmaps/jointplot-' + '-'.join(goalType.lower().split(' ')) + '-heatmap.png')
    plt.savefig('../img/heatmaps/jointplot-' + '-'.join(goalType.lower().split(' ')) + '-heatmap.png', bbox_inches='tight')
