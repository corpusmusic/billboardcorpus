"""
This file contains a method that grabs the data from the csv. Because it will
be used in all the analysis files, it is separated out here.

"""

import csv

CSV_COLUMNS = ['module', 'letter', 'full', 'root', 'quality', 'bar_of_phrase', 'bpm']

def read_data(filename, col_names):
    """
    Return a list of usable data.

    Args:
        filename: the name of the csv to read the data from. This is the output from the parser code.
        col_names: a list that is a subset of the CSV_COLUMNS list, indicating which columns to select.

    """
    corpus_list = []
    song_list = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) > 0:
                entry = {k: v for k, v in zip(CSV_COLUMNS, row) if k in col_names}
                song_list.append(entry)

            # line break means start the next song
            else:
                corpus_list.append(song_list)
                song_list = []

    return corpus_list
