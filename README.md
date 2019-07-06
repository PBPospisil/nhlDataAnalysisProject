# Data Visualization and Model Testing on 'NHL Game Data' 

Data analysis of the 'NHL Game Data', the dataset from kaggle and contributed by Martin Ellis. This project contains a series of scripts to filter data for processing and visualization. Spanning 6 years and containing rich detail for every play such as location on the ice and secondary play type, this data set motivated an effort to analyze NHL data and reveal new insights and characterize known tendencies. 


## Getting Started
All of the needed libraries are contained in the latest anaconda distribution.
### Prerequisites

```
Python 3
conda 4.5.12
```
## Running Scripts
Download the Kaggle Dataset here: [NHL Game Data](https://www.kaggle.com/martinellis/nhl-game-data)

## Predicting Win Percentage

### Goals Against Average as a predictor
<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/60749022-4dec2600-9f51-11e9-9166-b688f69e0bd6.png' alt='gaa-sv%' width='600'/>
</p>
### Play after a Giveaway
<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/60748876-770bb700-9f4f-11e9-8150-0f58b4e35c35.png' alt='bar-giveaway' width='600'/>
</p>
### Converted Giveaways
Trisurface plot of the number of converted GAs under 10 seconds by distance from GA to net and time
<p align='center'>
  <img src='https://user-images.githubusercontent.com/21959159/58520036-3ca24380-8173-11e9-8646-6cd7a36ec1a7.gif' width='600'>
</p>

![barplot-goal-type-after-GA-under10sec](https://user-images.githubusercontent.com/21959159/58521117-87728a00-8178-11e9-85fe-a43a18417b36.png)


![density-plot-play-until-goal-GA-with-stoppages](https://user-images.githubusercontent.com/21959159/58522103-1634d600-817c-11e9-805c-b34d4bb7f1e2.png)
![density-plot-time-ga-with-stoppages](https://user-images.githubusercontent.com/21959159/58522118-2c429680-817c-11e9-9c90-67f27dc48ee0.png)
![scatter-under-3sec-goals](https://user-images.githubusercontent.com/21959159/58522140-3ebcd000-817c-11e9-82bd-eef97b24b10d.png)

![goalie-top-10-sv%](https://user-images.githubusercontent.com/21959159/58522148-40869380-817c-11e9-840d-8d94bdd0a9aa.png)
![regplot-win%-winPred](https://user-images.githubusercontent.com/21959159/58522149-40869380-817c-11e9-9f48-33ca647cfeaa.png)
![winPred-boston-justGFGA](https://user-images.githubusercontent.com/21959159/58522150-40869380-817c-11e9-9b93-dcc7021f636b.png)
![scatterplot-goalies-win%vsGAA](https://user-images.githubusercontent.com/21959159/58522151-40869380-817c-11e9-86a7-4d94cf59bdf1.png)
