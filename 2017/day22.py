from pathlib import Path
import sys

from queue import Queue, Empty
#import time
#from collections import defaultdict
from functools import lru_cache


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

#from dataclasses import dataclass
from typing import List

Grid = List[List[str]]  # 2D grid of characters


# ============================================================
# PRINTING (unchanged)
# ============================================================
def print_grid2(grid: Grid, posx: int, posy: int) -> None:
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        out = ""
        for x in range(width):
            ch = grid[y][x]

            if x == posx and y == posy:
                out += f"[{ch}]"
            else:
                if out and not out.endswith("]"):
                    out += " "
                out += ch
        print(out)
    print()


# ============================================================
# COORDINATES AND DYNAMIC EXPANSION
# ============================================================
def ensure_inside(grid: Grid, x: int, y: int, origin_x: int, origin_y: int):
    """Ensures (x,y) fits inside the grid, expands if needed."""
    height = len(grid)
    width = len(grid[0])

    gx = x + origin_x
    gy = y + origin_y

    # Expand upward
    if gy < 0:
        grid.insert(0, ["." for _ in range(width)])
        origin_y += 1
        gy = 0

    # Expand downward
    if gy >= height:
        grid.append(["." for _ in range(width)])
        height += 1

    # Expand left
    if gx < 0:
        for row in grid:
            row.insert(0, ".")
        origin_x += 1
        gx = 0

    # Expand right
    if gx >= width:
        for row in grid:
            row.append(".")
        width += 1

    return grid, origin_x, origin_y

@lru_cache(None)
def to_grid_coords(x: int, y: int, origin_x: int, origin_y: int):
    """Convert logical coordinates to grid indices."""
    return y + origin_y, x + origin_x


# ============================================================
# DIRECTION HELPERS
# ============================================================
@lru_cache(None)
def rotate_right(dx: int, dy: int) -> tuple[int, int]:
    return -dy, dx

@lru_cache(None)
def rotate_left(dx: int, dy: int) -> tuple[int, int]:
    return dy, -dx


# ============================================================
# PART A SIMULATION
# ============================================================
def simulate_part_a(grid: Grid, steps: int = 10000) -> int:
    """
    Simulate the Part A infection process for a set number of steps.
    Returns total infections caused.
    """

    # Center origin
    origin_x = len(grid[0]) // 2
    origin_y = len(grid) // 2

    x, y = 0, 0         # logical position
    dx, dy = 0, -1      # facing UP
    infections = 0

    for _ in range(steps):
        # Convert to grid coords
        gy, gx = to_grid_coords(x, y, origin_x, origin_y)

        # Act based on state of the node
        if grid[gy][gx] == '#':
            dx, dy = rotate_right(dx, dy)
            grid[gy][gx] = '.'

        elif grid[gy][gx] == '.':
            dx, dy = rotate_left(dx, dy)
            grid[gy][gx] = '#'
            infections += 1

        else:
            raise RuntimeError("Unexpected grid state!")

        # Move forward
        x += dx
        y += dy

        # Expand grid if stepping outside
        grid, origin_x, origin_y = ensure_inside(grid, x, y, origin_x, origin_y)

    return infections

def simulate_part_b(grid: Grid, steps: int = 10000) -> int:
    # Center origin
    origin_x = len(grid[0]) // 2
    origin_y = len(grid) // 2

    x, y = 0, 0         # logical position
    dx, dy = 0, -1      # facing UP
    infections = 0

    for i in range(steps):
        if i%500000 == 0:
            print(float(i)/(float(steps)))
        # Convert to grid coords
        gy, gx = to_grid_coords(x, y, origin_x, origin_y)
       # print_grid2(grid,gx,gy)
        # Clean nodes become weakened.
        # Weakened nodes become infected.
        # Infected nodes become flagged.
        # Flagged nodes become clean.

        # Act based on state of the node
        if grid[gy][gx] == '.':
            dx, dy = rotate_left(dx, dy)
            grid[gy][gx] = 'W' # cleaned becomes weakened            
        elif grid[gy][gx] == 'W':
            # no turning
            grid[gy][gx] = '#'  # weakened becomes infected
            infections += 1
        elif grid[gy][gx] == '#':
            dx, dy = rotate_right(dx, dy)
            grid[gy][gx] = 'F'  # infected becomes flagged
        elif grid[gy][gx] == 'F':
            dx, dy = rotate_right(dx, dy)
            dx, dy = rotate_right(dx, dy)
            grid[gy][gx] = '.'  # flagged becomes cleaned



        else:
            raise RuntimeError("Unexpected grid state!")

         # Move forward
        x += dx
        y += dy

        # Expand grid if stepping outside
        grid, origin_x, origin_y = ensure_inside(grid, x, y, origin_x, origin_y)

     #   print_grid2(grid,gx,gy)
    return infections

# ============================================================
# MAIN
# ============================================================
def main():
    lines = read_lines(Path(__file__).resolve().parent / "input/day22.txt")
    grid = [list(line) for line in lines]

    # --- Part A ---
    result_a = simulate_part_a(grid)
    print("Day 22 a =", result_a)

    # --- Part B ---
    grid2 = [list(line) for line in lines]
    result_b = simulate_part_b(grid2,10000000)
    
    print("Day 22 b =", result_b)


if __name__ == "__main__":
    main()
