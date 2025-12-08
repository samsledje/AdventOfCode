import sys
import numpy as np
import networkx as nx
from tqdm import tqdm


if __name__ == "__main__":
    manifold = []
    memo = {}

    start_pos = (None, None)
    splitter_pos = []

    with open(sys.argv[1], "r") as f:
        for i, line in enumerate(f):
            for j, char in enumerate(line):
                if char == "S":
                    start_pos = (i, j)
                elif char == "^":
                    splitter_pos.append((i, j))
    splitter_pos = np.array(splitter_pos)

    n_nodes = splitter_pos.shape[0]
    edges = {i: [n_nodes, n_nodes] for i in range(n_nodes)}
    edgelist = []
    sinks = list(range(n_nodes, n_nodes + j))
    sink_map = {i: s for i, s in enumerate(sinks)}

    # Build edges
    for i, (y, x) in enumerate(splitter_pos):
        edges[i] = [sink_map[int(x) - 1], sink_map[int(x) + 1]]
        remaining = splitter_pos[i + 1 :, :]
        for j, (y2, x2) in enumerate(remaining):
            if (x + 1 == x2) and (y < y2) and (edges[i][1] >= n_nodes):
                edges[i][1] = j + i + 1
            elif (x - 1 == x2) and (y < y2) and (edges[i][0] >= n_nodes):
                edges[i][0] = j + i + 1

    for s in sinks:
        edges[s] = []

    # print(start_pos)
    # print(splitter_pos)
    print(edges)

    G = nx.from_dict_of_lists(edges, create_using=nx.DiGraph)
    print(G)
    print(f"Number of sinks: {len(sinks)}")
    all_paths = []
    for path in nx.all_simple_paths(G, 0, sinks):
        all_paths.append(path)

    for i, p in enumerate(all_paths):
        print(f"{i} {p}")

    print(len(all_paths))
