import opcode
from pathlib import Path
import sys
import re
from collections import Counter, defaultdict
from turtle import pos

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from utils.file_parsers import read_lines

# -------------------------------------------------------------------
# Opcode functions
# -------------------------------------------------------------------

def addr(reg, inst): 
    r = reg.copy()
    r[inst[3]] = reg[inst[1]] + reg[inst[2]]
    return r

def addi(reg, inst):
    r = reg.copy()
    r[inst[3]] = reg[inst[1]] + inst[2]
    return r

def mulr(reg, inst):
    r = reg.copy()
    r[inst[3]] = reg[inst[1]] * reg[inst[2]]
    return r

def muli(reg, inst):
    r = reg.copy()
    r[inst[3]] = reg[inst[1]] * inst[2]
    return r

def banr(reg, inst):
    r = reg.copy()
    r[inst[3]] = reg[inst[1]] & reg[inst[2]]
    return r

def bani(reg, inst):
    r = reg.copy()
    r[inst[3]] = reg[inst[1]] & inst[2]
    return r

def borr(reg, inst):
    r = reg.copy()
    r[inst[3]] = reg[inst[1]] | reg[inst[2]]
    return r

def bori(reg, inst):
    r = reg.copy()
    r[inst[3]] = reg[inst[1]] | inst[2]
    return r

def setr(reg, inst):
    r = reg.copy()
    r[inst[3]] = reg[inst[1]]
    return r

def seti(reg, inst):
    r = reg.copy()
    r[inst[3]] = inst[1]
    return r

def gtir(reg, inst):
    r = reg.copy()
    r[inst[3]] = 1 if inst[1] > reg[inst[2]] else 0
    return r

def gtri(reg, inst):
    r = reg.copy()
    r[inst[3]] = 1 if reg[inst[1]] > inst[2] else 0
    return r

def gtrr(reg, inst):
    r = reg.copy()
    r[inst[3]] = 1 if reg[inst[1]] > reg[inst[2]] else 0
    return r

def eqir(reg, inst):
    r = reg.copy()
    r[inst[3]] = 1 if inst[1] == reg[inst[2]] else 0
    return r

def eqri(reg, inst):
    r = reg.copy()
    r[inst[3]] = 1 if reg[inst[1]] == inst[2] else 0
    return r

def eqrr(reg, inst):
    r = reg.copy()
    r[inst[3]] = 1 if reg[inst[1]] == reg[inst[2]] else 0
    return r


# A dictionary of all opcodes
OPCODES = {
    "addr": addr, "addi": addi,"mulr": mulr, "muli": muli,"banr": banr, "bani": bani,"borr": borr, "bori": bori,"setr": setr, "seti": seti,"gtir": gtir, "gtri": gtri, "gtrr": gtrr,
    "eqir": eqir, "eqri": eqri, "eqrr": eqrr
}

# -------------------------------------------------------------------
# Parsing helpers
# -------------------------------------------------------------------

def parse_before(line):
    return list(map(int, line[9:-1].split(",")))

def parse_after(line):
    return list(map(int, line[9:-1].split(",")))

def parse_inst(line):
    return list(map(int, line.split()))

def eliminate_opcode(possible, opcode_name, confirmed_id):
    for opcode_id, names in possible.items():
        if opcode_id != confirmed_id:
            names.discard(opcode_name)   # safe: no error if not present


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main():
    lines = read_lines(Path(__file__).resolve().parent / 'input/day16.txt')

    reg_bef, inst, reg_aft = [], [], []
    opcode_usage = Counter()
    program = []
    index = 0
    while index < len(lines):
        if lines[index] == "" and lines[index+1] == "":
            break
        reg_bef.append(parse_before(lines[index]))
        inst.append(parse_inst(lines[index+1]))
        reg_aft.append(parse_after(lines[index+2]))
        index += 4
    
    while index < len(lines):
        if lines[index] != "":
            program.append(parse_inst(lines[index]))
        index += 1


    totsamp = 0

    for before, instruction, after in zip(reg_bef, inst, reg_aft):
        matches = [name for name, opfunc in OPCODES.items() if opfunc(before, instruction) == after]
        for match in matches:
            opcode_usage[match] += 1
        if len(matches) >= 3:
            totsamp += 1

    print("Day 16 Part 1:", totsamp)
   # print(opcode_usage)

    possible = defaultdict(set)
    for before, instruction, after in zip(reg_bef, inst, reg_aft):
        opcode_id = instruction[0]
        for name, opfunc in OPCODES.items():
            if opfunc(before, instruction) == after:
                possible[opcode_id].add(name)

    found = set()

    while len(found) < len(OPCODES):
        progress = False
        for i in possible:
            if len(possible[i]) == 1 and i not in found:
                (opcode_name,) = possible[i]
             #   print(f"Found unique at {i} = {opcode_name}")
                eliminate_opcode(possible, opcode_name, i)
                found.add(i)
                progress = True
        if not progress:
            break

  #  for i in sorted(possible):
  #      print(i, possible[i])

    # possible[id] is a set with exactly one name
    opcode_impl = {}
    for opcode_id, names in possible.items():
        (name,) = names  # unpack single element from set
        opcode_impl[opcode_id] = OPCODES[name]


    regs = [0,0,0,0]

    for codeline in program:
        #print(codeline)
        opcode = codeline[0]
        func = opcode_impl[opcode]   # pick the right function for this ID
        regs = func(regs, codeline)


      #  print(possible[opcode])
  #  print("Final registers:", regs)
    print("Day 16 Part 2:", regs[0])


if __name__ == "__main__":
    main()
