import pandas
import numpy as np
import csv
import time
import os
import math
import sys


def getMemorySize(mode=total):
    totalRowSize=0; rowSize=0
    csvfileFileSize = open(csvfile); csvReaderSize = csv.reader(csvfileFileSize)
    for index, row in enumerate(csvReaderSize):
        if index == 0:
            rowSize = sys.getsizeof(row)
        totalRowSize += sys.getsizeof(row)
    csvfileFileSize.close()

    if mode == 'row':
        return rowSize
    else:
        return totalRowSize

def checkAndMakeImgFolder(heatmap=False):
    if heatmap:
        if not os.path.isdir('../img'):
            os.makedirs('../img/heatmaps')
        else:
            if not os.path.isdir('../img/heatmaps'):
                os.makedirs('../img/heatmaps')
    else:
        if not os.path.isdir('../img'):
            os.mkdir('../img')

def displayBytes(bytes):
    if bytes < 1000:
        return ('{0:.' + str(2)+ 'f}').format(bytes) + 'B'
    elif bytes >= 1000 and bytes < 1000000:
        return ('{0:.' + str(2)+ 'f}').format(bytes/1000) + 'KB'
    elif bytes > 1000000:
        return ('{0:.' + str(2)+ 'f}').format(bytes/1000000) + 'MB'

def finishDot(numberOfDots):
    if not numberOfDots:
        return
    print('.', end='', flush=True)
    time.sleep(0.5)
    finishDot(numberOfDots-1)

    return

def finishing():
    print('\n\n Finishing', end='', flush=True)
    time.sleep(0.5)
    finishDot(3)
    print('\n', flush=True)

def getHourGlass(phase):
    hourGlasses = ['[/]', '[-]', '[\]', '[|]', '[/]', '[-]', '[\]', '[|]']

    return hourGlasses[phase]

def statusBar(lines, blocks, fileSize, rowSize, duration, bytesPerSecond, prefix=' Importing csv... ', suffix='Complete', block='\u2588', unFilled=50):
    blockSize = fileSize / 25
    unFilled = 25 - blocks

    percent = ('{0:.' + str(1) + 'f}').format(100 * float(lines * rowSize) / fileSize)
    bar = blocks * block + unFilled * '-'
    fileSizeFraction = '[' + displayBytes(lines*rowSize) + '/' + displayBytes(fileSize) + ']'
    hourGlass = getHourGlass(math.floor((duration - math.floor(duration)) / 0.125))

    print('\r%s |%s| %s%% %s %s %s %s %s' % (prefix, bar, percent, suffix, fileSizeFraction, displayBytes(bytesPerSecond) + '/s', hourGlass, '   '), end='\r')

    if (lines * rowSize >= blocks * blockSize):
        blocks += 1

    return blocks

def csvToDF(csvfile):
    lines=0; blocks=0; rowSize = 0; totalLines=0
    csvArr = []

    try:
        csvfileFile = open(csvfile)
        csvReader = csv.reader(csvfileFile)
        linesProcessedLastTime = 0
        t1 = time.time()
        lastTime = time.time()
        bytesProcessed = 0
        print()

        for row in csvReader:
            if rowSize == 0:
                rowSize = sys.getsizeof(row)
            csvArr = csvArr + [row]
            lines += 1
            t2 = time.time()
            if t2 - lastTime >= 1:
                bytesProcessed = (lines - linesProcessedLastTime) * rowSize
                linesProcessedLastTime = lines
                lastTime = t2

            blocks = statusBar(lines, blocks, getMemorySize(), rowSize, t2-t1, bytesProcessed)

        finishing()
        csvDF = pandas.DataFrame(np.array(csvArr), columns=csvArr[0]).drop([0])

        return csvDF

    except IOError:
        print('An error occured trying to read this file: ' + csvfile)

    except ValueError:
        print('Non-numeric data found in file.')

    except ImportError:
        print('No module found')

    except EOFError:
        print('EOFError')

    except KeyboardInterrupt:
        print('You cancelled the operation.')

    except AttributeError:
        print('Incorrect attribute for object, likely `NoneType` object.')

    except:
        print('An error occured.')

    return
