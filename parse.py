"""
This file contains some ideas about how to start playing with the Billboard corpus.
We don't necessarily need to use it unless it proves useful.

To use:
    - Copy the directory "McGill-Billboard" (the downloaded salami files) into this directory
    - Run "python parse.py"

"""

import os
import re

from collections import defaultdict, deque

ROOT_DIR = 'McGill-Billboard'

KEYS = [{'A'}, {'A#', 'Bb'}, {'B', 'Cb'}, {'C'}, {'C#', 'Db'}, {'D'}, {'D#', 'Eb'}, {'E', 'Fb'}, {'F'}, {'F#', 'Gb'}, {'G'}, {'G#', 'Ab'}]

def lookup_chord(key, key_list):
    """Look up the numerical position of a chord root relative to an ordered list of roots (possibly shifted)."""
    for i, k in enumerate(key_list):
        if key in k:
            return i

def corpus_list(root):
    """Return a list of all paths to the salami text files, relative to the root directory of the project."""
    return [os.path.join(* [root, sub_dir, 'salami_chords.txt']) for sub_dir in os.listdir(root)]

def get_chord_sequence(f):
    """
    Return a list of chord sequences from a given salami text file, and the tonic.

    TODO:
    - Need verification that it is muscially sound to parse this way.
    - Also want to do more in depth parsing to capture more info from the text file

    """
    fs = open(f)
    line = fs.readline()
    while 'tonic' not in line:
        line = fs.readline()
    tonic = line[line.index(':') + 2:-1]
    return tonic, re.findall(r'\S+:\S+', fs.read())

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

def get_relative(tonic, chords):
    """
    Return a list of the relative root numbers based on the tonic note and
    a list of absolute chords. Returns integers, where 0 -> I, 1 -> II, etc.

    TODO: needs testing and verification that it is working properly

    """
    root_num = lookup_chord(tonic, KEYS)
    shifted_keys = deque(KEYS)
    shifted_keys.rotate(-root_num)
    relative_chords = []
    for c in chords:
        root, quality = c.split(':')
        relative_chords.append(lookup_chord(root, shifted_keys))
    return relative_chords

if __name__ == '__main__':
    filenames = corpus_list(ROOT_DIR)
    relative_chords = []
    for f in filenames:
        tonic, chords = get_chord_sequence(f)
        relative_chords.append(get_relative(tonic, chords))

    chord_counts, transition_counts = get_overall_counts(relative_chords)
    for k, v in chord_counts.items():
        print k, '\t', v
