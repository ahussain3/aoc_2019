from enum import Enum

filename = "9.in"
DEBUG = False

# program = "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
# program = "1102,34915192,34915192,7,4,7,99,0"
# program = "104,1125899906842624,99"

program = open(filename).read().strip("\n")
memory = list(map(int, program.strip().split(','))) + [0]*4096

def print_program(program):
    line_numbers = [str(i).rjust(len(p)) for i, p in enumerate(program.strip().split(','))]
    for i in line_numbers:
        print(i, end=", ")
    print("")

    for i, p in enumerate(program.strip().split(',')):
        print(str(p).rjust(len(str(i))), end=", ")
    print("\n")

class ParamMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2

def run():
    BASE = 0
    i = 0
    # memory = list(map(int, program.split(","))) + [0] * 4096

    def read(i:int, mode:ParamMode = ParamMode.POSITION.value):
        if mode == ParamMode.POSITION.value:
            return memory[memory[i]]
        elif mode == ParamMode.RELATIVE.value:
            return memory[memory[i] + BASE]
        elif mode == ParamMode.IMMEDIATE.value:
            return memory[i]
        else:
            assert False, f"Unrecognized param mode: {mode}"

    def write(i, val):
        if DEBUG:
            print(f"Wrote value {val} to position {i}")
        memory[i] = val

    opcodes = {
        1 : {"name": "ADD", "func": lambda a, b, c: write(c, a + b), "width": 4},
        2 : {"name": "MUL", "func": lambda a, b, c: write(c, a * b), "width": 4},
        3 : {"name": "INP", "func": lambda a, b, c: write(a, int(input("Please provide an integer input: "))), "width": 2},
        4 : {"name": "OUT", "func": lambda a, b, c: print("Output:", a), "width": 2},
        5 : {"name": "JMP-T", "func": lambda a, b, c: b if a != 0 else i + 3, "width": 3},
        6 : {"name": "JMP-F", "func": lambda a, b, c: b if a == 0 else i + 3, "width": 3},
        7 : {"name": "LES", "func": lambda a, b, c: write(c, 1 if a < b else 0), "width": 4},
        8 : {"name": "EQ", "func": lambda a, b, c: write(c, 1 if a == b else 0), "width": 4},
        9 : {"name": "BASE", "func": lambda a, b, c: a, "width": 2},
    }

    while memory[i] != 99:
        raw = str(memory[i]).rjust(5, "0")
        op = int(raw[3:])
        p1_mode = int(raw[2])
        p2_mode = int(raw[1])
        p3_mode = int(raw[0])
        task = opcodes[op]

        a, b, c = None, None, None

        if task["width"] > 1:
            a = read(i+1, p1_mode)
        if task["width"] > 2:
            b = read(i+2, p2_mode)
        if task["width"] > 3:
            c = read(i+3, p3_mode)

        # Write params
        if op in {1, 2, 7, 8}:
            c = memory[i+3] + BASE if p3_mode == 2 else memory[i+3]
        if op in {3}:
            a = memory[i+1] + BASE if p1_mode == 2 else memory[i+1]

        if DEBUG:
            print(f"{i}:", raw, task["name"], a, b, c)

        result = task["func"](a, b, c)

        if op == 9:
            BASE = BASE + result
            if DEBUG:
                print("New Base", BASE)

        if op in {5, 6}:
            i = result
        else:
            i = i + task["width"]

        if DEBUG:
            import time
            time.sleep(1)

def main():
    print_program(program)
    run()

main()