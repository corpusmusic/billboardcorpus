from __future__ import division

from collections import defaultdict
from operator import itemgetter
from readdata import read_data

RN = ['I', 'bII', 'II', 'bIII', 'III', 'IV', 'bV', 'V', 'bVI', 'VI', 'bVII', 'VII', 'NonHarmonic']

def transition_probs_by_song(chord_lists):
    """Return dictionaries with individual chord counts and transition counts."""
    chord_counts = defaultdict(lambda: 0)
    transition_counts = defaultdict(lambda: 0)
    song_transition_probs = {}

    # for every song in the corpus, 'chords' will be a list of the chords
    for chords in chord_lists:
        length = len(chords)

        # for every chord in the list of chords
        for i in range(length-1):
            transition = (chords[i]['root'], chords[i+1]['root'])
            transition_counts[transition] += 1
            chord_counts[chords[i]['root']] += 1

        song_transition_probs[chords[i]['song_name']] = get_transition_probs(chord_counts, transition_counts)

        # reset the count dictionaries for the next song
        chord_counts = defaultdict(lambda: 0)
        transition_counts = defaultdict(lambda: 0)

    return song_transition_probs

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
    datafile = 'AlldataWithNonHarmonicsV5.csv'
    data = read_data(datafile)
    transition_probs = transition_probs_by_song(data)

    for song_name, probs in transition_probs.items():
        print song_name + '\n' + ('-' * len(song_name))

        # map roman numerals to integers for sorting, and covert back to display
        transitions = [(RN.index(c1), c2) for c1, c2 in probs]
        for c1, c2 in sorted(transitions):
            print '({} -> {}): {:.4f}'.format(RN[c1], c2, probs[(RN[c1], c2)])
        print #newline
