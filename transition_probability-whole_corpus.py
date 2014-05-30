from __future__ import division

from collections import defaultdict
from operator import itemgetter
from readdata import read_data
import sys

RN = ['I', 'bII', 'II', 'bIII', 'III', 'IV', 'bV', 'V', 'bVI', 'VI', 'bVII', 'VII', 'NonHarmonic']

def get_overall_counts(chord_lists):
    """Return dictionaries with individual chord counts and transition counts."""
    chord_counts = defaultdict(lambda: 0)
    transition_counts = defaultdict(lambda: 0)
    for chords in chord_lists:
        length = len(chords)
        for i in range(length-1):
            transition = (chords[i]['root'], chords[i+1]['root'])
            transition_counts[transition] += 1
            chord_counts[chords[i]['root']] += 1
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
    try:
        datafile = sys.argv[1]
    except:
        datafile = 'AlldataWithNonHarmonics.csv'

    headers = ['root']
    data = read_data(datafile, headers)
    chord_counts, transition_counts = get_overall_counts(data)
    transition_probs = get_transition_probs(chord_counts, transition_counts)

    # map roman numerals to integers for sorting, and covert back to display
    transitions = [(RN.index(c1), c2) for c1, c2 in transition_probs]
    for c1, c2 in sorted(transitions):
        print '({} -> {}): {:.4f}'.format(RN[c1], c2, transition_probs[(RN[c1], c2)])
