"""Day 16 solution."""
import copy
import numbers
from pathlib import Path
import sys
import re
from collections import deque



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

    def __str__(self):
        return "[" + ", ".join(
            str(self.buffer[(self.head + i) % self.max_size])
            for i in range(self.count)
        ) + "]"

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


def main():
   # lines = read_lines(Path(__file__).resolve().parent / 'input/day13.txt')

    buf = IndexedCircularBuffer(max_size=5)

    for c in "abcde": #"abcdefghijklmnop":
        buf.enqueue(c)

    buf.Spin(1)
    buf.Exchange(3,4)
    buf.SwapPartner('e','b')

    print(buf)
    print("Day 15 a = ", 0)

    print("Day 15 b = ", 0)

    


if __name__ == "__main__":
    main()
