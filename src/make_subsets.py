import pandas
import numpy as np
import csv
import time
import os
from csv_to_df import get_hour_glass
from csv_to_df import finishing
import math


class MakeSubsets(object):
    def __init__(self, file_name, csv_destination='../data/goals_after_giveaway.csv'):
        self.setup(file_name, mode=csv_destination)

    def setup(self, file_name, mode):
        self.csv_play_container = []
        csvfile = open(file_name)
        self.csv_reader = csv.reader(csvfile)
        self.is_prev_giveaway = False
        self.blocks=1
        self.is_first_page = True
        self.csv_destination = mode

    def get_time_message(self, time):
        if time > 60:
            return ' Elapsed time: ' + ('{0:' + str(2) +  '.' + str(0) + 'f}').format(time/60) + 'm:' + ('{0:' + str(2) +  '.' + str(0) + 'f}').format(time%60) + 's'
        else:
            return ' Elapsed time: ' + ('{0:' + str(2) +  '.' + str(2) + 'f}').format(time%60) + 's'

    def print_message(self, startTime):
        t1 = startTime
        t2 = time.time()
        print('\r%s %s\r' % (get_time_message(t2-t1), getHourGlass(math.floor((t2-t1 - math.floor(t2-t1)) / 0.125))), end='\r')

    def goals_stoppages_giveaways(self, row):
        if row[5] == 'Giveaway' or row[5] == 'Stoppage' or row[5] == 'Goal':
            self.csv_play_container += [row]

    def all_goals(self, row):
        if row[5] == 'Goal':
            self.csv_play_container += [row]

    def play_after_giveaway(self, row):
        if row[5] == 'Giveaway':
            self.is_prev_giveaway = True
        elif self.is_prev_giveaway == True:
            self.is_prev_giveaway = False
            self.csv_play_container += [row]

    def block_filled(self, index):
        if self.blocks*100000 == index:
            return True
        else:
            return False

    def get_play(self, row):
        if self.csv_destination == '../data/goals_after_giveaway.csv':
            self.goals_stoppages_giveaways(row)
        elif self.csv_destination == '../data/goals.csv':
            self.all_goals(row)
        elif self.csv_destination == '../data/play_after_giveaway.csv':
            self.play_after_giveaway(row)

    def save_df_to_csv(self):
        csv_df = pandas.DataFrame(np.array(self.csv_play_container), columns=self.csv_play_container[0])
        if self.is_first_page is True:
            csv_df = csv_df.drop(csv_df.index[0])
            self.is_first_page = False
        csv_df.to_csv(self.csv_destination, index=False, sep=',', encoding='utf-8', mode='a')
        self.csv_play_container = []
        self.blocks += 1

    def create_subset(self):
        for index, row in enumerate(self.csv_reader):
            if index == 0 and self.is_first_page is True:
                self.csv_play_container = self.csv_play_container + [row]
            self.get_play(row)
            if self.block_filled(index):
                self.save_df_to_csv()
        finishing()


if not os.path.isdir('../data'):
    os.mkdir('../data')

print('\nMaking subset 1/3...\n')

if os.path.exists('../data/goals_after_giveaway.csv'):
    os.remove('../data/goals_after_giveaway.csv')
MakeSubsets('../data/game_plays.csv', '../data/goals_after_giveaway.csv').create_subset()

print('\nMaking subset 2/3...\n')

if os.path.exists('../data/goals.csv'):
    os.remove('../data/goals.csv')
MakeSubsets('../data/game_plays.csv', '../data/goals.csv').create_subset()

print('\nMaking subset 3/3...\n')

if os.path.exists('../data/play_after_giveaway.csv'):
    os.remove('../data/play_after_giveaway.csv')
MakeSubsets('../data/game_plays.csv', '../data/play_after_giveaway.csv').create_subset()

print('\nSubsets successfully created.')
