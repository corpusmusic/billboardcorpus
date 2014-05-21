from __future__ import division

from collections import defaultdict

ROOT_DIR = 'TODO'
CSV_NAME = 'TODO'

def read_data():
    """Return a list of all paths to the parsed csv files, relative to the root directory of the project."""
    return [os.path.join(* [ROOT_DIR, sub_dir, CSV_NAME]) for sub_dir in os.listdir(ROOT_DIR)]

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
    for f in read_data():
        pass
