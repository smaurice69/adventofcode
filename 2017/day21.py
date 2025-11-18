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


import math

def combine_blocks(blocks: List[Grid]) -> Grid:
    """
    Combine equally-sized square blocks into one big grid.

    `blocks` is a flat list in row-major order:
        [ b00, b01, ..., b0N,
          b10, b11, ..., b1N,
          ...
        ]
    """
    if not blocks:
        return []

    block_size = len(blocks[0])            # e.g. 3 or 4
    num_blocks = len(blocks)
    blocks_per_row = int(math.isqrt(num_blocks))

    if blocks_per_row * blocks_per_row != num_blocks:
        raise ValueError(f"Number of blocks ({num_blocks}) is not a perfect square")

    final_size = blocks_per_row * block_size
    combined: Grid = [[""] * final_size for _ in range(final_size)]

    for idx, block in enumerate(blocks):
        br = idx // blocks_per_row        # block row
        bc = idx % blocks_per_row         # block col
        for r in range(block_size):
            for c in range(block_size):
                combined[br * block_size + r][bc * block_size + c] = block[r][c]

    return combined


def flip_horizontal(grid: Grid) -> Grid:
    """Flip grid horizontally (mirror left-right)."""
    return [list(reversed(row)) for row in grid]

def print_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))

def print_blocks(blocks: List[Grid], block_size: int) -> None:
    """
    Print a list of NxN blocks laid out in their natural square arrangement.
    (Same structure as split_grid produces)
    """
    num_blocks = len(blocks)
    blocks_per_row = int(num_blocks ** 0.5)

    for br in range(blocks_per_row):            # block row
        for r in range(block_size):             # row inside each block
            line = []
            for bc in range(blocks_per_row):    # block column
                block_index = br * blocks_per_row + bc
                block = blocks[block_index]
                line.append("".join(block[r]))
            print(" ".join(line))
        print()  # blank line between block rows


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

def grid_to_key(grid: Grid) -> str:
    """Convert a grid into a string key like '.#./..#/###'."""
    return "/".join("".join(row) for row in grid)

def build_rule_map(rules: List[Rule]) -> dict[str, Grid]:
    """
    Build a dict mapping *all variants* of each input pattern to its output grid.
    Key: string form of variant (e.g. '.#./..#/###')
    Value: the rule's output Grid
    """
    rule_map: dict[str, Grid] = {}

    for rule in rules:
        for variant in all_variants(rule.inp):
            key = grid_to_key(variant)
            rule_map[key] = rule.out   # overwrite is fine; all variants map to same out

    return rule_map

def enhance_block(block: Grid, rule_map: dict[str, Grid]) -> Optional[Grid]:
    """Return transformed block using precomputed rule_map, or None if no match."""
    key = grid_to_key(block)
    return rule_map.get(key)


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

        lines = read_lines(Path(__file__).resolve().parent / "input/day21.txt")
        rules: List[Rule] = load_rules(lines)
        rule_map = build_rule_map(rules)

        # Starting pattern as given
        start_str = ".#./..#/###"
        grid = parse_pattern(start_str)

        for i in range(18):
           # print(f"\n=== Iteration {i} ===")
         #   print("Current grid:")
         #   print_grid(grid)

            size = len(grid)
            if size % 2 == 0:
                block_size = 2
             #   print("Divisible by 2, using 2x2 blocks")
            elif size % 3 == 0:
                block_size = 3
             #   print("Divisible by 3, using 3x3 blocks")
            else:
                print("ERROR: grid size not divisible by 2 or 3!")
                return

            # 1) split grid into blocks of size block_size
            blocks = split_grid(grid, block_size=block_size)

            # 2) transform each block via matching rule
            new_blocks: List[Grid] = []
            for block in blocks:
                out_block = enhance_block(block, rule_map)
                if out_block is None:
                    print("No matching rule found for block:")
                    print_grid(block)
                    return
                new_blocks.append(out_block)

            # Debug: see the blocks after transformation
       #     print("\nBlocks after applying rules:")
       #     print_blocks(new_blocks, block_size + 1)  # out blocks are +1 in size (2→3, 3→4)

            # 3) combine transformed blocks into the next grid
            grid = combine_blocks(new_blocks)
            if i == 4:
                on_counta = sum(row.count("#") for row in grid)
       # print("\nFinal grid after 5 iterations:")
       # print_grid(grid)

        # Example: count lit pixels (#)
        on_count = sum(row.count("#") for row in grid)
        print("Day 21 a = ", on_counta)
        print("Day 21 b = ", on_count)  # placeholder if you’re doing part b later


if __name__ == "__main__":
    main()
