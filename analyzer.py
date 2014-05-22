from __future__ import division

from collections import defaultdict
from operator import itemgetter
import csv

def read_data(filename):
    """
    Return a list of lists where the inner lists are the chords for a song and
    and the outer list is a list of songs. The specific data captured for each song
    will change as the parser gets written.

    """
    corpus_list = []
    song_list = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if len(row) > 0:
                chord, root = row
                song_list.append(root)

            # line break means start the next song
            else:
                corpus_list.append(song_list)
                song_list = []
    return corpus_list

def get_overall_counts(chord_lists):
    """
    Return dictionaries with individual chord counts and transition counts. If
    the same chord appears multiple times in a row, only the first is counted.

    """
    chord_counts = defaultdict(lambda: 0)
    transition_counts = defaultdict(lambda: 0)
    for chords in chord_lists:
        length = len(chords)
        for i in range(length-1):
            if chords[i] != chords[i+1]:
                transition = (chords[i], chords[i+1])
                transition_counts[transition] += 1
                chord_counts[chords[i]] += 1
        if chords[length-1] != chords[length-2]:
            chord_counts[chords[length-1]] += 1
    return chord_counts, transition_counts

def get_transition_probs(chord_counts, transition_counts):
    """
    Returns a dictionary of transition probabilities based on counts for chords
    and transitions.

    """
    probs = dict(transition_counts) # make a copy so we don't destroy the counts dictionary
    for (first, second), count in transition_counts.items():
        probability = transition_counts[(first, second)] / chord_counts[first]
        probs[(first, second)] = probability
    return probs

if __name__ == '__main__':
    roots = read_data('example.csv')
    chord_counts, transition_counts = get_overall_counts(roots)
    transition_probs = get_transition_probs(chord_counts, transition_counts)

    for transition, prob in sorted(transition_probs.items(), key=itemgetter(1), reverse=True):
        print transition, '\t', prob
