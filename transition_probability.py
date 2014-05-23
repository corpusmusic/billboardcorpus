from __future__ import division

from collections import defaultdict
from operator import itemgetter
from readdata import read_data

def get_overall_counts(chords):
    """
    Return dictionaries with individual chord counts and transition counts. If
    the same chord appears multiple times in a row, only the first is counted.

    """
    chord_counts = defaultdict(lambda: 0)
    transition_counts = defaultdict(lambda: 0)
    length = len(chords)
    for i in range(length-1):
        transition = (chords[i], chords[i+1])
        transition_counts[transition] += 1
        chord_counts[chords[i]] += 1
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
    datafile = '15SimpleSongs.csv'
    headers = ['root']
    roots = [entry['root'] for entry in read_data(datafile, headers, False)]
    chord_counts, transition_counts = get_overall_counts(roots)
    transition_probs = get_transition_probs(chord_counts, transition_counts)

    for transition, prob in sorted(transition_probs.items(), key=itemgetter(1), reverse=True):
        print transition, '\t', prob
