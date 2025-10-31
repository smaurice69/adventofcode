"""Day 2 solution."""

from ast import Num
from pathlib import Path
import sys
import numpy as np
from numba import njit

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

@njit
def jump_process_part_b(numbers):
    idx = 0
    steps = 0
    n = len(numbers)
    while 0 <= idx < n:
        val = numbers[idx]
        numbers[idx] += -1 if val >= 3 else 1
        idx += val
        steps += 1
    return steps

@njit
def jump_process(numbers):
    idx = 0
    steps = 0
    n = len(numbers)
    while 0 <= idx < n:
        val = numbers[idx]
        numbers[idx] += 1
        idx += val
        steps += 1
    return steps

def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day5.txt')

    index = 0
    steps = 0

    numbers = [int(line.strip()) for line in lines if line.strip()]

   # numbers = original.copy()
    n = len(numbers)

    while 0 <= index < n:
       # if index < 0 or index >= len(numbers):
       #     break
        numbers[index] += 1
        index = index + numbers[index] - 1
        steps+=1
       # print(numbers)

   # print ("Day 2 a = ", steps)
   # numbers = [int(line.strip()) for line in lines if line.strip()]
    print("Day 2 a2 =", jump_process(numbers))
    numbers = [int(line.strip()) for line in lines if line.strip()]
    print("Day 2 b =", jump_process_part_b(numbers))

   

if __name__ == "__main__":
    main()
