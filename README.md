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
Goals Against Average (GAA) is shown here to have a weak correlation with Goaltender Win Percentage. One reason for this is that goals are complex events that are influenced by other players including a goaltender's teammate(s); because of this GAA is stronger predictor for Team Win Percentage.

#### Team Win Percentage
<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/60953113-c3d9ef80-a2b9-11e9-8f0b-f400234da641.png' alt='gaa-win%-teams' width='580'/>
</p>

### Play after a Giveaway
<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/61005094-bad23800-a324-11e9-9add-55ac5d469e81.png' alt='bar-giveaway' width='600'/>
</p>

### Converted Giveaways
Trisurface plot of the number of converted GAs under 10 seconds by distance from GA to net and time
<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/58520036-3ca24380-8173-11e9-8646-6cd7a36ec1a7.gif' alt='gif'          width='600'/>
</p>

![barplot-goal-type-after-GA-under10sec](https://user-images.githubusercontent.com/21959159/58521117-87728a00-8178-11e9-85fe-a43a18417b36.png)



![scatter-under-3sec-goals](https://user-images.githubusercontent.com/21959159/58522140-3ebcd000-817c-11e9-82bd-eef97b24b10d.png)

![goalie-top-10-sv%](https://user-images.githubusercontent.com/21959159/58522148-40869380-817c-11e9-840d-8d94bdd0a9aa.png)
