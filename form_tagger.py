"""
This file attempts to run the Viterbi alogithm, using form information as the hidden
states, and chord and position in phrase information as the observations.

"""

from __future__ import division

from collections import defaultdict
from operator import itemgetter
from readdata import read_data

def get_probabilities(chord_list):
    """
    Return all parameters needed for viterbi.

    Returns:
        transition_probs: the probability of one hidden state going to another for all hidden states
        emission_probs: the probability of seeing an observed state given the hidden state
        initial_probs: the initial probability of starting in a given hidden state
        states: a tuple containing all the hidden states in the data

    """
    emission_counts = defaultdict(lambda: 0)
    module_counts = defaultdict(lambda: 0)
    transition_counts = defaultdict(lambda: 0)
    initial_counts = defaultdict(lambda: 0)
    for chords in chord_list:
        for i in range(len(chords)):
            if i == 0:
                initial_counts[chords[i]['module']] += 1
            else:
                transition = (chords[i-1]['module'], chords[i]['module'])
                transition_counts[transition] += 1

            emission = (chords[i]['module'], '_'.join([chords[i]['root'], chords[i]['bar_of_phrase']]))
            emission_counts[emission] += 1
            module_counts[chords[i]['module']] += 1

    states = tuple(module_counts.keys())
    num_states = len(states)

    transition_probs = {}
    emission_probs = {}
    for (first, second), count in transition_counts.items():
        probability = (transition_counts[(first, second)] + 1) / (module_counts[first] + num_states)
        transition_probs[(first, second)] = probability

    for module, root in emission_counts.keys():
        probability = emission_counts[(module, root)] / module_counts[module]
        emission_probs[(module, root)] = probability

    num_initial_states = sum(x for x in initial_counts.values())
    initial_probs = {k: v / num_initial_states for k, v in initial_counts.items()}
    for s in states:
        if s not in initial_probs:
            initial_probs[s] = 0.0001

    return transition_probs, emission_probs, initial_probs, states

# copied from wikipedia
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p.get((y, obs[0]), 0.0001)
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p.get((y0, y), 0.0001) * emit_p.get((y, obs[t]), 0.0001), y0) for y0 in states)
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
    datafile = 'example1.csv'
    # datafile = 'AlldataWithNonHarmonics.csv'
    headers = ['module', 'root', 'bar_of_phrase', 'letter']
    data = read_data(datafile, headers)
    transition_probs, emission_probs, initial_probs, states = get_probabilities(data)

    print states
    # for one, two in emission_probs:
    #     print '{}->{}: {:.4f}'.format(one, two, emission_probs[(one, two)])

    # for state in initial_probs:
    #     print state, initial_probs[state]

    # for song in data:
    #     obs = [entry['module'] for entry in song]
    #     print viterbi(obs, states, initial_probs, transition_probs, emission_probs)
    #     print # newline
