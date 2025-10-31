"""Day 4 solution."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

def is_duplicate_free(data):
    return len(data) == len(set(data))

def is_anagram_free(words):
    seen = set()
    for word in words:
        key = ''.join(sorted(word))  # canonical form
        if key in seen:
            return False  # found an anagram of a previous word
        seen.add(key)
    return True

def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day4.txt')

    valid = 0

    for line in lines:
        vector = list(line.split())
        if is_duplicate_free(vector):
            valid += 1
        
    print("Day 4 a = ",valid)

    valid =0
    for line in lines:
        vector = list(line.split())
        if is_anagram_free(vector):
            valid += 1
    
    print("Day 4 b = ",valid)
    


if __name__ == "__main__":
    main()
