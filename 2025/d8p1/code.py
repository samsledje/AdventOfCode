import sys
import numpy as np
from scipy.spatial.distance import pdist, squareform


def unravel(idx, num_items):
    x = idx // num_items
    y = idx % num_items
    return (x, y)


if __name__ == "__main__":
    box_coords = []
    circuits = []
    boxes_assigned = {}

    NUM_CONNECTIONS = 1000

    with open(sys.argv[1], "r") as f:
        for line in f:
            box_coords.append([int(i) for i in line.strip().split(",")])

    box_coords = np.array(box_coords)
    N_boxes = box_coords.shape[0]

    distances = pdist(box_coords)
    distances_sq = squareform(distances)

    upper = np.triu(distances_sq, 1)
    idx = np.argsort(upper, axis=None)
    row, col = np.unravel_index(idx, upper.shape)
    num_zero = int((N_boxes * (N_boxes - 1)) / 2) + N_boxes
    ordered_pairs = np.vstack([row, col]).T[num_zero:, :]
    ordered_pairs = ordered_pairs[: NUM_CONNECTIONS + 1, :]

    for i, (p0, p1) in enumerate(ordered_pairs):
        p0, p1 = int(p0), int(p1)
        print(
            f"[{i}] Pair {p0}, {p1} joins {box_coords[p0]} with {box_coords[p1]} (distance {distances_sq[p0, p1]})"
        )
        if (p0 in boxes_assigned) and (p1 in boxes_assigned):
            p0_circuit = boxes_assigned[p0]
            p1_circuit = boxes_assigned[p1]
            joint_circuit = p0_circuit.union(p1_circuit)
            for i_ in joint_circuit:
                boxes_assigned[i_] = joint_circuit
        elif p0 in boxes_assigned:
            existing_circuit = boxes_assigned[p0]
            existing_circuit.add(p1)
            for i_ in existing_circuit:
                boxes_assigned[i_] = existing_circuit
        elif p1 in boxes_assigned:
            existing_circuit = boxes_assigned[p1]
            existing_circuit.add(p0)
            for i_ in existing_circuit:
                boxes_assigned[i_] = existing_circuit
        else:
            new_circuit = set([p0, p1])
            boxes_assigned[p0] = new_circuit
            boxes_assigned[p1] = new_circuit

        # print(boxes_assigned)

    print(len(boxes_assigned))
    circuits = set([tuple(i) for i in boxes_assigned.values()])
    sorted_circuits = sorted(list(circuits), key=lambda x: len(x), reverse=True)
    # print(sorted_circuits)
    circuit_lengths = [len(i) for i in sorted_circuits]
    print(circuit_lengths)
    print(sum(circuit_lengths))
    print(np.prod(circuit_lengths[:3]))

    # print(box_coords.shape, distances.shape)
    # print(argmin_2d(distances))
