from pathlib import Path
import sys
import threading
from queue import Queue, Empty
import time
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

from dataclasses import dataclass
from typing import List, Optional

Grid = List[List[str]]  # 2D grid of characters

@dataclass
class Rule:
    inp: Grid
    out: Grid


def parse_pattern(pattern: str) -> Grid:
    """
    "../.#" -> [[".", "."],
                [".", "#"]]
    """
    return [list(row) for row in pattern.split("/")]


def load_rules(lines: List[str]) -> List[Rule]:
    rules: List[Rule] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        inp_str, out_str = line.split(" => ")
        inp = parse_pattern(inp_str)
        out = parse_pattern(out_str)
        rules.append(Rule(inp=inp, out=out))
    return rules

def rotate(grid: Grid) -> Grid:
    """Rotate grid 90° clockwise."""
    size = len(grid)
    return [[grid[size - j - 1][i] for j in range(size)] for i in range(size)]


def flip_horizontal(grid: Grid) -> Grid:
    """Flip grid horizontally (mirror left-right)."""
    return [list(reversed(row)) for row in grid]


def all_variants(grid: Grid) -> List[Grid]:
    """
    All 8 variants: 4 rotations × (normal + flipped).
    """
    variants = []
    g = grid
    for _ in range(4):
        variants.append(g)
        variants.append(flip_horizontal(g))
        g = rotate(g)
    # Optionally deduplicate if you care
    return variants

def find_matching_rule(grid: Grid, rules: List[Rule]) -> Optional[Rule]:
    """
    Return the first rule whose input pattern matches the grid
    (considering rotations and flips).
    """
    for rule in rules:
        for variant in all_variants(grid):
            if variant == rule.inp:
                return rule
    return None

def split_grid(grid: Grid, block_size: int) -> List[Grid]:
    """
    Split a 2D grid into evenly sized block_size × block_size subgrids.
    Returns a list of grids (row-major order).
    """
    size = len(grid)
    blocks: List[Grid] = []

    for row in range(0, size, block_size):
        for col in range(0, size, block_size):
            block = [grid[r][col:col + block_size]
                     for r in range(row, row + block_size)]
            blocks.append(block)

    return blocks

def main():

    lines = read_lines(Path(__file__).resolve().parent / "input/day21test.txt")
    rules: List[Rule] = load_rules(lines)

    # Starting pattern as given
    start_str = ".#./..#/###"

    grid = parse_pattern(start_str)

    print("Starting grid:")
    for row in grid:
        print("".join(row))
    numdiv = 1
    blocksize = len(grid[0])
    if(len(grid[0])%3==0):
        numdiv = len (grid[0]) // 3
        blocksize = 3
        print("Divisible by 3, numdiv =", numdiv)

    elif(len(grid[0])%2==0):
        numdiv = len(grid[0]) // 2
        blocksize = 2
        print("Divisible by 2, numdiv =", numdiv)

    else:
        print("ERROR!")



    #split into numdiv by numdiv grids
    grids = split_grid(grid, block_size=blocksize)
    print(grids)
    # Find matching rule
    rule = find_matching_rule(grid, rules)
    if rule is None:
        print("No matching rule found.")
        return

    print("\nMatched rule:")
    for row in rule.inp:
        print("".join(row))

    print("\nOutput pattern:")
    for row in rule.out:
        print("".join(row))

    print("Day 21 a = ", 0)
    print("Day 21 b = ", 0)


if __name__ == "__main__":
    main()
