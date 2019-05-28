import pandas
import numpy as np
import csv
import time

def csvToDF(csvfile):
    lines=0
    csv_arr = []
    csvfile_f = open(csvfile)
    csv_reader = csv.reader(csvfile_f)

    for row in csv_reader:
        csv_arr = csv_arr + [row]
        lines += 1
        if lines%10000 == 0:
            print('processed ', lines, 'lines.')

    csv_df = pandas.DataFrame(np.array(csv_arr), columns=csv_arr[0]).drop([0])

    return csv_df
