"""Day 10 solution."""
import numbers
from pathlib import Path
import sys
import re
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.shortest_paths import has_path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


from dataclasses import dataclass
from math import sqrt, floor


def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day12.txt')
    
    edges = []

    for i in range(len(lines)):
        dirs = list(lines[i].split("<->"))
        left = dirs[0].strip()
        for x in dirs[1].split(","):
            right = x.strip()
            edges.append((left,right))

    G = nx.Graph()

    G.add_edges_from(edges)

    numcool = 0
    for i in range(len(lines)):
        dirs = list(lines[i].split("<->"))
        left = dirs[0].strip()
        if nx.has_path(G,"0",left):
            numcool+=1

    print("Day 12 a = ", numcool)


    num_groups = nx.number_connected_components(G)
    print("Day 12 b = ",num_groups)


"""
    print("Undirected: is whole graph connected?", nx.is_connected(G))
    print("Undirected: connected components:")
    cc = list(nx.connected_components(G))
  #  for i, comp in enumerate(cc, 1):
  #      print(f"  Component {i}: {sorted(comp)}")

    # Are two specific nodes connected?
    u, v = "2", "3"
    print(f"Path {u}->{v} exists?", nx.has_path(G, u, v))

    # Visualize components with colors
    pos = nx.spring_layout(G, seed=0)
    pos = nx.spring_layout(G, seed=0)
    color_map = {}
    for idx, comp in enumerate(cc):
        for n in comp:
            color_map[n] = idx
    node_colors = [color_map[n] for n in G.nodes()]

    plt.figure()
    nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap="tab10")
    plt.title("Undirected graph – connected components")
    plt.show()
"""
    


if __name__ == "__main__":
    main()
