import sys
import networkx as nx

if __name__ == "__main__":
    edgelist = []

    with open(sys.argv[1], "r") as f:
        for line in f:
            source, targets = line.strip().split(":")
            targets = targets.strip().split()
            for t in targets:
                edgelist.append([source, t])

    # print(edgelist)
    G = nx.from_edgelist(edgelist, create_using=nx.DiGraph)

    num_paths = 0
    for p in nx.all_simple_paths(G, "you", "out"):
        num_paths += 1
    print(num_paths)
