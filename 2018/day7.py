
from itertools import count
from pathlib import Path
from pickletools import read_decimalnl_short
import sys
from collections import defaultdict
from collections import Counter

from datetime import datetime, date, time
import re

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines



def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day7test.txt')
    
    transitions = defaultdict(list)   # step -> list of next steps
    prereq = defaultdict(set)         # step -> set of prerequisite steps
    all_steps = set()

    # Build graph
    for line in lines:
        a = line.split(" ")
        s1 = a[1]
        s2 = a[7]

        transitions[s1].append(s2)
        prereq[s2].add(s1)

        all_steps.add(s1)
        all_steps.add(s2)

    # Ensure every step exists in prereq (even if it has no prereqs)
    for step in all_steps:
        prereq.setdefault(step, set())

    # Steps with no prerequisites are initially available
    available = sorted([s for s in all_steps if not prereq[s]])

    restr = ""

    # While there are steps you can still do
    while available:
        # Pick alphabetically first available step
        step = available.pop(0)
        restr += step

        # For each step unlocked by 'step'
        for nxt in transitions[step]:
            # Remove this prerequisite
            if step in prereq[nxt]:
                prereq[nxt].remove(step)
            # If no more prereqs, it becomes available
            if not prereq[nxt]:
                if nxt not in available and nxt not in restr:
                    available.append(nxt)

        # Keep available alphabetically sorted
        available.sort()

    print("Day 7 a =", restr)
    print("Day 7 b =", 0)
    
if __name__ == "__main__":
    main()
