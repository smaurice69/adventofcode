"""Day 8 solution."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day8test.txt')
    registers = {}

    for line in lines:
        vector = list(line.split())
        # set register
        print(vector[0])
        registers[vector[0]] = 0

        # vector[0] = register
        # vector[1] = inc or dec
        # vector[2] = # of inc/dec
        # vector[3] = "if"
        # vector[4] = register
        # vector[5] = >, <, != == etc
        # vector[6] = value to compare with

    for line in lines:
        vector = list(line.split())

        reg_to_change = vector[0]
        reg_to_compare = vector[4]
        a = vector[5]
        if a == "==":
            print("inside a ==")
            if reg_to_compare == vector[6]:
                if vector[1] == "dec":
                    print("inside a dec")
                    registers[reg_to_change] -= vector[2]
                elif vector[1] == "inc":
                    print("inside a inc")
                    registers[reg_to_change] += vector[2]



        if vector[3] != "if":
            print("Error if")
        if vector[1] != "dec" and vector[1] != "inc":
            print("Error dec/inc")



    print ("Day 2 a = ", 0)

    print(registers)

    lines = read_lines(Path(__file__).resolve().parent / 'input/day2.txt')



if __name__ == "__main__":
    main()
