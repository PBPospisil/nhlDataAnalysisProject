import pandas
import numpy as np
import csv
import time

def csvToDF(csvfile):
    lines=0
    csvArr = []
    csvfileF = open(csvfile)
    csvReader = csv.reader(csvfileF)

    for row in csvReader:
        csvArr = csvArr + [row]
        lines += 1
        if lines%10000 == 0:
            print('processed ', lines, 'lines.')

    csvDF = pandas.DataFrame(np.array(csvArr), columns=csvArr[0]).drop([0])

    return csvDF
