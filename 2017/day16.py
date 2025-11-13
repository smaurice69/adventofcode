"""Day 16 solution."""
import copy
import numbers
from pathlib import Path
import string
import sys
import re
from collections import deque
import numpy as np
from numba import njit




ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


class IndexedCircularBuffer:
    """A circular buffer with 16 unique single-character elements."""

    def __init__(self, max_size=16):
        self.max_size = max_size
        self.buffer = [None] * max_size
        self.head = 0
        self.tail = 0
        self.count = 0
        self.char_to_index = {}

    def __len__(self):
        return self.count

    #def __str__(self):
        ##return "[" + ", ".join(
        #return "" + "".join(
            #str(self.buffer[(self.head + i) % self.max_size])
            #for i in range(self.count)
        #) + ""
    
    def state(self) -> str:
        # logical order from head
        return "".join(self.buffer[(self.head + i) % self.max_size] for i in range(self.count))

    def __str__(self):
        return self.state()



    def __contains__(self, item):
        return item in self.char_to_index

    def is_full(self):
        return self.count == self.max_size

    def is_empty(self):
        return self.count == 0

    def enqueue(self, char):
        """Add a unique single-character element to the buffer."""
        if self.is_full():
            raise OverflowError("Buffer is full.")
        if not isinstance(char, str) or len(char) != 1:
            raise ValueError("Only single-character strings are allowed.")
        if char in self.char_to_index:
            raise ValueError(f"Character '{char}' already exists in buffer.")

        self.buffer[self.tail] = char
        self.char_to_index[char] = self.tail
        self.tail = (self.tail + 1) % self.max_size
        self.count += 1

    def dequeue(self):
        """Remove and return the front element."""
        if self.is_empty():
            raise IndexError("Buffer is empty.")

        char = self.buffer[self.head]
        self.buffer[self.head] = None
        del self.char_to_index[char]
        self.head = (self.head + 1) % self.max_size
        self.count -= 1
        return char

    def __getitem__(self, key):
        """Access by index or by content (character)."""
        if isinstance(key, int):
            if key < 0 or key >= self.count:
                raise IndexError("Index out of range.")
            return self.buffer[(self.head + key) % self.max_size]
        elif isinstance(key, str) and len(key) == 1:
            if key not in self.char_to_index:
                raise KeyError(f"Character '{key}' not found.")
            return self.char_to_index[key]
        else:
            raise TypeError("Key must be an int (index) or single-character str.")

    def __iter__(self):
        for i in range(self.count):
            yield self.buffer[(self.head + i) % self.max_size]


# -------------------------------
    # NEW METHODS
    # -------------------------------
    def SwapPartner(self, a, b):
        """Swap the positions of characters a and b."""
        if a not in self.char_to_index or b not in self.char_to_index:
            raise KeyError("Both characters must exist in buffer.")

        idx_a = self.char_to_index[a]
        idx_b = self.char_to_index[b]

        # Swap in buffer
        self.buffer[idx_a], self.buffer[idx_b] = self.buffer[idx_b], self.buffer[idx_a]

        # Update lookup
        self.char_to_index[a], self.char_to_index[b] = idx_b, idx_a

    def Exchange(self, i, j):
        """Swap the characters at logical positions i and j."""
        if not (0 <= i < self.count) or not (0 <= j < self.count):
            raise IndexError("Indices out of range.")

        real_i = (self.head + i) % self.max_size
        real_j = (self.head + j) % self.max_size

        char_i, char_j = self.buffer[real_i], self.buffer[real_j]

        # Swap in buffer
        self.buffer[real_i], self.buffer[real_j] = char_j, char_i

        # Update lookup
        if char_i is not None:
            self.char_to_index[char_i] = real_j
        if char_j is not None:
            self.char_to_index[char_j] = real_i

    def Spin(self, n):
        """Move the start of the list n items backward (rotate right)."""
        if self.is_empty():
            return
        n = n % self.count  # normalize
        self.head = (self.head - n) % self.max_size
        self.tail = (self.head + self.count) % self.max_size


def process_code(buf: IndexedCircularBuffer, items: list[str]) -> IndexedCircularBuffer:
    for cmd in items:
        new_string = cmd[1:]
        if cmd[0] == 's':
            buf.Spin(int(new_string))
        elif cmd[0] == 'x':
            a, b = new_string.split('/')
            buf.Exchange(int(a), int(b))
        elif cmd[0] == 'p':
            a, b = new_string.split('/')
            buf.SwapPartner(a, b)
        else:
            raise ValueError(f"Unknown command: {cmd}")
    return buf

def detect_cycle_and_compute(buf: IndexedCircularBuffer, items: list[str], total_iters: int) -> str:
    seen = {}  # state -> iteration index
    order = [] # list of states in order

    # initial state
    s = buf.state()
    seen[s] = 0
    order.append(s)

    # advance until we see a repeat
    while True:
        process_code(buf, items)
        s = buf.state()
        if s in seen:
            start = seen[s]          # where the cycle starts in 'order'
            cycle_len = len(order) - start
            break
        seen[s] = len(order)
        order.append(s)

    # total_iters applications from the very beginning:
    if total_iters < len(order):
        return order[total_iters]

    # Skip the pre-period (start), then mod by cycle length
    if total_iters < start:
        return order[total_iters]
    else:
        offset_in_cycle = (total_iters - start) % cycle_len
        return order[start + offset_in_cycle]


def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day16.txt')
    items = list(lines[0].split(","))


    


    buf = IndexedCircularBuffer(max_size=16)

    for c in "abcdefghijklmnop":
        buf.enqueue(c)

    iter1 = process_code(buf,items)
   
    print("day 16 a = ", iter1)

    iter1orig = copy.copy(iter1)

   

    buf = IndexedCircularBuffer(max_size=16)
    for c in "abcdefghijklmnop":
        buf.enqueue(c)

    target = 1_000_000_000
    result = detect_cycle_and_compute(buf, items, target)
    print("Day 16 b =", result)

    
    


if __name__ == "__main__":
    main()
