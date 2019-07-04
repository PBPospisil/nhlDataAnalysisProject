import pandas
import numpy as np
import csv
import time
import os
from csvToDF import getHourGlass
from csvToDF import finishing
import math


def getTimeMessage(time):
    if time > 60:
        return ' Elapsed time: ' + ('{0:' + str(2) +  '.' + str(0) + 'f}').format(time/60) + 'm:' + ('{0:' + str(2) +  '.' + str(0) + 'f}').format(time%60) + 's'
    else:
        return ' Elapsed time: ' + ('{0:' + str(2) +  '.' + str(2) + 'f}').format(time%60) + 's'

def printMessage(startTime):
    t1 = startTime
    t2 = time.time()
    print('\r%s %s\r' % (getTimeMessage(t2-t1), getHourGlass(math.floor((t2-t1 - math.floor(t2-t1)) / 0.125))), end='\r')


def filterCsvForGoalsAfterGA(csvfile):
    csv_arr = []
    time_difference = []
    csvfile_f = open(csvfile)
    csv_reader = csv.reader(csvfile_f)
    isPrevGA = False
    j=1
    lines = 0
    isFirstPage = True
    t1 = time.time()

    for index, row in enumerate(csv_reader):
        if index == 0 and isFirstPage is True:
            csv_arr = csv_arr + [row]

        if row[5] == 'Giveaway' or row[5] == 'Stoppage' or row[5] == 'Goal':
            csv_arr += [row]

        printMessage(t1)

        if j*100000 == index:

            csv_df = pandas.DataFrame(np.array(csv_arr), columns=csv_arr[0])
            if isFirstPage is True:
                csv_df = csv_df.drop(csv_df.index[0])
                isFirstPage = False

            csv_df.to_csv('../data/goals_after_giveaway.csv', index=False, sep=',', encoding='utf-8', mode='a')
            csv_arr = []

            j += 1

    finishing()


def filterCsvForAllGoals(csvfile):
    csv_arr = []
    time_difference = []
    csvfile_f = open(csvfile)
    csv_reader = csv.reader(csvfile_f)
    isPrevGA = False
    j=1
    lines = 0
    isFirstPage = True
    t1 = time.time()

    for index, row in enumerate(csv_reader):
        if index == 0 and isFirstPage is True:
            csv_arr = csv_arr + [row]

        if row[5] == 'Goal':
            csv_arr += [row]

        printMessage(t1)

        if j*100000 == index:

            csv_df = pandas.DataFrame(np.array(csv_arr), columns=csv_arr[0])
            if isFirstPage is True:
                csv_df = csv_df.drop(csv_df.index[0])
                isFirstPage = False

            csv_df.to_csv('../data/goals.csv', index=False, sep=',', encoding='utf-8', mode='a')
            csv_arr = []

            j += 1
    finishing()


def filterCsvForPlaysAfterGA(csvfile):
    csv_arr = []
    time_difference = []
    csvfile_f = open(csvfile)
    csv_reader = csv.reader(csvfile_f)
    isPrevGA = False
    j=1
    lines = 0
    isFirstPage = True
    t1 = time.time()

    for index, row in enumerate(csv_reader):
        if index == 0 and isFirstPage is True:
            csv_arr = csv_arr + [row]

        if row[5] == 'Giveaway':
            lines += 1
            isPrevGA = True
        elif isPrevGA == True:
            isPrevGA = False
            csv_arr += [row]

        printMessage(t1)

        if j*100000 == index:

            csv_df = pandas.DataFrame(np.array(csv_arr), columns=csv_arr[0])
            if isFirstPage is True:
                csv_df = csv_df.drop(csv_df.index[0])
                isFirstPage = False

            csv_df.to_csv('../data/play_after_GA.csv', index=False, sep=',', encoding='utf-8', mode='a')
            csv_arr = []

            j += 1
    finishing()


if not os.path.isdir('../data'):
    os.mkdir('../data')

print('\nMaking subset 1/3...\n')

if os.path.exists('../data/goals_after_giveaway.csv'):
    os.remove('../data/goals_after_giveaway.csv')
filterCsvForGoalsAfterGA('../../../game_plays.csv')

print('\nMaking subset 2/3...\n')

if os.path.exists('../data/goals.csv'):
    os.remove('../data/goals.csv')
filterCsvForAllGoals('../../../game_plays.csv')

print('\nMaking subset 3/3...\n')

if os.path.exists('../data/play_after_GA.csv'):
    os.remove('../data/play_after_GA.csv')
filterCsvForPlaysAfterGA('../../../game_plays.csv')

print('\nSubsets successfully created.')
