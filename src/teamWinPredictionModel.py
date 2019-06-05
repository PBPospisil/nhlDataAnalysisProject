import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF_largeFile import csvToDF_largeFile
from collections import defaultdict
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import norm
from math import sqrt
import sys
import time

def regression_line_calc(dataframe):
    meanWinPred = dataframe['winPred'].mean()
    meanWinPercentage = dataframe['winPercentage'].mean()
    stdWinPred = dataframe['winPred'].std()
    stdWinPercentage = dataframe['winPercentage'].std()
    n = dataframe['winPred'].count()
    sum_xy = 0
    for index,x in enumerate(dataframe['winPred']):
        sum_xy += (x * dataframe.iloc[index, 6])

    beta = (sum_xy - n * meanWinPred * meanWinPercentage) / ((n-1) * stdWinPred**2)
    alpha = meanWinPercentage - beta * meanWinPred
    return beta, alpha

def userInterfaceOptions():
    print('\n'*100 ,'(1) team predicted and actual win %')
    print(' (2) predicted win % of each team for each season - regplot')
    print(' (3) predicted win % of each team for each season - scatterplot')

    return str(input('\nEnter corresponding option number (q to quit): '))

def quit():
    print('\nExiting', end='', flush=True)
    time.sleep(0.5)
    print('.', end='', flush=True)
    time.sleep(0.5)
    print('.', end='', flush=True)
    time.sleep(0.5)
    print('.', end='', flush=True)
    time.sleep(0.5)
    print('\n', flush=True)

def teamPredictionLinePlot(goalieStatsDF, teamStatsDF, teamOfInterest, beta_, alpha_):

    seasonTeamDF = goalieStatsDF.loc[goalieStatsDF['season'] == 20172018].copy()
    seasonTeamDF.loc[:,'game_id'] = seasonTeamDF.game_id.astype(np.int)
    teamStatsDF.loc[:,'game_id'] = teamStatsDF.game_id.astype(np.int)
    seasonTeamDF = seasonTeamDF.sort_values('game_id', ascending=True, inplace=False)
    teamStatsDF = teamStatsDF.sort_values('game_id', ascending=True, inplace=False)

    gameID = []
    cummgamesPlayed = []
    cummWins = []
    cummGF = []
    cummGA = []
    cummPP = []
    cummPK = []
    predWinPercentage = []
    actualWinPercentage = []
    winPercentageDiff = []
    errorBetweenWinPercentages = []
    prevGame = 0
    GAsum = 0
    GFsum = 0
    GPsum = 0
    PPOPP = 0
    PPG = 0
    PKOPP = 0
    PKSaved = 0
    gamesWinSum = 0
    for index, game in enumerate(seasonTeamDF.loc[seasonTeamDF['team_id'] == teamOfInterest, 'game_id'].unique()):
        teamsInGame = []
        GPsum += 1
        for team in seasonTeamDF.loc[seasonTeamDF['game_id'] == game, 'team_id']:
            if team == teamOfInterest and seasonTeamDF.iloc[index, 15] == 'W' and team not in teamsInGame:
                gamesWinSum += 1
            elif team == teamOfInterest and team not in teamsInGame:
                GAsum += (seasonTeamDF.iloc[index, 13] - seasonTeamDF.iloc[index, 11])
            elif team == teamOfInterest and team in teamsInGame:
                GAsum += (seasonTeamDF.iloc[index, 13] - seasonTeamDF.iloc[index, 11])
            elif team != teamOfInterest:
                GFsum += (seasonTeamDF.iloc[index, 13] - seasonTeamDF.iloc[index, 11])
            teamsInGame.append(team)

        for innerindex, team in enumerate(teamStatsDF.loc[teamStatsDF['game_id'] == game, 'team_id']):
            if team == teamOfInterest:
                PPOPP += teamStatsDF.iloc[innerindex, 10]
                PPG += teamStatsDF.iloc[innerindex, 11]
            else:
                PKOPP += teamStatsDF.iloc[innerindex, 10]
                PKSaved += teamStatsDF.iloc[innerindex, 10] - teamStatsDF.iloc[innerindex, 11]

        cummGA.append(GAsum)
        cummGF.append(GFsum)

        if PPOPP == 0 or PKOPP == 0:
            cummPK.append(PKSaved / 1)
            cummPP.append(PPG / 1)
        else:
            cummPK.append(PKSaved / PKOPP)
            cummPP.append(PPG / PPOPP)

        cummWins.append(gamesWinSum)
        cummgamesPlayed.append(GPsum)

        winPrediction = ((GFsum / GAsum) + cummPK[-1]*cummPP[-1] ) * 0.9
        predWinPercentage.append(alpha_ + beta_ * winPrediction)
        actualWinPercentage.append(gamesWinSum / GPsum)
        winPercentageDiff.append(abs(predWinPercentage[-1] - actualWinPercentage[-1]))
        if actualWinPercentage[-1] == 0:
            errorBetweenWinPercentages.append(abs(winPercentageDiff[-1] / 1))
        else:
            errorBetweenWinPercentages.append(abs(winPercentageDiff[-1] / actualWinPercentage[-1]))
        gameID.append(GPsum)

    winPredictionDF = pandas.DataFrame(np.array(gameID), columns=['game_id'])
    winPredictionDF['predWinPercentage'] = predWinPercentage
    winPredictionDF['actualWinPercentage'] = actualWinPercentage
    winPredictionDF['winPercentageDiff'] = winPercentageDiff
    winPredictionDF['error'] = errorBetweenWinPercentages

    return winPredictionDF


teamInfo = csvToDF('../data/teamInfo.')
goalieStatsDF = csvToDF('../data/game_goalie_stats.csv')
gameDF = csvToDF('../data/game.csv')
teamStatsDF = csvToDF('../data/game_teams_stats.csv')

goalieStatsDF.loc[:,'timeOnIce'] = goalieStatsDF.timeOnIce.astype(np.int)

seasons = []
teamSeasonIdDictList = []
ID = 1
teamSeasonIdDict = defaultdict(int)

for game in goalieStatsDF['game_id'].unique():
    if gameDF.loc[gameDF['game_id'] == game, 'type'].item() == 'P':
        goalieStatsDF.drop(goalieStatsDF.loc[goalieStatsDF['game_id'] == game].index, inplace=True)
        teamStatsDF.drop(teamStatsDF.loc[teamStatsDF['game_id'] == game].index, inplace=True)

for game in goalieStatsDF['game_id']:
    seasons.append(gameDF.loc[gameDF['game_id'] == game, 'season'].item())

goalieStatsDF['season'] = seasons

goalieStatsDF.loc[:,'season'] = goalieStatsDF.season.astype(str)

teamSeasons = []
for game in teamStatsDF['game_id']:
    teamSeasons.append(gameDF.loc[gameDF['game_id'] == game, 'season'].item())
teamStatsDF['season'] = teamSeasons

for index, _ in enumerate(goalieStatsDF['game_id']):

    if teamSeasonIdDict[' '.join([goalieStatsDF.iloc[index, 2], goalieStatsDF.iloc[index, 19]])] == 0:
        teamSeasonIdDict[' '.join([goalieStatsDF.iloc[index, 2], goalieStatsDF.iloc[index, 19]])] = ID
        teamSeasonIdDictList.append(' '.join([goalieStatsDF.iloc[index, 2], goalieStatsDF.iloc[index, 19]]))
        ID += 1
    else:
        teamSeasonIdDictList.append(' '.join([goalieStatsDF.iloc[index, 2], goalieStatsDF.iloc[index, 19]]))


goalieStatsDF['teamSeasonIdDictList'] = teamSeasonIdDictList

goalieStatsDF = goalieStatsDF.drop(goalieStatsDF.loc[goalieStatsDF['savePercentage'] == 'NA'].index)

goalieStatsDF.loc[:,'savePercentage'] = goalieStatsDF.savePercentage.astype(np.float)
goalieStatsDF.loc[:,'evenShotsAgainst'] = goalieStatsDF.evenShotsAgainst.astype(np.int)
goalieStatsDF.loc[:,'evenSaves'] = goalieStatsDF.evenSaves.astype(np.int)
goalieStatsDF.loc[:,'shortHandedSaves'] = goalieStatsDF.shortHandedSaves.astype(np.int)
goalieStatsDF.loc[:,'shortHandedShotsAgainst'] = goalieStatsDF.shortHandedShotsAgainst.astype(np.int)


teamStatsDF.loc[:,'goals'] = teamStatsDF.goals.astype(np.int)
teamStatsDF.loc[:,'shots'] = teamStatsDF.shots.astype(np.int)
teamStatsDF.loc[:,'powerPlayOpportunities'] = teamStatsDF.powerPlayOpportunities.astype(np.int)
teamStatsDF.loc[:,'powerPlayGoals'] = teamStatsDF.powerPlayGoals.astype(np.int)
teamStatsDF.loc[:,'faceOffWinPercentage'] = teamStatsDF.faceOffWinPercentage.astype(np.float)

oneSeasonEntire = pandas.DataFrame(np.zeros(len(teamSeasonIdDict)))
oneSeasonEntire['teamSeasonIdDictList'] = teamSeasonIdDict.keys()
oneSeasonEntire['totalTOI'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['wins'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['GAA'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['savePercentage'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['gamesPlayed'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['winPercentage'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['shots'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['saves'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['PPO'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['PPG'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['PKSaved'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['PKOPP'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['FOWinP'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['FOs'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['winPred'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['GF'] = np.zeros(len(oneSeasonEntire))
oneSeasonEntire['shotsFor'] = np.zeros(len(oneSeasonEntire))

oneSeasonEntire.drop(0, axis=1, inplace=True)

oneSeasonEntireSeasons = []
oneSeasonTeam = []
gameID = []

for outerIndex, teamSeason in enumerate(oneSeasonEntire['teamSeasonIdDictList']):
    [team, season] = str(teamSeason).split(' ')
    oneSeasonEntireSeasons.append(season)
    oneSeasonTeam.append(team)
    teamSpecific = goalieStatsDF.loc[goalieStatsDF['team_id'] == team]
    teamSpecificPPFO = teamStatsDF.loc[teamStatsDF['team_id'] == team]
    teamSpecificPPFOinv = teamStatsDF.loc[teamStatsDF['team_id'] != team]
    for innerIndex, game in enumerate(teamSpecificPPFO['game_id']):
        if teamSpecificPPFO.iloc[innerIndex, 15] == season:
            oneSeasonEntire.iloc[outerIndex, 9] += teamSpecificPPFO.iloc[innerIndex, 10]

            oneSeasonEntire.iloc[outerIndex, 10] += teamSpecificPPFO.iloc[innerIndex, 11]

            oneSeasonEntire.iloc[outerIndex, 11] += teamSpecificPPFOinv.iloc[innerIndex, 10]-teamSpecificPPFOinv.iloc[innerIndex, 11]

            oneSeasonEntire.iloc[outerIndex, 12] += teamSpecificPPFOinv.iloc[innerIndex, 10]

            oneSeasonEntire.iloc[outerIndex, 13] += teamSpecificPPFO.iloc[innerIndex, 12]

            oneSeasonEntire.iloc[outerIndex, 14] += 1

            oneSeasonEntire.iloc[outerIndex, 16] += teamSpecificPPFO.iloc[innerIndex, 6] - teamSpecificPPFO.iloc[innerIndex, 11]

            oneSeasonEntire.iloc[outerIndex, 17] += teamSpecificPPFO.iloc[innerIndex, 7] - teamSpecificPPFO.iloc[innerIndex, 11]

    for innerIndex, _ in enumerate(teamSpecific['game_id']):
        if teamSpecific.iloc[innerIndex, 19] == season:
            # shots
            oneSeasonEntire.iloc[outerIndex, 7] += teamSpecific.iloc[innerIndex, 13]

            #saves
            oneSeasonEntire.iloc[outerIndex, 8] += teamSpecific.iloc[innerIndex, 11]

            #totalTOI
            oneSeasonEntire.iloc[outerIndex, 1] += teamSpecific.iloc[innerIndex, 3]

            #wins
            if teamSpecific.iloc[innerIndex, 15] == 'W':
                oneSeasonEntire.iloc[outerIndex, 2] += 1
            oneSeasonEntire.iloc[outerIndex, 5] += 1

    oneSeasonEntire.iloc[outerIndex, 3] = ((oneSeasonEntire.iloc[outerIndex, 7] - oneSeasonEntire.iloc[outerIndex, 8]) * 3600) / oneSeasonEntire.iloc[outerIndex, 1]

    if oneSeasonEntire.iloc[outerIndex, 7] != 0:
        oneSeasonEntire.iloc[outerIndex, 4] = int(oneSeasonEntire.iloc[outerIndex, 8]) / int(oneSeasonEntire.iloc[outerIndex, 7])
    oneSeasonEntire.iloc[outerIndex, 6] = oneSeasonEntire.iloc[outerIndex, 2] / oneSeasonEntire.iloc[outerIndex, 5]

    PPPercentage = oneSeasonEntire.iloc[outerIndex, 10] / oneSeasonEntire.iloc[outerIndex, 9]
    SHPercentage = oneSeasonEntire.iloc[outerIndex, 11] / oneSeasonEntire.iloc[outerIndex, 12]
    FOPercentage = oneSeasonEntire.iloc[outerIndex, 13] / oneSeasonEntire.iloc[outerIndex, 14]
    GFPercentage = oneSeasonEntire.iloc[outerIndex, 16] / oneSeasonEntire.iloc[outerIndex, 17]
    GFA = (oneSeasonEntire.iloc[outerIndex, 16] * 3600) / oneSeasonEntire.iloc[outerIndex, 1]

    oneSeasonEntire.iloc[outerIndex, 15] = ((GFA / oneSeasonEntire.iloc[outerIndex, 3]) + (PPPercentage*SHPercentage))

oneSeasonEntire['season'] = oneSeasonEntireSeasons
oneSeasonEntire['team_id'] = oneSeasonTeam

print('Correlation coefficient for regression data: ', oneSeasonEntire['winPred'].corr(oneSeasonEntire['winPercentage']))

oneSeasonEntire.loc[:,'season'] = oneSeasonEntire.season.astype(np.int)
oneSeasonEntire.loc[:,'team_id'] = oneSeasonEntire.team_id.astype(np.int)

while (1):
    userChoice = userInterfaceOptions()
    if userChoice == '1':
        print('\n\nTeam --- ID\n')
        for index, team in enumerate(teamInfo['team_id']):
            print(teamInfo.iloc[index,2] + ' ' + teamInfo.iloc[index,3] + ' --- ' + team)

        mainTeam = str(input('\nEnter the team ID to view a specific team chart (q to quit): '))
        if mainTeam == 'q':
            quit()
            break
        elif not mainTeam.isnumeric() or int(mainTeam) < 1 or int(mainTeam) > 53:
            print('Input is not a number in the proper range.')
            continue
        if mainTeam not in teamInfo['team_id'].unique():
            print('Input is not a team id.')
            continue
        shortNameMainTeam = teamInfo.loc[teamInfo['team_id'] == mainTeam, 'shortName'].item()
        teamNameMainTeam = teamInfo.loc[teamInfo['team_id'] == mainTeam, 'teamName'].item()

        teamOfInterest = int(mainTeam)

        goalieStatsDF.loc[:,'season'] = goalieStatsDF.season.astype(np.int)
        goalieStatsDF.loc[:,'team_id'] = goalieStatsDF.team_id.astype(np.int)

        beta, alpha = regression_line_calc(oneSeasonEntire)

        winPredictionDF = teamPredictionLinePlot(goalieStatsDF, teamStatsDF, teamOfInterest, beta, alpha)

        line1 = plt.plot(winPredictionDF['game_id'], winPredictionDF['predWinPercentage'], label='Predicted win%', linestyle='-')
        line2 = plt.plot(winPredictionDF['game_id'], winPredictionDF['actualWinPercentage'], label='Actual win%', linestyle='--')
        line3 = plt.plot(winPredictionDF['game_id'], winPredictionDF['winPercentageDiff'], label='Difference in Pred. vs. Actual', linestyle='-.')
        line4 = plt.plot(winPredictionDF['game_id'], winPredictionDF['error'], label='Prediction Error', linestyle=':')

        plt.legend()
        plt.xlabel('Game')
        plt.ylabel('Win Prediction')
        plt.title('Predicted win %, actual win %, of the ' + shortNameMainTeam + ' ' + teamNameMainTeam + ' in the 2017-2018 season')
        figureName = '../img/win-prediction-winpercentage-error.png'
    elif userChoice == '2':
        ax = sns.regplot(x='winPred', y='winPercentage', data=oneSeasonEntire)
        plt.xlabel('Win Prediction')
        plt.ylabel('Win Percentage')
        plt.title('Win percentage vs. win prediction of each season for every team 2012-2018')
        figureName = '../img/win-prediction-winpercentage-regplot.png'

    elif userChoice == '3':
        ax = sns.scatterplot(x='winPred', y='winPercentage', data=oneSeasonEntire)
        plt.xlabel('Win Prediction')
        plt.ylabel('Win Percentage')
        plt.title('Win percentage vs. win prediction of each season for every team 2012-2018')
        figureName = '../img/win-prediction-winpercentage-scatterplot.png'

    elif userChoice == 'q':
        quit()
        break
    else:
        continue

    checkAndMakeImgFolder()

    os.remove(figureName)
    plt.savefig(figureName, bbox_inches='tight')

#
