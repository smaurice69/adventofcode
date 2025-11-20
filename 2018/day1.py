
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines



def main():
    """Run the Day 1 solution."""
    lines = read_lines(Path(__file__).resolve().parent / 'input/day1.txt')

    # Convert once
    nums = [int(x) for x in lines]

    # Part 1
    freq = sum(nums)
    print("Day 1 a =", freq)

    # Part 2
    seen = {0}
    curfreq = 0
    index = 0
    totidx = 0
    while True:
        curfreq += nums[index]
        if curfreq in seen:
            print("Day 1 b =", curfreq)
            break
        seen.add(curfreq)
        index += 1
        if index == len(nums):
            index = 0
    
if __name__ == "__main__":
    main()
