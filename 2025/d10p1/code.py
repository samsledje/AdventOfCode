import sys
import re
import numpy as np
import networkx as nx


def build_button_mask(b, nmax):
    toggles = b.strip("(").strip(")").split(",")
    mask = ""
    for i in range(nmax):
        mask += "1" if str(i) in toggles else "0"

    return int(mask, 2)


if __name__ == "__main__":
    matcher = re.compile(r"^\[(.*)\] (\((?:\d+,*)+\).*)* \{(.*)\}$")

    total_shortest_dist = 0

    with open(sys.argv[1], "r") as f:
        for line in f:
            match = re.match(matcher, line)
            lights = match.group(1).replace(".", "0").replace("#", "1")
            n_lights = len(lights)
            buttons = [build_button_mask(b, n_lights) for b in match.group(2).split()]
            target_light = int(lights, 2)
            joltage = np.array([int(i) for i in match.group(3).split(",")])

            edges = []
            for source in range(2**n_lights):
                for button in buttons:
                    target = source ^ button
                    edges.append([source, target])

            graph = nx.from_edgelist(edges)
            shortest_dist = nx.shortest_path_length(graph, 0, target_light)
            total_shortest_dist += shortest_dist

        print(total_shortest_dist)
