from pathlib import Path
import sys
import threading
from queue import Queue, Empty
import time

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
    last_sound = None

    while 0 <= ip < len(lines):
        opcode, x, y = parse_instruction(lines[ip])

        if opcode == "set":
            registers[x] = read_value(y, registers)

        elif opcode == "add":
            registers[x] = registers.get(x, 0) + read_value(y, registers)

        elif opcode == "mul":
            registers[x] = registers.get(x, 0) * read_value(y, registers)

        elif opcode == "mod":
            registers[x] = registers.get(x, 0) % read_value(y, registers)

        elif opcode == "snd":
            last_sound = read_value(x, registers)

        elif opcode == "rcv":
            if read_value(x, registers) != 0:
                # Recover last sound and halt
                return last_sound

        elif opcode == "jgz":
            if read_value(x, registers) > 0:
                ip += read_value(y, registers)
                continue

        # Normal instruction flow
        ip += 1

    return last_sound




def main():
    lines = read_lines(Path(__file__).resolve().parent / "input/day18.txt")

    last_sound = run_program(lines)

    print("Day 18 a = ", last_sound)
    
    inbox_a = Queue()
    inbox_b = Queue()
    reg_a: dict[str, int] = {}
    reg_b: dict[str, int] = {}
    
    reg_a['p'] = 0 # program ID
    reg_b['p'] = 1 

    ip_a = 0
    ip_b = 0
    wait_a = False
    wait_b = False
    sendcount_A = 0
    sendcount_B = 0
    
    while not (wait_a and wait_b):
        opcode_a, x_a, y_a = parse_instruction(lines[ip_a])
        opcode_b, x_b, y_b = parse_instruction(lines[ip_b])

            
        if opcode_a == "snd":
            msg_out = read_value(x_a, reg_a)
            inbox_b.put(msg_out)
            sendcount_A += 1
          #  print("Message ", msg_out, " sent from 0 to 1")
            ip_a += 1
        elif opcode_a == "rcv":
            if inbox_a.empty() == True:
                wait_a = True
         #       print("Still waiting A")                
            else:
                wait_a = False
                msg_in = inbox_a.get()
                reg_a[x_a] = msg_in
                ip_a += 1
        
        elif opcode_a == "set":
            reg_a[x_a] = read_value(y_a, reg_a)
            ip_a += 1
        elif opcode_a == "add":
            reg_a[x_a] = reg_a.get(x_a, 0) + read_value(y_a, reg_a)
            ip_a += 1
        elif opcode_a == "mul":
            reg_a[x_a] = reg_a.get(x_a, 0) * read_value(y_a, reg_a)
            ip_a += 1
        elif opcode_a == "mod":
            reg_a[x_a] = reg_a.get(x_a, 0) % read_value(y_a, reg_a)
            ip_a += 1
        elif opcode_a == "jgz":
            if read_value(x_a, reg_a) > 0:
                ip_a += read_value(y_a, reg_a)
            else:
                ip_a += 1


        if opcode_b == "snd":
            msg_out = read_value(x_b, reg_b)
            inbox_a.put(msg_out)
            sendcount_B += 1
       #     print("Message ", msg_out, " sent from 1 to 0")
            ip_b += 1
        elif opcode_b == "rcv":
            if inbox_b.empty() == True:
                wait_b = True
            #    print("Still waiting B")
            else:
                wait_b = False
                msg_in = inbox_b.get()
                reg_b[x_b] = msg_in
                ip_b += 1        
        elif opcode_b == "set":
            reg_b[x_b] = read_value(y_b, reg_b)
            ip_b += 1
        elif opcode_b == "add":
            reg_b[x_b] = reg_b.get(x_b, 0) + read_value(y_b, reg_b)
            ip_b += 1
        elif opcode_b == "mul":
            reg_b[x_b] = reg_b.get(x_b, 0) * read_value(y_b, reg_b)
            ip_b += 1
        elif opcode_b == "mod":
            reg_b[x_b] = reg_b.get(x_b, 0) % read_value(y_b, reg_b)
            ip_b += 1
        elif opcode_b == "jgz":
            if read_value(x_b, reg_b) > 0:
                ip_b += read_value(y_b, reg_b)   
            else:
                ip_b += 1

    
    print("Day 18 b = ", sendcount_B)


if __name__ == "__main__":
    main()
