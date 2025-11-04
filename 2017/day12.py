"""Day 10 solution."""
import numbers
from pathlib import Path
import sys
import re
import networkx as nx
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


from dataclasses import dataclass
from math import sqrt, floor


def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day11.txt')
    dirs = list(lines[0].split(","))


    print("Day 12 a = ", 2)
    print("Day 12 b = ", 3)

    # ---------- 1) Undirected graph ----------
    G = nx.Graph()
    G.add_edges_from([
        ("A", "B"), ("A", "C"), ("B", "D"),
        # second island:
        ("X", "Y")
    ])
    G.add_node("Z")  # isolated node

    print("Undirected: is whole graph connected?", nx.is_connected(G))
    print("Undirected: connected components:")
    cc = list(nx.connected_components(G))
    for i, comp in enumerate(cc, 1):
        print(f"  Component {i}: {sorted(comp)}")

    # Are two specific nodes connected?
    u, v = "A", "D"
    print(f"Path {u}->{v} exists?", nx.has_path(G, u, v))

    # Visualize components with colors
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

    # ---------- 2) Directed graph (SCCs) ----------
    DG = nx.DiGraph()
    DG.add_edges_from([
        # SCC1
        ("a", "b"), ("b", "c"), ("c", "a"),
        # SCC2
        ("d", "e"), ("e", "d"),
        # cross edges (do not merge SCCs unless both directions exist)
        ("c", "d"),  # a path from SCC1 -> SCC2
        ("f", "g")  # singleton chain; no way back
    ])

    print("\nDirected: is strongly connected?", nx.is_strongly_connected(DG))
    print("Directed: strongly connected components (SCCs):")
    scc = list(nx.strongly_connected_components(DG))
    for i, comp in enumerate(scc, 1):
        print(f"  SCC {i}: {sorted(comp)}")

    # Check reachability between two nodes (directed)
    s, t = "a", "e"
    print(f"Directed path {s}->{t} exists?", nx.has_path(DG, s, t))

    # Visualize SCCs with colors
    pos2 = nx.spring_layout(DG, seed=1)
    color_map2 = {}
    for idx, comp in enumerate(scc):
        for n in comp:
            color_map2[n] = idx
    node_colors2 = [color_map2[n] for n in DG.nodes()]

    plt.figure()
    nx.draw_networkx(DG, pos2, node_color=node_colors2, cmap="tab10", arrows=True)
    plt.title("Directed graph – strongly connected components")
    plt.show()

    # Bonus: condensation graph (DAG of SCCs)
    C = nx.condensation(DG)  # each SCC collapses to a node
    plt.figure()
    nx.draw_networkx(C, with_labels=True)
    plt.title("Condensation DAG (each node is an SCC)")
    plt.show()



if __name__ == "__main__":
    main()
