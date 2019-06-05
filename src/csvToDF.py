import pandas
import numpy as np
import csv
import time
import os
import math
import sys


def csvToDataframeAndUi(csvfile):
    uploadSpeed = lines = blocks = rowSize = totalLines = linesProcessedLastTime = 0;
    totalSizeInMemory, rowSizeInMemory = getMemorySize(csvfile)
    csvfileFile = open(csvfile); csvReader = csv.reader(csvfileFile)
    csvArr = []; initialTime = lastTime = time.time(); print();

    for row in csvReader:
        csvArr = csvArr + [row]; now = time.time(); lines += 1;
        uploadSpeed, lastTime, linesProcessedLastTime = getUploadSpeed(now, lastTime, lines,
                                                                       linesProcessedLastTime,
                                                                       rowSizeInMemory,
                                                                       uploadSpeed)
        blocks = statusBar(lines, blocks, totalSizeInMemory,
                           rowSizeInMemory,
                           now-initialTime, uploadSpeed)
    finishing()
    csvfileFile.close()

    return csvArr

def cleanDataFrame(csvArr):
    return pandas.DataFrame(np.array(csvArr), columns=csvArr[0]).drop([0])

def getMemorySize(csvfile):
    totalRowSize=0; rowSize=0
    csvfileFileSize = open(csvfile); csvReaderSize = csv.reader(csvfileFileSize)
    for index, row in enumerate(csvReaderSize):
        if index == 0:
            rowSize = sys.getsizeof(row)
        totalRowSize += sys.getsizeof(row)
    csvfileFileSize.close()

    return totalRowSize, rowSize

def getUploadSpeed(now, lastTime, lines, linesProcessedLastTime, rowSize, bytesProcessed):
    if now - lastTime >= 1:
        bytesProcessed = (lines - linesProcessedLastTime) * rowSize
        lastTime = now
        linesProcessedLastTime = lines;
    return bytesProcessed, lastTime, linesProcessedLastTime

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

def getUiPercent(lines, rowSize, fileSize):
    return ('{0:.' + str(1) + 'f}').format(100 * float(lines * rowSize) / fileSize)

def getUiBar(blocks, block, unFilled):
    return blocks * block + unFilled * '-'

def getUiFileSizeFraction(lines, rowSize, fileSize):
    return '[' + displayBytes(lines*rowSize) + '/' + displayBytes(fileSize) + ']'

def getUihourGlass(duration):
    return getHourGlass(math.floor((duration - math.floor(duration)) / 0.125))

def getBlocks(lines, rowSize, blocks, blockSize):
    if (lines * rowSize >= blocks * blockSize):
        blocks += 1
    return blocks

def printUi(percent, bar, fileSizeFraction, hourGlass, bytesPerSecond,
            prefix=' Importing csv... ', suffix='Complete', block='\u2588', unFilled=25):

    print('\r%s |%s| %s%% %s %s %s %s %s' % (prefix, bar, percent, suffix,
                                             fileSizeFraction,
                                             displayBytes(bytesPerSecond) + '/s',
                                             hourGlass, '   '),
                                             end='\r')

def composeUi(lines, rowSize, fileSize, blocks, block, unFilled, duration, bytesPerSecond):
    printUi(getUiPercent(lines, rowSize, fileSize), getUiBar(blocks, block, unFilled),
          getUiFileSizeFraction(lines, rowSize, fileSize), getUihourGlass(duration),
          bytesPerSecond)

def statusBar(lines, blocks, fileSize, rowSize, duration, bytesPerSecond, prefix=' Importing csv... ', suffix='Complete', block='\u2588', unFilled=25):
    blockSize = fileSize / 25
    unFilled = 25 - blocks

    composeUi(lines, rowSize, fileSize, blocks, block, unFilled, duration, bytesPerSecond)

    return getBlocks(lines, rowSize, blocks, blockSize)

def csvToDF(csvfile):
    try:
        return cleanDataFrame(csvToDataframeAndUi(csvfile))

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
