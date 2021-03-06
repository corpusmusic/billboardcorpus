"""
This file attempts to run the Viterbi alogithm, using form information as the hidden
states, and chord and position in phrase information as the observations.

"""

from __future__ import division

from collections import defaultdict
from operator import itemgetter
from readdata import read_data
import sys

SMOOTHER = 0.0001

def get_probabilities(chord_list):
    """
    Return all parameters needed for viterbi.

    Returns:
        transition_probs: the probability of one hidden state going to another for all hidden states
        emission_probs: the probability of seeing an observed state given the hidden state
        initial_probs: the initial probability of starting in a given hidden state
        states: a tuple containing all the hidden states in the data

    """
    def get_hidden_state(i):
        return chords[i]['module']
        # return '_'.join([chords[i]['module'], chords[i]['bar_of_phrase']])
        # return '_'.join([chords[i]['module'], chords[i]['bar_of_phrase'], chords[i]['bars_per_phrase']])

    def get_observed_state(i):
        # return '_'.join([chords[i]['root'], chords[i]['bar_of_phrase']])
        return chords[i]['root']

    emission_counts = defaultdict(lambda: 0)
    module_counts = defaultdict(lambda: 0)
    transition_counts = defaultdict(lambda: 0)
    initial_counts = defaultdict(lambda: 0)
    for chords in chord_list:
        for i in range(len(chords)):

            # skip instrumental songs
            if 'Frankenstein' in chords[i]['song_name'] or 'ThemeFromElectricSurfboard' in chords[i]['song_name']:
                break

            if i == 0:
                initial_counts[get_hidden_state(i)] += 1
            else:
                transition = (get_hidden_state(i-1), get_hidden_state(i))
                transition_counts[transition] += 1

            emission = (get_hidden_state(i), get_observed_state(i))
            emission_counts[emission] += 1
            module_counts[get_hidden_state(i)] += 1

    states = tuple(module_counts.keys())
    num_states = len(states)

    transition_probs = {}
    emission_probs = {}
    for (first, second), count in transition_counts.items():
        probability = (transition_counts[(first, second)] + 1) / (module_counts[first] + num_states)
        transition_probs[(first, second)] = probability

    for hidden, observed in emission_counts.keys():
        probability = emission_counts[(hidden, observed)] / module_counts[hidden]
        emission_probs[(hidden, observed)] = probability

    num_initial_states = sum(x for x in initial_counts.values())
    initial_probs = {k: v / num_initial_states for k, v in initial_counts.items()}
    for s in states:
        if s not in initial_probs:
            initial_probs[s] = SMOOTHER

    return transition_probs, emission_probs, initial_probs, states

# copied from wikipedia
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p.get((y, obs[0]), SMOOTHER)
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p.get((y0, y), SMOOTHER) * emit_p.get((y, obs[t]), SMOOTHER), y0) for y0 in states)
            V[t][y] = prob
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath
    n = 0           # if only one element is observed max is sought in the initialization values
    if len(obs)!=1:
        n = t
    (prob, state) = max((V[n][y], y) for y in states)
    return (prob, path[state])

if __name__ == '__main__':
    try:
        datafile = sys.argv[1]
    except:
        datafile = 'AllDataWithNonHarmonics.csv'

    headers = ['module', 'root', 'bar_of_phrase', 'letter', 'bars_per_phrase', 'song_name']
    data = read_data(datafile, headers)
    transition_probs, emission_probs, initial_probs, states = get_probabilities(data)

    # print states
    # for one, two in emission_probs:
    #     print '{}->{}: {:.4f}'.format(one, two, emission_probs[(one, two)])

    # for state in initial_probs:
    #     print state, initial_probs[state]

    total_correct = 0
    total = 0
    for song in data:
        obs = [entry['root'] for entry in song]
        correct = [entry['module'].split('_')[0] for entry in song]
        prob, predictions = viterbi(obs, states, initial_probs, transition_probs, emission_probs)
        predictions = [pred.split('_')[0] for pred in predictions]
        num_correct = sum(1 for pred, cor in zip(predictions, correct) if pred == cor)
        total += len(predictions)
        total_correct += num_correct

    print 'accuracy:', total_correct / total

