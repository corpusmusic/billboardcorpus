from __future__ import division

from collections import defaultdict
from operator import itemgetter
from readdata import read_data

def get_probabilities(chord_list):
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

            emission = (chords[i]['module'], chords[i]['root'])
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

    return transition_probs, emission_probs, initial_probs, states

# copied from wikipedia
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max((V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states)
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
    datafile = '15SimpleSongs.csv'
    headers = ['module', 'root']
    data = read_data(datafile, headers)
    transition_probs, emission_probs, initial_probs, states = get_probabilities(data)
    print states
