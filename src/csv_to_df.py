import pandas
import numpy as np
import csv
import time
import os
import math
import sys


def csv_to_dataframe_and_ui(csvfile):
    upload_speed = lines = blocks = row_size = total_lines = lines_processed_last_time = 0;
    total_size_in_memory, row_size_in_memory = get_memory_size(csvfile)
    opened_csvfile = open(csvfile); csv_reader = csv.reader(opened_csvfile)
    csv_plays = []; initial_time = last_time = time.time(); print();

    for row in csv_reader:
        csv_plays = csv_plays + [row]; now = time.time(); lines += 1;
        upload_speed, last_time, lines_processed_last_time = getupload_speed(now, last_time, lines,
                                                                       lines_processed_last_time,
                                                                       row_size_in_memory,
                                                                       upload_speed)
        blocks = status_bar(lines, blocks, total_size_in_memory,
                           row_size_in_memory,
                           now-initial_time, upload_speed)
    finishing()
    opened_csvfile.close()

    return csv_plays

def clean_dataframe(csv_plays):
    return pandas.DataFrame(np.array(csv_plays), columns=csv_plays[0]).drop([0])

def get_memory_size(csvfile):
    total_row_size = row_size = 0
    csvfile_file_size = open(csvfile); csv_reader_size = csv.reader(csvfile_file_size)
    for index, row in enumerate(csv_reader_size):
        if index == 0:
            row_size = sys.getsizeof(row)
        total_row_size += sys.getsizeof(row)
    csvfile_file_size.close()

    return total_row_size, row_size

def getupload_speed(now, last_time, lines, lines_processed_last_time, row_size, bytes_processed):
    if now - last_time >= 1:
        bytes_processed = (lines - lines_processed_last_time) * row_size
        last_time = now
        lines_processed_last_time = lines;
    return bytes_processed, last_time, lines_processed_last_time

def check_and_make_img_folder(jointplot=False):
    if jointplot:
        if not os.path.isdir('../img'):
            os.makedirs('../img/joinplots')
        else:
            if not os.path.isdir('../img/joinplots'):
                os.makedirs('../img/joinplots')
    else:
        if not os.path.isdir('../img'):
            os.mkdir('../img')

def display_bytes(bytes):
    if bytes < 1000:
        return ('{0:.' + str(2)+ 'f}').format(bytes) + 'B'
    elif bytes >= 1000 and bytes < 1000000:
        return ('{0:.' + str(2)+ 'f}').format(bytes/1000) + 'KB'
    elif bytes > 1000000:
        return ('{0:.' + str(2)+ 'f}').format(bytes/1000000) + 'MB'

def finish_dot(number_of_dots):
    if not number_of_dots:
        return
    print('.', end='', flush=True)
    time.sleep(0.5)
    finish_dot(number_of_dots-1)

    return

def finishing():
    print('\n\n Finishing', end='', flush=True)
    time.sleep(0.5)
    finish_dot(3)
    print('\n', flush=True)

def get_hour_glass(phase):
    hour_glasses = ['[/]', '[-]', '[\]', '[|]', '[/]', '[-]', '[\]', '[|]']

    return hour_glasses[phase]

def get_ui_percent(lines, row_size, file_size):
    return ('{0:.' + str(1) + 'f}').format(100 * float(lines * row_size) / file_size)

def get_ui_bar(blocks, block, unfilled):
    return blocks * block + unfilled * '-'

def get_ui_file_size_fraction(lines, row_size, file_size):
    return '[' + display_bytes(lines*row_size) + '/' + display_bytes(file_size) + ']'

def get_ui_hour_glass(duration):
    return get_hour_glass(math.floor((duration - math.floor(duration)) / 0.125))

def get_blocks(lines, row_size, blocks, block_size):
    if (lines * row_size >= blocks * block_size):
        blocks += 1
    return blocks

def print_ui(percent, bar, file_size_fraction, hour_glass, bytes_per_second,
            prefix=' Importing csv... ', suffix='Complete', block='\u2588', unfilled=25):

    print('\r%s |%s| %s%% %s %s %s %s %s' % (prefix, bar, percent, suffix,
                                             file_size_fraction,
                                             display_bytes(bytes_per_second) + '/s',
                                             hour_glass, '   '),
                                             end='\r')

def compose_ui(lines, row_size, file_size, blocks, block, unfilled, duration, bytes_per_second):
    print_ui(get_ui_percent(lines, row_size, file_size), get_ui_bar(blocks, block, unfilled),
          get_ui_file_size_fraction(lines, row_size, file_size), get_ui_hour_glass(duration),
          bytes_per_second)

def status_bar(lines, blocks, file_size, row_size, duration, bytes_per_second,
               prefix=' Importing csv... ', suffix='Complete', block='\u2588',
               unfilled=25):
    block_size = file_size / 25
    unfilled = 25 - blocks

    compose_ui(lines, row_size, file_size, blocks, block, unfilled, duration, bytes_per_second)

    return get_blocks(lines, row_size, blocks, block_size)

def csv_to_df(csvfile):
    try:
        return clean_dataframe(csv_to_dataframe_and_ui(csvfile))

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
