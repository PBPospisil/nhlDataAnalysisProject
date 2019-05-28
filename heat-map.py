import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF_largeFile import csvToDF_largeFile
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt


goals_df = csvToDF('../goals.csv')

goals_df = goals_df.drop(goals_df.loc[goals_df['x'] == 'NA'].index)

goals_df.loc[:,'x'] = goals_df.x.astype(np.float)
goals_df.loc[:,'y'] = goals_df.y.astype(np.float)

goals_df = goals_df.loc[goals_df['secondaryType'] == 'Slap Shot']

heatmap_goals_df = pandas.DataFrame(np.array([]))
heatmap_goals_df['x'] = goals_df['x']
heatmap_goals_df['y'] = goals_df['y']
heatmap_goals_df = heatmap_goals_df.drop(0, axis=1)

sns.jointplot(x='x', y='y', data=heatmap_goals_df, kind='kde', color='r', xlim=(-100,100), ylim=(-42.5,42.5))
plt.show()
