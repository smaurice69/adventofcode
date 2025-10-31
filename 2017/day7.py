

#from ast import Num
from pathlib import Path

import sys
#from tkinter import N
#from numba.stencils.stencil import StencilFuncLowerer
#import numpy as np
#from numba import njit
#from bigtree import Node
#from bigtree import list_to_tree
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines
from utils.node import Node

def iter_leaves(node):
    if not node.children:
        yield node
        return
    for ch in node.children:
        yield from iter_leaves(ch)

def iter_paths(root):
    path = []

    def dfs(n):
        path.append(n)
        if not n.children:           # leaf
            yield list(path)
        else:
            for ch in n.children:
                yield from dfs(ch)
        path.pop()

    yield from dfs(root)

def iter_path_names(root, sep="/"):
    for path in iter_paths(root):
        yield sep.join(n.name for n in path)

def iter_paths_with_weight(root):
    for path in iter_paths(root):
        total = sum(n.attrs.get("weight", getattr(n, "weight", 0)) for n in path)
        yield path, total

def node_weight(n):
    w = n.attrs.get("weight", getattr(n, "weight", 0))
    try:
        return int(w)
    except (TypeError, ValueError):
        return 0

def subtree_sum(node, memo=None):
    if memo is None:
        memo = {}
    key = id(node)                     # or node.name if names are unique
    if key in memo:
        return memo[key]
    total = node_weight(node)
    for ch in node.children:
        total += subtree_sum(ch, memo)
    memo[key] = total                  # ✅ store before returning
    return total



from collections import Counter

def find_correction(root):
    memo = {}

    def dfs(n):
        if len(n.children) <= 1:
            return None

        # compute subtree totals for each child
        child_sums = [(ch, subtree_sum(ch, memo)) for ch in n.children]
        counts = Counter(s for _, s in child_sums)

        if len(counts) == 1:
            return None  # this level is balanced

        # Find the outlier and the intended (target) weight
        target_total = counts.most_common(1)[0][0]
        unique_total = next(s for s, c in counts.items() if c == 1)
        off_child = next(ch for ch, s in child_sums if s == unique_total)

        # Recurse deeper to find the actual culprit
        deeper = dfs(off_child)
        if deeper:
            return deeper

        # This node is the culprit: adjust its own weight
        missing = target_total - unique_total
        corrected = node_weight(off_child) + missing
        return off_child, corrected

    return dfs(root)




def print_level1_sums(root):
    for child in root.children:
        total = subtree_sum(child)
        print(f"{child.name}: total subtree weight = {total}")

def find_imbalance(root):
    # (level-1 node, its total subtree weight)
    pairs = [(child, subtree_sum(child)) for child in root.children]
    totals = [t for _, t in pairs]
    cnt = Counter(totals)

    # unique (the odd one out) and target (the common total among siblings)
    try:
        unique_total = next(t for t, c in cnt.items() if c == 1)
        target_total = next(t for t, c in cnt.items() if c > 1)
    except StopIteration:
        raise ValueError("No imbalance at level 1 (all subtree totals equal).")

    # the level-1 node that is off
    off_node = next(ch for ch, t in pairs if t == unique_total)

    # how much that branch is missing/excess vs the target
    missing = target_total - unique_total           # positive => needs to increase
    new_weight = node_weight(off_node) + missing    # corrected own weight

    return missing, new_weight



def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day7.txt')

    nodes: dict[str, Node] = {}

    def get_node(name: str) -> Node:
        n = nodes.get(name)
        if n is None:
            n = Node(name)
            nodes[name] = n
        return n

    parents, children = set(), set()
    
    for line in lines:
        toks = line.split()
        if not toks:
            continue

        parent_name = toks[0]
        parent = get_node(parent_name)
        parent.attrs["weight"] = int(toks[1].lstrip('(').rstrip(')'))
        parents.add(parent_name)

        if "->" in toks:
            arrow = toks.index("->")
            for t in toks[arrow + 1:]:
                child_name = t.rstrip(",")
                child = get_node(child_name)
                parent.add_child(child)         # <-- important: link BOTH sides
                children.add(child_name)

    root_name = (parents - children).pop()
    root = nodes[root_name]
    
    

    culprit, corrected = find_correction(root)
    print("Day 7 a =", root.name)
    print("Day 7 b =", corrected)   # the weight off_child should have



   

if __name__ == "__main__":
    main()
