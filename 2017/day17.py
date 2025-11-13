"""Day 17 solution."""
import copy
import numbers
from pathlib import Path
import string
import sys
import re
from collections import deque
import numpy as np
from numba import njit

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class CircularBuffer:
    def __init__(self, first_value):
        """Create a circular buffer with a single starting value (e.g. 0)."""
        first = Node(first_value)
        first.next = first        # points to itself
        self.head = first         # fixed start for printing (your 0)
        self.current = first      # moving pointer

    def move(self, n):
        """Move n steps forward from the current node."""
        if self.current is None:
            return

        for _ in range(n):
            self.current = self.current.next

    def index_of(self, value):
        if self.head is None:
            return -1

        idx = 0
        node = self.head
        first_loop = True

        while first_loop or node is not self.head:
            first_loop = False

            if node.value == value:
                return idx

            idx += 1
            node = node.next

        return -1  # not found
    def value_after_index(self, index):
        if self.head is None or index < 0:
            return None

        node = self.head
        for _ in range(index):
            node = node.next

        # node is now at index
        return node.next.value   # get element at index+1
    def clear(self):
        self.head = None
        self.current = None



    def append(self, value):
        """Insert a new node *after* current, and make it the new current."""
        new_node = Node(value)
        # insert new_node after self.current
        new_node.next = self.current.next
        self.current.next = new_node
        # now current should point to the newly added node
        self.current = new_node

    def __str__(self):
        """Print starting from head, with current in parentheses."""
        if self.head is None:
            return "CircularBuffer()"

        items = []
        node = self.head
        first_loop = True

        while first_loop or node is not self.head:
            first_loop = False

            if node is self.current:
                items.append(f"({node.value})")
            else:
                items.append(str(node.value))

            node = node.next

        # two spaces between for readability, like your example
        return "  ".join(items)

    __repr__ = __str__



ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

@njit
def fast_part2(steps, N):
    pos = 0
    length = 1
    after_zero = None
    for value in range(1, N + 1):
        
        pos = (pos + steps) % length
        if pos == 0:
            after_zero = value
        pos += 1
        length += 1
    return after_zero


def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day16.txt')
   
   

    steps = 348

    buf = CircularBuffer(0)
   # buf.append(0)
    
    for i in range(2017):
        buf.move(steps)
        buf.append(i+1)
       # buf.move(1)
       # print(buf)

   
    print("Day 17 a = ", buf.current.next.value)

    print("Day 17 b = ", fast_part2(steps,50000000))
        



if __name__ == "__main__":
    main()
