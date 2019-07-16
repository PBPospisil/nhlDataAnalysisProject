# Data Visualization and Model Testing on 'NHL Game Data' 

Data analysis of the 'NHL Game Data', the dataset from kaggle and contributed by Martin Ellis. This project contains a series of scripts to clean and process data for visualization. Containing unique data features including details for every play such as location on the ice and secondary play type, this data set motivated an effort to analyze NHL data and reveal new insights and explore known tendencies. 

From the beginning, the main goal of this project has been to gain more experience with data analysis tools in python, specifically the matplotlib and seaborn libraries for visualization. In order to spend more time on visulization and expedite the process leading upto visualization, cleaning and processing pipelines were developed using an object-oriented paradigm. Therefore, the images made result from the declaration of a graphing object and calling a few methods on the object according to the specification of the intended image.

Further improvements upon the graphing class objects will include detailed customization of graph style and user-defined data profiles for graphing.


## Getting Started
All of the needed libraries are contained in the latest anaconda distribution.
### Prerequisites

```
Python 3
conda 4.5.12
```
### Setting up the Environment
Download the respository, cd to src and use the makefile command:
```
make data
```
Download the Kaggle Dataset here: [NHL Game Data](https://www.kaggle.com/martinellis/nhl-game-data). Move to the data folder, unzip the archive, then use the included makefile command:
```
make subsets
```
which declares an object of the ```MakeSubsets()``` class. This class contains methods that condense the game_plays.csv file in order to decrease processing time upon further use. The scripts that use this csv require only a subset of this data file. 

### Graph Data
The base class for this library is ```GraphData()```, which holds general graphing data like column data types. The member functions for ```GraphData()``` currently imports a csv file to a dataframe, and another cleans missing rows.  

## Predicting Win Percentage

Another goal of this project was to investigate the power of certain indicators to predict win percentage and to illustrate strength of prediction using the developed graphing library.

### Goals Against Average as a predictor

The class ```GraphGoalieStats()```, takes keyword arguments ```mode``` and ```figure_name``` and ```GraphTeamStats()```takes no keyword args., but like ```GraphGoalieStats()```, ```GraphTeamStats()``` inherits much of its functionality from the ```GraphModel()``` class.

#### Goaltender Win Percentage
```mode```: accepts 'GAA' or 'savePercentage'

```figure_name```: string-type file name of figure
<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/60957127-5a5ddf00-a2c1-11e9-93a9-caae0e07dcad.png' alt='gaa-win%-goaltender' width='600'/>
</p>
Goals Against Average (GAA) is shown here to have a weak correlation with Goaltender Win Percentage (GWP). One reason for this is that goals are complex events that are influenced by other players including a goaltender's teammate(s); because of this GAA is stronger predictor for Team Win Percentage (TWP).

#### Team Win Percentage
<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/60953113-c3d9ef80-a2b9-11e9-8f0b-f400234da641.png' alt='gaa-win%-teams' width='580'/>
</p>

### Exploring Different Prediction Methods
The main functionality of the ```GraphModel()``` class is to support easy development of various prediction methods and visualization functions.

#### Goals For (GF) Goals Against (GA)
The ratio of GF to GA is often used as the basis for a linear model. The scatter plot below has a win prediction calculated using

<p align='center'>
  <img src='https://latex.codecogs.com/svg.latex?%5Cbg_black%20%5Cfrac%7BGF%7D%7BGA%7D' alt='gf/ga' />
</p>

which has a correlation coefficient of 0.899 with TWP.

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61102169-04f11180-a42a-11e9-8068-bcb69d05e061.png' alt='scatter-winpred-noalpha' align='center' width='600' />
</p>

After some experimentation, it was found that a win prediction calculated using the following equation

<p align='center'>
  <img src='https://latex.codecogs.com/svg.latex?%5Cbg_black%20%5Cfrac%7BGF%7D%7BGA%7D&plus;PP%5Ccdot%20PK' alt='gf/ga+pk*pp' />
</p>

correlates highly with TWP, with a correlation coefficient of 0.911. 

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61024867-2db2d180-a36c-11e9-89e5-690f85697fbe.png' alt='scatter-winpred-withalpha' align='center' width='600' />
</p>

#### Error in the Model

To see how the model performs, ```GraphModel()``` has the option to create line plots with absolute error margins of a given team and season. One plot is produced by a single call to ```LinearModel()```. Overall team win percentage in a season should be easier to predict as a season goes on, due to the distribution centering around am average win percentage.

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61258485-37a14f80-a733-11e9-9dc8-18c1a7c0e967.png' alt='error-winpred-for-team' align='center' width='600' />
</p>

However, the predictive ability of the model is underwhelming as shown in the line plot above. With ~10% error in the model by the last game and an average error that slides under 20%, the predicted TWP is generally too optimistic and higher than the actual win percentage.

In order to compensate for the overestimate in the model, the prediction formula was modified with a coefficient as follows 

<p align='center'>
  <img src='https://latex.codecogs.com/svg.latex?PredW%20%3A%3D%20%5Calpha%20%5Ccdot%20%5Cleft%20%5B%20%5Cfrac%7BGF%7D%7BGA%7D%20&plus;%20PP%5Ccdot%20PK%20%5Cright%20%5D' alt='gf/ga+pk*pp' />
</p>

The alpha coefficient is optimized by minimizing mean squared error (MSE) of each call to the ```LinearModel()``` class, until an iterative (time-out) or optimized-value threshold is reached. This also allows for a specific value to be optimized given a certain subset of data (i.e. for a single season or team).

The plot below is of the same team and season, but with an optimized alpha coefficient.

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61027537-b2551e00-a373-11e9-9634-e0b4333b976a.png' alt='error-winpred-for-team' align='center' width='600' />
</p>

Error in model prediction is reduced by at least 50% with an alpha of 0.800.

The scatter plot of alpha values for each season below illustrates convergence of the alpha coefficient. Because predicted TWP is largely dependent on GF/GA, alpha responds to changes in GF/GA. This explains the decrease in the alpha convergence value for the 2016-2017 season, as GF/GA spikes by late 2015 into 2016. This could be explained by the added coach's challenge in 2015-2016, the purpose of which was partially to increase goals by limiting overturned goals.

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61100303-fb17e000-a422-11e9-9833-1f83fb49d187.png' alt='alpha-scatter' align='center' width='600' />
</p>

## Giveaways

Since this dataset includes detailed play-by-play information, analysis was done related to the impact that a giveaway has on the game. A particular point of interest was the impact that a giveaway has on the next play, or the string of plays to follow.

Additionally, a focus on a spatio-temporal distribution of converted giveaways 

### Play after a Giveaway

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61005094-bad23800-a324-11e9-9add-55ac5d469e81.png' alt='bar-giveaway' width='600'/>
</p>

### Goal Type after a Giveaway

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61211916-089cc680-a6be-11e9-9668-1ee7a6587ec0.png' alt='barplot-goal-type-after-GA-under10sec' width='600'/>
</p>


### Converted Giveaway Distribution based on Time and Distance from net

Trisurface plot of the number of converted GAs under 10 seconds by distance from GA to net and time
<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61162272-1509ff00-a4c5-11e9-8dd2-cdaefcac3c11.gif' alt='gif'          width='600'/>
</p>

The scatter plot below shows the spatial distribution of the types of goals scored within 3 seconds of a giveaway.

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/58522140-3ebcd000-817c-11e9-82bd-eef97b24b10d.png' alt='scatter-under-3sec-goals' width='725'/>
</p>

The density plots below illustrate distributions of the time after a giveaway and number of plays after a giveaway before a goal is scored. The goals used in the plots are only scored after a giveaway and before a stoppage in play. Goals aren't included if a stoppage occurs after a giveaway and before a goal. 

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61169337-588e5880-a519-11e9-97b6-3207055ca310.png' alt='density-plot-time' width='600'/>
</p>

Declaring an instance of ```GraphGiveawayGoals()``` and calling create_density_plot() with keyword argument mode set to 'time' or 'count'.

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61193300-ccdf0e00-a677-11e9-8d1b-aecd2596fa6a.png' alt='density-plot-plays-after' width='600'/>
</p>

## Goaltender Save Percentage

The line plot below includes 10 goaltenders with the most TOI 

<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61169340-5fb56680-a519-11e9-8dcb-f7a1644fc19d.png' alt='goalie-top-10-sv%' width='600'/>
</p>
