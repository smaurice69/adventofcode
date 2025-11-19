from itertools import count
from pathlib import Path
from sqlite3 import Cursor
import sys

#import threading
#from queue import Queue, Empty
#import time
#from collections import defaultdict
#from functools import lru_cache
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

import re
from pprint import pprint

def parse_state_machine(text: str):
    # Split into state blocks
    blocks = re.split(r"\bIn state ([A-Z]):\s*", text)[1:]  # First element is empty before first match

    # blocks is like: ["A", "  If the current value...", "B", "  If the current value...", ...]
    # So pair them: (state_name, block_text)
    states = {blocks[i]: blocks[i+1] for i in range(0, len(blocks), 2)}

    machine = {}

    for state, block in states.items():
        transitions = {}
        
        # Find each "If the current value is X:" block
        cases = re.split(r"If the current value is ([01]):", block)[1:]
        # cases = ["0", "instructions...", "1", "instructions..."]

        for i in range(0, len(cases), 2):
            current_value = int(cases[i])
            instructions = cases[i+1]

            # Extract write instruction
            write_match = re.search(r"Write the value (\d)", instructions)
            write_val = int(write_match.group(1)) if write_match else None

            # Extract move direction
            move_match = re.search(r"Move one slot to the (right|left)", instructions)
            move = move_match.group(1) if move_match else None

            # Extract next state
            next_match = re.search(r"Continue with state ([A-Z])", instructions)
            next_state = next_match.group(1) if next_match else None

            transitions[current_value] = {
                "write": write_val,
                "move": move,
                "next": next_state
            }

        machine[state] = transitions

    return machine

def print_tape(tape, cursor, start=-10, end=10):
    """
    Print values on the tape from index start to end (inclusive),
    marking the cursor position with [value].
    """
    output = []

    for i in range(start, end + 1):
        val = tape[i]
        if i == cursor:
            output.append(f"[{val}]")
        else:
            output.append(str(val))

    print(" ".join(output))



def main():

        lines = read_lines(Path(__file__).resolve().parent / "input/day25.txt")

      #  print(lines[3:])

        #parsed = parse_state_machine(lines[3:])
        curstate = lines[0][-2]
        line2 = lines[1].split(" ")
        checksumcnt = int(line2[5])
        parsed = parse_state_machine("".join(lines[3:]))
        tape = defaultdict(int)
        cursorindex = 0
       # print_tape(tape, cursorindex)
        for i in range(checksumcnt):
        #    if(i%100000 == 0):
         #       print(float(i)/float(checksumcnt))
            write_value = parsed[curstate][tape[cursorindex]]["write"]
            move = 1 if parsed[curstate][tape[cursorindex]]["move"] == "right" else -1
            next_state = parsed[curstate][tape[cursorindex]]["next"]            
            
            tape[cursorindex] = write_value
            
            cursorindex += move
            curstate = next_state
            
         #   print_tape(tape,cursorindex)

        count_ones = sum(1 for v in tape.values() if v == 1)


        #print(parsed)

        print("Day 25 a = ", count_ones)

if __name__ == "__main__":
    main()
