import sys

selection_scores = {
        'R': 1,
        'P': 2,
        'S': 3,
        }

battle_scores = {
        'R': {'A': 3, 'B': 0, 'C': 6},
        'P': {'A': 6, 'B': 3, 'C': 0},
        'S': {'A': 0, 'B': 6, 'C': 3},
        }


get_throw = {
        'A': {'X': 'S', 'Y': 'R', 'Z': 'P'},
        'B': {'X': 'R', 'Y': 'P', 'Z': 'S'},
        'C': {'X': 'P', 'Y': 'S', 'Z': 'R'}
        }

def calc_score(him, strat):
    me = get_throw[him][strat]
    return selection_scores[me] + battle_scores[me][him]

running_score = 0
with open(sys.argv[1],'r') as f:
    for l in f:
        him, strat = l.strip().split()
        running_score += calc_score(him, strat)

print(running_score)
