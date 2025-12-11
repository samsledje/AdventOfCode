import sys
import networkx as nx
from functools import lru_cache


@lru_cache(maxsize=10000)
def count_paths(G: nx.Graph, src: str, target: str):
    if target in nx.neighbors(G, src):
        return 1
    else:
        num_paths = 0
        for n in nx.neighbors(G, src):
            num_paths += count_paths(G, n, target)

        return num_paths


if __name__ == "__main__":
    edgelist = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            source, targets = line.strip().split(":")
            targets = targets.strip().split()
            for t in targets:
                edgelist.append([source, t])

    G = nx.from_edgelist(edgelist, create_using=nx.DiGraph)
    G_r = nx.reverse_view(G)

    num_paths = 0

    paths_start = count_paths(G, "svr", "fft")
    paths_mid = count_paths(G, "fft", "dac")
    paths_end = count_paths(G, "dac", "out")

    print(paths_start * paths_mid * paths_end)
