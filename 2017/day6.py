

from ast import Num
from pathlib import Path
import sys
from tkinter import N
from numba.stencils.stencil import StencilFuncLowerer
import numpy as np
from numba import njit

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

#@njit

def index_of_largest(lst):
    if not lst:
        raise ValueError("List is empty")
    max_val = lst[0]
    max_idx = 0
    for i, val in enumerate(lst):
        if val > max_val:
            max_val = val
            max_idx = i
    return max_idx

def index_of_key(d, key):
    for i, k in enumerate(d):
        if k == key:
            return i
    raise KeyError(f"{key} not found")



def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day6.txt')

    index = 0
    steps = 0

    seen = set()

    numbers = list(map(int, lines[0].split()))

    while 1:
        steps = steps + 1
        largest_num = numbers[index_of_largest(numbers)]
        index = index_of_largest(numbers)
        to_distribute = numbers[index]
        numbers[index] = 0      
        
        while to_distribute > 0:
            index = (index + 1) % len(numbers)
            numbers[index] += 1
            to_distribute -= 1        
        
        if tuple(numbers) in seen:
            break
        seen.add(tuple(numbers))

    print("Day 6 a = ", steps)

    seen = {}  # dict so we can index the number series
    idx2 = 0
    index = 0
    steps = 0

    numbers = list(map(int, lines[0].split()))
    while 1:
        steps = steps + 1
        largest_num = numbers[index_of_largest(numbers)]
        index = index_of_largest(numbers)
        to_distribute = numbers[index]
        numbers[index] = 0      
        
        while to_distribute > 0:
            index = (index + 1) % len(numbers)
            numbers[index] += 1
            to_distribute -= 1        
        
        key = tuple(numbers)
        if key in seen:
            break
        seen[key] = steps

    print("Day 6 b = ", steps - index_of_key(seen,key)-1) 
    



   

if __name__ == "__main__":
    main()
