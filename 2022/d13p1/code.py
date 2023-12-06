import sys
import ast

CORRECT = 1
INCORRECT = 0
CONTINUE = -1

def parse_packet(p):
    return ast.literal_eval(p)

def compare_packets(p, q):
    if isinstance(p, int) and isinstance(q, int):
        if p < q:
            return CORRECT
        elif p > q:
            return INCORRECT
        else:
            return CONTINUE
    if isinstance(p, int) and not isinstance(q, int):
        p = [p]
    if isinstance(q, int) and not isinstance(p, int):
        q = [q]

    for i in range(len(q)):
        try:
            elp = p[i]
            elq = q[i]
        except IndexError:
            return CORRECT

        comp = compare_packets(elp, elq)
        if comp != CONTINUE:
            return comp
    if len(p) > len(q):
        return INCORRECT

    return CONTINUE

pairs = []
with open(sys.argv[1],'r') as f:
    for line in f:
        left = parse_packet(line.strip())
        right = parse_packet(f.readline().strip())
        pairs.append((left, right))
        f.readline()

rsum = sum([i+1 for i, (l,r) in enumerate(pairs) if compare_packets(l,r)])
print(rsum)

#for i, (l,r) in enumerate(pairs):
#    print(i+1, l, r)
#    print(i+1, compare_packets(l, r))
