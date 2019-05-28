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
from get_goalie_to_subtractGAA_from_csv import extractFromCsv
from scipy.stats import norm
from math import sqrt
import sys
import time

def regression_line_calc(dataframe):
    mean_winPred = dataframe['winPred'].mean()
    mean_winPercentage = dataframe['winPercentage'].mean()
    std_winPred = dataframe['winPred'].std()
    std_winPercentage = dataframe['winPercentage'].std()
    n = dataframe['winPred'].count()
    sum_xy = 0
    for index,x in enumerate(dataframe['winPred']):
        sum_xy += (x * dataframe.iloc[index, 6])

    beta = (sum_xy - n * mean_winPred * mean_winPercentage) / ((n-1) * std_winPred**2)
    alpha = mean_winPercentage - beta * mean_winPred
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

def teamPredictionLinePlot(goalie_stats_df, team_stats_df, teamOfInterest, beta_, alpha_):

    season_team_df = goalie_stats_df.loc[goalie_stats_df['season'] == 20172018].copy()
    season_team_df.loc[:,'game_id'] = season_team_df.game_id.astype(np.int)
    team_stats_df.loc[:,'game_id'] = team_stats_df.game_id.astype(np.int)
    season_team_df = season_team_df.sort_values('game_id', ascending=True, inplace=False)
    team_stats_df = team_stats_df.sort_values('game_id', ascending=True, inplace=False)

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
    for index, game in enumerate(season_team_df.loc[season_team_df['team_id'] == teamOfInterest, 'game_id'].unique()):
        teamsInGame = []
        GPsum += 1
        for team in season_team_df.loc[season_team_df['game_id'] == game, 'team_id']:
            if team == teamOfInterest and season_team_df.iloc[index, 15] == 'W' and team not in teamsInGame:
                gamesWinSum += 1
            elif team == teamOfInterest and team not in teamsInGame:
                GAsum += (season_team_df.iloc[index, 13] - season_team_df.iloc[index, 11])
            elif team == teamOfInterest and team in teamsInGame:
                GAsum += (season_team_df.iloc[index, 13] - season_team_df.iloc[index, 11])
            elif team != teamOfInterest:
                GFsum += (season_team_df.iloc[index, 13] - season_team_df.iloc[index, 11])
            teamsInGame.append(team)

        for innerindex, team in enumerate(team_stats_df.loc[team_stats_df['game_id'] == game, 'team_id']):
            if team == teamOfInterest:
                PPOPP += team_stats_df.iloc[innerindex, 10]
                PPG += team_stats_df.iloc[innerindex, 11]
            else:
                PKOPP += team_stats_df.iloc[innerindex, 10]
                PKSaved += team_stats_df.iloc[innerindex, 10] - team_stats_df.iloc[innerindex, 11]

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
        #winPrediction = (GFsum / GAsum)
        predWinPercentage.append(alpha_ + beta_ * winPrediction)
        actualWinPercentage.append(gamesWinSum / GPsum)
        winPercentageDiff.append(abs(predWinPercentage[-1] - actualWinPercentage[-1]))
        if actualWinPercentage[-1] == 0:
            errorBetweenWinPercentages.append(abs(winPercentageDiff[-1] / 1))
        else:
            errorBetweenWinPercentages.append(abs(winPercentageDiff[-1] / actualWinPercentage[-1]))
        gameID.append(GPsum)

    win_prediction_df = pandas.DataFrame(np.array(gameID), columns=['game_id'])
    win_prediction_df['predWinPercentage'] = predWinPercentage
    win_prediction_df['actualWinPercentage'] = actualWinPercentage
    win_prediction_df['winPercentageDiff'] = winPercentageDiff
    win_prediction_df['error'] = errorBetweenWinPercentages

    return win_prediction_df


team_info = csvToDF('../team_info.csv')
goalie_stats_df = csvToDF('../game_goalie_stats.csv')
game_df = csvToDF('../game.csv')
team_stats_df = csvToDF('../game_teams_stats.csv')

goalie_stats_df.loc[:,'timeOnIce'] = goalie_stats_df.timeOnIce.astype(np.int)

seasons = []
team_season_id = []
ID = 1
teamSeasonID = defaultdict(int)

for game in goalie_stats_df['game_id'].unique():
    if game_df.loc[game_df['game_id'] == game, 'type'].item() == 'P':
        goalie_stats_df.drop(goalie_stats_df.loc[goalie_stats_df['game_id'] == game].index, inplace=True)
        team_stats_df.drop(team_stats_df.loc[team_stats_df['game_id'] == game].index, inplace=True)

for game in goalie_stats_df['game_id']:
    seasons.append(game_df.loc[game_df['game_id'] == game, 'season'].item())

goalie_stats_df['season'] = seasons

goalie_stats_df.loc[:,'season'] = goalie_stats_df.season.astype(str)

teamSeasons = []
for game in team_stats_df['game_id']:
    teamSeasons.append(game_df.loc[game_df['game_id'] == game, 'season'].item())
team_stats_df['season'] = teamSeasons

for index, _ in enumerate(goalie_stats_df['game_id']):

    if teamSeasonID[' '.join([goalie_stats_df.iloc[index, 2], goalie_stats_df.iloc[index, 19]])] == 0:
        teamSeasonID[' '.join([goalie_stats_df.iloc[index, 2], goalie_stats_df.iloc[index, 19]])] = ID
        team_season_id.append(' '.join([goalie_stats_df.iloc[index, 2], goalie_stats_df.iloc[index, 19]]))
        ID += 1
    else:
        team_season_id.append(' '.join([goalie_stats_df.iloc[index, 2], goalie_stats_df.iloc[index, 19]]))


goalie_stats_df['team_season_id'] = team_season_id

goalie_stats_df = goalie_stats_df.drop(goalie_stats_df.loc[goalie_stats_df['savePercentage'] == 'NA'].index)

goalie_stats_df.loc[:,'savePercentage'] = goalie_stats_df.savePercentage.astype(np.float)
goalie_stats_df.loc[:,'evenShotsAgainst'] = goalie_stats_df.evenShotsAgainst.astype(np.int)
goalie_stats_df.loc[:,'evenSaves'] = goalie_stats_df.evenSaves.astype(np.int)
goalie_stats_df.loc[:,'shortHandedSaves'] = goalie_stats_df.shortHandedSaves.astype(np.int)
goalie_stats_df.loc[:,'shortHandedShotsAgainst'] = goalie_stats_df.shortHandedShotsAgainst.astype(np.int)


team_stats_df.loc[:,'goals'] = team_stats_df.goals.astype(np.int)
team_stats_df.loc[:,'shots'] = team_stats_df.shots.astype(np.int)
team_stats_df.loc[:,'powerPlayOpportunities'] = team_stats_df.powerPlayOpportunities.astype(np.int)
team_stats_df.loc[:,'powerPlayGoals'] = team_stats_df.powerPlayGoals.astype(np.int)
team_stats_df.loc[:,'faceOffWinPercentage'] = team_stats_df.faceOffWinPercentage.astype(np.float)

one_season_entire = pandas.DataFrame(np.zeros(len(teamSeasonID)))
one_season_entire['team_season_id'] = teamSeasonID.keys()
one_season_entire['totalTOI'] = np.zeros(len(one_season_entire))
one_season_entire['wins'] = np.zeros(len(one_season_entire))
one_season_entire['GAA'] = np.zeros(len(one_season_entire))
one_season_entire['savePercentage'] = np.zeros(len(one_season_entire))
one_season_entire['gamesPlayed'] = np.zeros(len(one_season_entire))
one_season_entire['winPercentage'] = np.zeros(len(one_season_entire))
one_season_entire['shots'] = np.zeros(len(one_season_entire))
one_season_entire['saves'] = np.zeros(len(one_season_entire))
one_season_entire['PPO'] = np.zeros(len(one_season_entire))
one_season_entire['PPG'] = np.zeros(len(one_season_entire))
one_season_entire['PKSaved'] = np.zeros(len(one_season_entire))
one_season_entire['PKOPP'] = np.zeros(len(one_season_entire))
one_season_entire['FOWinP'] = np.zeros(len(one_season_entire))
one_season_entire['FOs'] = np.zeros(len(one_season_entire))
one_season_entire['winPred'] = np.zeros(len(one_season_entire))
one_season_entire['GF'] = np.zeros(len(one_season_entire))
one_season_entire['shotsFor'] = np.zeros(len(one_season_entire))

one_season_entire.drop(0, axis=1, inplace=True)

one_season_entire_seasons = []
one_season_team = []
gameID = []

for outerIndex, teamSeason in enumerate(one_season_entire['team_season_id']):
    [team, season] = str(teamSeason).split(' ')
    one_season_entire_seasons.append(season)
    one_season_team.append(team)
    team_specific = goalie_stats_df.loc[goalie_stats_df['team_id'] == team]
    team_specific_PPFO = team_stats_df.loc[team_stats_df['team_id'] == team]
    team_specific_PPFOinv = team_stats_df.loc[team_stats_df['team_id'] != team]
    for innerIndex, game in enumerate(team_specific_PPFO['game_id']):
        if team_specific_PPFO.iloc[innerIndex, 15] == season:
            one_season_entire.iloc[outerIndex, 9] += team_specific_PPFO.iloc[innerIndex, 10]

            one_season_entire.iloc[outerIndex, 10] += team_specific_PPFO.iloc[innerIndex, 11]

            one_season_entire.iloc[outerIndex, 11] += team_specific_PPFOinv.iloc[innerIndex, 10]-team_specific_PPFOinv.iloc[innerIndex, 11]

            one_season_entire.iloc[outerIndex, 12] += team_specific_PPFOinv.iloc[innerIndex, 10]

            one_season_entire.iloc[outerIndex, 13] += team_specific_PPFO.iloc[innerIndex, 12]

            one_season_entire.iloc[outerIndex, 14] += 1

            one_season_entire.iloc[outerIndex, 16] += team_specific_PPFO.iloc[innerIndex, 6] - team_specific_PPFO.iloc[innerIndex, 11]

            one_season_entire.iloc[outerIndex, 17] += team_specific_PPFO.iloc[innerIndex, 7] - team_specific_PPFO.iloc[innerIndex, 11]

    for innerIndex, _ in enumerate(team_specific['game_id']):
        if team_specific.iloc[innerIndex, 19] == season:
            # shots
            one_season_entire.iloc[outerIndex, 7] += team_specific.iloc[innerIndex, 13]

            #saves
            one_season_entire.iloc[outerIndex, 8] += team_specific.iloc[innerIndex, 11]

            #totalTOI
            one_season_entire.iloc[outerIndex, 1] += team_specific.iloc[innerIndex, 3]

            #wins
            if team_specific.iloc[innerIndex, 15] == 'W':
                one_season_entire.iloc[outerIndex, 2] += 1
            one_season_entire.iloc[outerIndex, 5] += 1

    one_season_entire.iloc[outerIndex, 3] = ((one_season_entire.iloc[outerIndex, 7] - one_season_entire.iloc[outerIndex, 8]) * 3600) / one_season_entire.iloc[outerIndex, 1]

    if one_season_entire.iloc[outerIndex, 7] != 0:
        one_season_entire.iloc[outerIndex, 4] = int(one_season_entire.iloc[outerIndex, 8]) / int(one_season_entire.iloc[outerIndex, 7])
    one_season_entire.iloc[outerIndex, 6] = one_season_entire.iloc[outerIndex, 2] / one_season_entire.iloc[outerIndex, 5]

    PPPercentage = one_season_entire.iloc[outerIndex, 10] / one_season_entire.iloc[outerIndex, 9]
    SHPercentage = one_season_entire.iloc[outerIndex, 11] / one_season_entire.iloc[outerIndex, 12]
    FOPercentage = one_season_entire.iloc[outerIndex, 13] / one_season_entire.iloc[outerIndex, 14]
    GFPercentage = one_season_entire.iloc[outerIndex, 16] / one_season_entire.iloc[outerIndex, 17]
    GFA = (one_season_entire.iloc[outerIndex, 16] * 3600) / one_season_entire.iloc[outerIndex, 1]

    one_season_entire.iloc[outerIndex, 15] = ((GFA / one_season_entire.iloc[outerIndex, 3]) + (PPPercentage*SHPercentage))

one_season_entire['season'] = one_season_entire_seasons
one_season_entire['team_id'] = one_season_team

print('Correlation coefficient for regression data: ', one_season_entire['winPred'].corr(one_season_entire['winPercentage']))

one_season_entire.loc[:,'season'] = one_season_entire.season.astype(np.int)
one_season_entire.loc[:,'team_id'] = one_season_entire.team_id.astype(np.int)

while (1):
    userChoice = userInterfaceOptions()
    if userChoice == '1':
        print('\n\nTeam --- ID\n')
        for index, team in enumerate(team_info['team_id']):
            print(team_info.iloc[index,2] + ' ' + team_info.iloc[index,3] + ' --- ' + team)

        main_team = str(input('\nEnter the team ID to view a specific team chart (q to quit): '))
        if main_team == 'q':
            quit()
            break
        elif not main_team.isnumeric() or int(main_team) < 1 or int(main_team) > 53:
            print('Input is not a number in the proper range.')
            continue
        if main_team not in team_info['team_id'].unique():
            print('Input is not a team id.')
            continue
        short_name_main_team = team_info.loc[team_info['team_id'] == main_team, 'shortName'].item()
        team_name_main_team = team_info.loc[team_info['team_id'] == main_team, 'teamName'].item()

        teamOfInterest = int(main_team)

        goalie_stats_df.loc[:,'season'] = goalie_stats_df.season.astype(np.int)
        goalie_stats_df.loc[:,'team_id'] = goalie_stats_df.team_id.astype(np.int)

        beta, alpha = regression_line_calc(one_season_entire)

        win_prediction_df = teamPredictionLinePlot(goalie_stats_df, team_stats_df, teamOfInterest, beta, alpha)

        line1 = plt.plot(win_prediction_df['game_id'], win_prediction_df['predWinPercentage'], label='Predicted win%', linestyle='-')
        line2 = plt.plot(win_prediction_df['game_id'], win_prediction_df['actualWinPercentage'], label='Actual win%', linestyle='--')
        line3 = plt.plot(win_prediction_df['game_id'], win_prediction_df['winPercentageDiff'], label='Difference in Pred. vs. Actual', linestyle='-.')
        line4 = plt.plot(win_prediction_df['game_id'], win_prediction_df['error'], label='Prediction Error', linestyle=':')

        plt.legend()
        plt.xlabel('Game')
        plt.ylabel('Win Prediction')
        plt.title('Predicted win %, actual win %, of the ' + short_name_main_team + ' ' + team_name_main_team + ' in the 2017-2018 season')

    elif userChoice == '2':
        ax = sns.regplot(x='winPred', y='winPercentage', data=one_season_entire)
        plt.xlabel('Win Prediction')
        plt.ylabel('Win Percentage')
        plt.title('Win percentage vs. win prediction of each season for every team 2012-2018')

    elif userChoice == '3':
        ax = sns.scatterplot(x='winPred', y='winPercentage', data=one_season_entire)
        plt.xlabel('Win Prediction')
        plt.ylabel('Win Percentage')
        plt.title('Win percentage vs. win prediction of each season for every team 2012-2018')

    elif userChoice == 'q':
        quit()
        break
    else:
        continue

    plt.show()

#
