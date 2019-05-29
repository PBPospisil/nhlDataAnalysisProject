import pandas
import numpy as np
import csv
import time

def csvToDF_largeFile(csvfile):
    csv_arr = []
    time_difference = []
    csvfile_f = open(csvfile)
    csv_reader = csv.reader(csvfile_f)
    isPrevGA = False
    j=1
    lines = 0
    isFirstPage = True

    for index, row in enumerate(csv_reader):
        if index == 0 and isFirstPage is True:
            csv_arr = csv_arr + [row]

        t1 = time.time()


        #if row[5] == 'Giveaway' or row[5] == 'Shot' or row[5] == 'Stoppage':
        if row[5] == 'Giveaway':
            lines += 1
            isPrevGA = True
        elif isPrevGA == True:
            isPrevGA = False
            csv_arr += [row]


        if j*100000 == index:

            csv_df = pandas.DataFrame(np.array(csv_arr), columns=csv_arr[0])
            if isFirstPage is True:
                csv_df = csv_df.drop(csv_df.index[0])
                isFirstPage = False

            #print(csv_df)

            csv_df.to_csv('play_after_GA.csv', index=False, sep=',', encoding='utf-8', mode='a')
            csv_arr = []
            j += 1
            time_difference = []
            t2 = time.time()
            print('Elapsed time: ', t2-t1, 'seconds.', ' --- ', 'Sections completed: ', j)


    return lines
