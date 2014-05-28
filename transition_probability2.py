from __future__ import division

from collections import defaultdict
from operator import itemgetter
from readdata import read_data

RN = ['I', 'bII', 'II', 'bIII', 'III', 'IV', 'bV', 'V', 'bVI', 'VI', 'bVII', 'VII', 'NonHarmonic']

def get_overall_counts(chord_lists):
    """Return dictionaries with individual chord counts and transition counts."""
    chord_counts = defaultdict(lambda: 0)
    transition_counts = defaultdict(lambda: 0)
    song_counts = defaultdict(lambda: 0)
    j = 0
    for chords in chord_lists:
        length = len(chords)
        for i in range(length-1):
            transition = (chords[i]['root'], chords[i+1]['root'])
            song_transition = (transition, chords[i]['song_name'])
            print song_transition
            song_counts[song_transition] += 1
            transition_counts[transition] += 1
            chord_counts[chords[i]['root']] += 1
            if i == (length - 1):
                j += length
    return chord_counts, transition_counts, song_counts

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
    datafile = 'AlldataWithNonHarmonicsV2.csv'
    data = read_data(datafile)
    chord_counts, transition_counts, song_counts = get_overall_counts(data)
    transition_probs = get_transition_probs(chord_counts, transition_counts)

    # map roman numerals to integers for sorting, and covert back to display
    transitions = [(RN.index(c1), c2) for c1, c2 in transition_probs]
    for c1, c2 in sorted(transitions):
        print '({} -> {}): {:.4f}'.format(RN[c1], c2, transition_probs[(RN[c1], c2)])
