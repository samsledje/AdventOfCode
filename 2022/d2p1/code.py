import sys

selection_scores = {
        'X': 1,
        'Y': 2,
        'Z': 3,
        }

battle_scores = {
        'X': {'A': 3, 'B': 0, 'C': 6},
        'Y': {'A': 6, 'B': 3, 'C': 0},
        'Z': {'A': 0, 'B': 6, 'C': 3},
        }


def calc_score(me, him):
    return selection_scores[me] + battle_scores[me][him]

running_score = 0
with open(sys.argv[1],'r') as f:
    for l in f:
        him, me = l.strip().split()
        running_score += calc_score(me, him)

print(running_score)
