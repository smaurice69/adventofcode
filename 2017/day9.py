"""Day 9 solution."""

from pathlib import Path
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

import re

def remove_between(s: str, start: str, end: str) -> tuple[str, int]:
    """
    Remove all text between 'start' and 'end' (non-greedy),
    returning (clean_string, total_inner_chars_removed).

    total_inner_chars_removed sums ONLY the characters INSIDE the delimiters,
    i.e., for each '<...>' counts len(...) not including '<' or '>'.
    """
    pattern = re.escape(start) + r".*?" + re.escape(end)
    matches = list(re.finditer(pattern, s))
    # characters inside each pair (exclude start/end themselves)
    inner_removed = sum(len(m.group(0)) - 2 for m in matches)
    new_s = re.sub(pattern, "", s)
    return new_s, inner_removed

def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day9.txt')
    line = lines[0]
    # 1) remove canceled characters: '!' plus the next char
    new_line = []
    i = 0
    n = len(line)
    while i < n:
        if line[i] == "!":
            i += 2  # skip '!' and the following character
        else:
            new_line.append(line[i])
            i += 1
    new_line = "".join(new_line)

    # 2) remove garbage sections and count inner garbage characters
    cleaned, garbage_count = remove_between(new_line, "<", ">")

    # 3) score groups in the cleaned stream
    score = 0
    depth = 0
    for ch in cleaned:
        if ch == "{":
            depth += 1
            score += depth
        elif ch == "}":
            depth -= 1
            # (optional) sanity guard: depth should never go negative

    print("Day 9 a =", score)  # total group score
    print("Day 9 b =", garbage_count)  # total non-canceled garbage chars


if __name__ == "__main__":
    main()
