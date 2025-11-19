from pathlib import Path
import sys
import threading
from queue import Queue, Empty
import time
from sympy import *

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def parse_instruction(s):
    parts = s.split()

    if len(parts) == 3:
        opcode, x, y = parts
        return opcode, x, y

    if len(parts) == 2:
        opcode, x = parts
        return opcode, x, None

    raise ValueError(f"Invalid instruction: {s}")


def is_int(s) -> bool:
    try:
        int(s)
        return True
    except (TypeError, ValueError):
        return False


def read_value(arg, registers) -> int:
    if arg is None:
        raise ValueError("read_value called with None")

    if is_int(arg):
        return int(arg)

    return registers.get(arg, 0)  # default 0 for unknown registers

def run_program(lines):
    registers: dict[str, int] = {}
    ip = 0
    num_mul = 0

    while 0 <= ip < len(lines):
        opcode, x, y = parse_instruction(lines[ip])
  #      print(opcode, x, y)
        if opcode == "set":
            registers[x] = read_value(y, registers)

        elif opcode == "sub":
            registers[x] = registers.get(x, 0) - read_value(y, registers)

        elif opcode == "mul":
            registers[x] = registers.get(x, 0) * read_value(y, registers)
            num_mul += 1

        elif opcode == "jnz":
            if read_value(x, registers) != 0:
                ip += read_value(y, registers)
                continue

        # Normal instruction flow
        ip += 1

    return num_mul

def run_programb(lines):
    b=108400 #starting values
    c=125400
    h = 0
    for i in range(b,c+1,17):
        if(isprime(i) == False):
            h+=1

    return h
#    print(f"b={b},c={c}")

    



def main():
    lines = read_lines(Path(__file__).resolve().parent / "input/day23.txt")

    ans = run_program(lines)

    
    
    print("Day 23 a = ", ans)

    ans2 = run_programb(lines)

    print("Day 23 b = ", ans2)


if __name__ == "__main__":
    main()
