from __future__ import division

from collections import defaultdict
from operator import itemgetter
from readdata import read_data
import csv
import sys

RN = ['I', 'bII', 'II', 'bIII', 'III', 'IV', 'bV', 'V', 'bVI', 'VI', 'bVII', 'VII', 'NonHarmonic']

for j in range(0,4):
    z = ['4','4','4','4']
    t = ['1','2','3','4']

    def transition_probs_by_song(chord_lists):
        """
        Return a dictionary where the keys are song names, and the values are
        dictionaries with transitional probabilities.

        """
        chord_counts = defaultdict(lambda: 0)
        transition_counts = defaultdict(lambda: 0)
        song_transition_probs = {}
        total_counts = 0

        # for every song in the corpus, 'chords' will be a list of the chords
        for chords in chord_lists:
            length = len(chords)

            # for every chord in the list of chords, count all the transitions and root occurances
            for i in range(length-1):
                if((chords[i]['bars_per_phrase'] == z[j]) and (chords[i]['bar_of_phrase'] == t[j])):
                    transition = (chords[i]['root'])
                    transition_counts[transition] += 1
                    chord_counts[chords[i]['root']] += 1
                    total_counts += 1

            # add the transition probabilities for this song into a giant dictionary
            song_transition_probs[chords[i]['song_name']] = get_transition_probs(total_counts, transition_counts)

            # reset the count dictionaries for the next song
            chord_counts = defaultdict(lambda: 0)
            transition_counts = defaultdict(lambda: 0)
            total_counts = 0

        return song_transition_probs

    def get_transition_probs(total_counts, transition_counts):
        """
        Returns a dictionary of transition probabilities based on counts for chords
        and transitions.

        """
        probs = {}

        # go through all 144 possible transitions
        for first in RN:

             # use try catch to avoid divide by 0 errors or key errors
            try:
                probability = transition_counts[(first)] / total_counts
                probs[(first)] = probability

                # if a transition isn't found in the data, give it probability 0
            except:
                probs[(first)] = 0
        return probs

    def write_csv(probabilities):
        with open('output0th%.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for song_name, probs in transition_probs.items():

                # get all probabilities in sorted order, and get rid of non-harmonic transitions
                transitions = [(RN.index(c1)) for c1 in probs if c1 != 'NonHarmonic']
                line = [probs[(RN[c1])] for c1 in sorted(transitions)]

                # uncomment the following line to add the song name as the first value in the csv
                line = [song_name] + line

                # write to csv
                writer.writerow(line)

    if __name__ == '__main__':
        try:
            datafile = sys.argv[1]
        except:
            datafile = 'AlldataWithNonHarmonics.csv'

        data = read_data(datafile)
        transition_probs = transition_probs_by_song(data)

        write_csv(transition_probs)

        for song_name, probs in transition_probs.items():
            print song_name + '\n' + ('-' * len(song_name)) + 'Bar Phrase ' + t[j] + ' of ' + z[j]

            # map roman numerals to integers for sorting, and covert back to display
            # this isn't actually necessary, just makes printing the results look nicer
            transitions = [(RN.index(c1)) for c1 in probs]
            for c1 in sorted(transitions):
                probability = probs[(RN[c1])]
                if probability != 0:
                    print '({} ->): {:.4f}'.format(RN[c1], probability)
            print #newline
