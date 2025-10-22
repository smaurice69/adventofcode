"""Day 1 solution."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def main():
    """Run the Day 1 solution."""
    lines = read_lines(Path(__file__).resolve().parent / 'input/day1test.txt')
    print(lines)


if __name__ == "__main__":
    main()
