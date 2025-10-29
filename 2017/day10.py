"""Day 10 solution."""

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
       # print("current length:", cur_length)
        old_nums = numbers.copy()
        numbers = reverse_circular(numbers, current_position, cur_length)
       # print("Old numbers:", old_nums, "New numbers:", numbers)
        current_position = (current_position + cur_length + skip_size) % len(numbers)  # <-- fix
        skip_size += 1
       # print("current length =", cur_length, ", current position =", current_position, ", skip_size =", skip_size)
       # print(numbers)

    print("Day 10 a =", numbers[0]*numbers[1])  # total group score


if __name__ == "__main__":
    main()
