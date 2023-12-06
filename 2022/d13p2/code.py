import sys
import ast
import functools

CORRECT = 1
INCORRECT = -1
CONTINUE = 0

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

packets = []
with open(sys.argv[1],'r') as f:
    for line in f:
        if line.strip() == '':
            continue
        packets.append(parse_packet(line.strip()))

packets.append([[2]])
packets.append([[6]])

cmpfn = functools.cmp_to_key(compare_packets)

packets_sorted = sorted(packets, key = cmpfn, reverse=True)

index_2 = packets_sorted.index([[2]])
index_6 = packets_sorted.index([[6]])
decoder_key = (index_2+1) * (index_6+1)
print(decoder_key)
