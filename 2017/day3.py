"""Day 2 solution."""

grid = {}
grid[0,0] = 1

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines



import math

def spiral_coords(n: int) -> tuple[int, int]:
    """Return (x, y) coordinates of n in an infinite square spiral 
    centered at (0, 0) with 1 at the origin."""
    if n == 1:
        return (0, 0)
    
    k = math.ceil((math.sqrt(n) - 1) / 2)  # ring index
    t = 2 * k + 1                           # side length
    m = t ** 2                              # max value in this ring
    d = m - n                               # steps from bottom-right corner
    edge = t - 1                            # length of each edge
    
    if d < edge:  # bottom edge (moving left)
        return (k - d, -k)
    elif d < 2 * edge:  # left edge (moving up)
        d -= edge
        return (-k, -k + d)
    elif d < 3 * edge:  # top edge (moving right)
        d -= 2 * edge
        return (-k + d, k)
    else:  # right edge (moving down)
        d -= 3 * edge
        return (k, k - d)


def manhattan_distance_from_origin(coords: tuple[int, int]) -> int:
    x1, y1 = coords
    return abs(x1) + abs(y1)

def get_value(x,y):
    return grid.get((x,y),0)
def sum_neighbors(x, y):
    total = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue  # skip the center cell
            total += get_value(x + dx, y + dy)
    return total

def print_grid(radius):
    for y in range(-radius, radius + 1):  # print top to bottom
        row = []
        for x in range(-radius, radius + 1):
            val = get_value(x, y)
            row.append(f"{val:3d}")  # formatted width for alignment
        print(" ".join(row))

def run_until_threshold(THRESHOLD):
    the_num = None

    for radius in range(1, 5):
        # First loop: y = radius-1, radius-2, ..., 0, -1, ..., -radius
        for y in range(radius - 1, -radius - 1, -1):
            val = sum_neighbors(radius, y)
            grid[(radius, y)] = val
            if val > THRESHOLD:
                return val  # exit immediately

        for x in range(radius, -radius - 1, -1):
            val = sum_neighbors(x, -radius)
            grid[(x, -radius)] = val
            if val > THRESHOLD:
                return val

        for y in range(-radius + 1, radius + 1):
            val = sum_neighbors(-radius, y)
            grid[(-radius, y)] = val
            if val > THRESHOLD:
                return val

        for x in range(-radius + 1, radius + 1):
            val = sum_neighbors(x, radius)
            grid[(x, radius)] = val
            if val > THRESHOLD:
                return val

        # Second loop: only the topmost y = radius
        for y in (radius,):
            val = sum_neighbors(radius, y)
            grid[(radius, y)] = val
            if val > THRESHOLD:
                return val

    return the_num  # None if never exceeded



def main():

 #   lines = read_lines(Path(__file__).resolve().parent / 'input/day2.txt')
        
    
    print("Day 3 a = ",manhattan_distance_from_origin(spiral_coords(368078)))

    THRESHOLD = 368078  # ← set your desired cutoff value here
    print("Day 3 b = ",run_until_threshold(THRESHOLD))




if __name__ == "__main__":
    main()
