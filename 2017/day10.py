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

def reverse_circular(lst, start, length):
    n = len(lst)
    for i in range(length // 2):
        a = (start + i) % n
        b = (start + length - 1 - i) % n
        lst[a], lst[b] = lst[b], lst[a]
    return lst


def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day10.txt')

    lengths = list(map(int, lines[0].split(",")))
    numbers = list(range(256))
   # lengths = [3, 4, 1, 5]
   # numbers = [0, 1, 2, 3, 4]
    current_position = 0
    skip_size = 0

    while skip_size < len(lengths):
        cur_length = lengths[skip_size]
        old_nums = numbers.copy()
        numbers = reverse_circular(numbers, current_position, cur_length)
        current_position = (current_position + cur_length + skip_size) % len(numbers)  # <-- fix
        skip_size += 1

    print("Day 10 a =", numbers[0]*numbers[1])  # total group score

    # ---------------- Part 2 (Knot Hash) ----------------
    # Convert to ASCII codes + suffix
    raw = lines[0].strip()

    ascii_lengths = [ord(c) for c in raw] + [17, 31, 73, 47, 23]
    # comment
    numbers = list(range(256))
    current_position = 0
    skip_size = 0

    for _ in range(64):
        for length in ascii_lengths:  # <-- iterate lengths EACH round
            reverse_circular(numbers, current_position, length)
            current_position = (current_position + length + skip_size) % len(numbers)
            skip_size += 1

    # Dense hash: XOR blocks of 16
    dense = []
    for block in range(16):
        x = 0
        base = block * 16
        for j in range(16):
            x ^= numbers[base + j]
        dense.append(x)

    # Hex digest (two lowercase hex digits per byte)
    hex_str = ''.join(f'{b:02x}' for b in dense)
    print("Day 10 b = ", hex_str)


if __name__ == "__main__":
    main()
