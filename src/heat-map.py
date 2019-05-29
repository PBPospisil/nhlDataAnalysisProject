import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF_largeFile import csvToDF_largeFile
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt


goalsDF = csvToDF('../goals.csv')

goalsDF = goalsDF.drop(goalsDF.loc[goalsDF['x'] == 'NA'].index)

goalsDF.loc[:,'x'] = goalsDF.x.astype(np.float)
goalsDF.loc[:,'y'] = goalsDF.y.astype(np.float)

goalsDF = goalsDF.loc[goalsDF['secondaryType'] == 'Slap Shot']

heatmapGoalsDF = pandas.DataFrame(np.array([]))
heatmapGoalsDF['x'] = goalsDF['x']
heatmapGoalsDF['y'] = goalsDF['y']
heatmapGoalsDF = heatmapGoalsDF.drop(0, axis=1)

sns.jointplot(x='x', y='y', data=heatmapGoalsDF, kind='kde', color='r', xlim=(-100,100), ylim=(-42.5,42.5))
plt.show()
