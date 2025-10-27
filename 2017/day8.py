"""Day 8 solution."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines


def main():

    lines = read_lines(Path(__file__).resolve().parent / 'input/day8.txt')
    registers = {}
    global_max = 0

    for line in lines:
        vector = list(line.split())
        # set register
     #   print(vector[0])
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
        condition = False
        the_val = int(registers[vector[4]])
        the_comp = int(vector[6])
        if a == "==":
            if the_val == the_comp:
                condition = True
        elif a == ">":
            if the_val   > the_comp:
                condition = True
        elif a == "<":
            if the_val < the_comp:
                condition = True
        elif a == "<=":
            if the_val <= the_comp:
                condition = True
        elif a == ">=":
            if the_val >= the_comp:
                condition = True
        elif a == "!=":
            if the_val != the_comp:
                condition = True
        else:
            print("unknown operator")
            break
        if condition == True:
            if(vector[1] == "inc"):
                registers[reg_to_change] += int(vector[2])
            else:
                registers[reg_to_change] -= int(vector[2])
        if(max(registers.values()) > global_max):
            global_max = max(registers.values())


    print ("Day 8 a = ", max(registers.values()))
    print("Day 8 b = ", global_max)

    # print(registers)

    lines = read_lines(Path(__file__).resolve().parent / 'input/day2.txt')



if __name__ == "__main__":
    main()
