"""Day 10 solution."""
import numbers
from pathlib import Path
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

import re

from dataclasses import dataclass
from math import sqrt, floor

@dataclass(frozen=True)
class Hex:
    q: float
    r: float

# Flat-top directions: E, SE, SW, W, NW, NE
DIRS = [
    Hex(+1,  0), Hex(+1, -1), Hex(0, -1),
    Hex(-1,  0), Hex(-1, +1), Hex(0, +1),
]

# AoC 6-dir labels -> flat-top axial deltas
DIRECTION_VECTORS = {
    "n":  (0, -1),   # our SW
    "ne": (1, -1),   # our SE
    "se": (1,  0),   # our E
    "s":  (0,  1),   # our NE
    "sw": (-1, 1),   # our NW
    "nw": (-1, 0),   # our W
}


def move(h: Hex, direction: str) -> Hex:
    """Return a new Hex moved one step (or approximate) in given direction."""
    direction = direction.lower()
    if direction not in DIRECTION_VECTORS:
        raise ValueError(f"Invalid direction '{direction}'. Must be one of {list(DIRECTION_VECTORS)}")

    dq, dr = DIRECTION_VECTORS[direction]
    return Hex(h.q + dq, h.r + dr)



def add(a: Hex, b: Hex) -> Hex:
    return Hex(a.q + b.q, a.r + b.r)

def neighbor(a: Hex, d: int) -> Hex:
    return add(a, DIRS[d % 6])

def distance(a: Hex, b: Hex) -> int:
    # axial distance without exposing cube coords
    dq, dr = a.q - b.q, a.r - b.r
    return int((abs(dq) + abs(dq + dr) + abs(dr)) // 2)

# ------- line drawing (inclusive) -------
def _axial_round(h: Hex) -> Hex:
    # round fractional axial via implicit cube rounding
    x, z = h.q, h.r
    y = -x - z
    rx, ry, rz = round(x), round(y), round(z)
    dx, dy, dz = abs(rx - x), abs(ry - y), abs(rz - z)

    if dx > dy and dx > dz:
        rx = -ry - rz
    elif dy > dz:
        ry = -rx - rz
    else:
        rz = -rx - ry
    return Hex(rx, rz)

def line(a: Hex, b: Hex):
    """Yield Hexes from a to b (inclusive)."""
    n = distance(a, b)
    if n == 0:
        yield Hex(int(a.q), int(a.r))
        return
    for i in range(n + 1):
        t = i / n
        yield _axial_round(Hex(a.q * (1 - t) + b.q * t,
                               a.r * (1 - t) + b.r * t))

# ------- axial <-> pixel (flat-top) -------
# size = hex radius (center to side)
# x = 1.5*size*q
# y = sqrt(3)*size*(r + q/2)
def axial_to_pixel(h: Hex, size: float, ox: float = 0.0, oy: float = 0.0) -> tuple[float, float]:
    x = size * (1.5 * h.q)
    y = size * (sqrt(3) * (h.r + h.q / 2.0))
    return (x + ox, y + oy)

def pixel_to_axial(x: float, y: float, size: float, ox: float = 0.0, oy: float = 0.0) -> Hex:
    px, py = x - ox, y - oy
    qf = (2.0 / 3.0) * (px / size)
    rf = (-1.0 / 3.0) * (px / size) + (py / (sqrt(3) * size))
    return _axial_round(Hex(qf, rf))


def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day11.txt')
    dirs = list(lines[0].split(","))

   # a, b = Hex(0, 0), Hex(3, -1)

    #dirs = ["ne","ne","s","s"]

    maxdist = 0
    shex = Hex(0,0)
    nexthex = shex
    for i in dirs:
        nexthex = move(nexthex,i)
        if(distance(nexthex, shex) > maxdist):
            maxdist = distance(nexthex, shex)


    print("Day 11 a = ", distance(nexthex, shex))
    print("Day 11 b = ", maxdist)

if __name__ == "__main__":
    main()
