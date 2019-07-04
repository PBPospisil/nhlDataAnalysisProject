import os
import pandas
import numpy as np
import csv
from csvToDF import csvToDF
from csvToDF import checkAndMakeImgFolder
from collections import defaultdict
import matplotlib.pyplot as plt
from scipy.stats import norm
import sys
import time
from graph_data import GraphData


class UiElement(object):

    def __init__(self):
        pass

    def quit(self, delay=0):
        print('\nExiting', end='', flush=True)
        time.sleep(delay)
        print('.', end='', flush=True)
        time.sleep(delay)
        print('.', end='', flush=True)
        time.sleep(delay)
        print('.', end='', flush=True)
        time.sleep(delay)
        print('\n', flush=True)

    def user_interface_options(self):
        print('\n'*100 ,'(1) team predicted and actual win %')
        print(' (2) predicted win % of each team for each season - regplot')
        print(' (3) predicted win % of each team for each season - scatterplot')

        return str(input('\nEnter corresponding option number (q to quit): '))

    def show_team_menu(self, win_prediction):
        while(1):
            print('\n\nTeam --- ID\n')
            for index, team in enumerate(win_prediction.team_info['team_id']):
                print(win_prediction.team_info.iloc[index,2] + ' ' + win_prediction.team_info.iloc[index,3] + ' --- ' + team)
            main_team = str(input('\nEnter the team ID to view a specific team chart: '))

            if not main_team.isnumeric() or int(main_team) < 1 or int(main_team) > 53:
                print('Input is not a number in the proper range.')
                continue
            if main_team not in win_prediction.team_info['team_id'].unique():
                print('Input is not a team id.')
                continue
            else:
                break

        return [win_prediction.team_info.loc[win_prediction.team_info['team_id'] == main_team, 'shortName'].item(),
                win_prediction.team_info.loc[win_prediction.team_info['team_id'] == main_team, 'teamName'].item(),
                main_team]

    def menu_branches(self, win_prediction, userChoice):
        if userChoice == '1':
            win_prediction.graph_model_error(self.show_team_menu(win_prediction))
        elif userChoice == '2':
            win_prediction.graph_model_regplot()
        elif userChoice == '3':
            win_prediction.graph_model_scatterplot()
        elif userChoice == 'test':
            win_prediction.graph_all_teams_for_epsilon()
        elif userChoice == 'alpha':
            win_prediction.find_op_alpha()
        elif userChoice == 'alphav2':
            win_prediction.season_op_alpha()
        elif userChoice == 'q':
            return 'q'

    def menu_and_save_graph(self, win_prediction):
        while (1):
            if self.menu_branches(win_prediction, self.user_interface_options()) == 'q':
                self.quit()
                break
