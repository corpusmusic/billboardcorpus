"""
This file contains some ideas about how to start playing with the Billboard corpus.
We don't necessarily need to use it unless it proves useful.

To use:
    - Copy the directory "McGill-Billboard" (the downloaded salami files) into this directory
    - Run "python parse.py"

"""

import os
import re

from collections import defaultdict

ROOT_DIR = 'McGill-Billboard'

def corpus_iterator(root):
    """Iterate over the corpus directory and yield paths to the text files."""
    for sub_dir in os.listdir(root):
        dir_path = os.path.join(root, sub_dir)
        for f in os.listdir(dir_path):
            yield os.path.join(dir_path, f)

def get_chord_sequence(f):
    """Return a list of chord sequences from a given salami text file."""
    return re.findall(r'\S+:\S+', open(f).read())

def get_overall_counts():
    """
    Return dictionaries with individual chord counts and transition counts. If
    the same chord appears multiple times in a row, only the first is counted.

    """
    chord_counts = defaultdict(lambda: 0)
    transition_counts = defaultdict(lambda: 0)
    for f in corpus_iterator(ROOT_DIR):
        chords = get_chord_sequence(f)
        length = len(chords)
        for i in range(length-1):
            if chords[i] != chords[i+1]:
                transition = (chords[i], chords[i+1])
                transition_counts[transition] += 1
                chord_counts[chords[i]] += 1
        if chords[length-1] != chords[length-2]:
            chord_counts[chords[length-1]] += 1
    return chord_counts, transition_counts

if __name__ == '__main__':
    chord_counts, transition_counts = get_overall_counts()
    for k, v in chord_counts.items():
        print k, '\t', v

