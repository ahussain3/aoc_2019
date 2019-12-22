import time
from enum import Enum
from itertools import cycle

filename = "13.in"
DEBUG = False
REQ_INP = False

program = open(filename).read().strip("\n")

WIDTH = 40
HEIGHT = 26
SCREEN = [["." for i in range(WIDTH)] for j in range(HEIGHT)]

TILES = {
    0: ".",  # empty
    1: "#",  # wall
    2: "1",  # block
    3: "-",  # paddle
    4: "*",  # ball
}

def draw_tile(x, y, t):
    SCREEN[y][x] = TILES[t]

def print_screen():
    for j in range(HEIGHT):
        for i in range(WIDTH):
            print(SCREEN[j][i], end="")
        print("")
    print("".join(["-"]*WIDTH))

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
    global REQ_INP
    BASE = 0
    i = 0
    memory = list(map(int, program.split(","))) + [0] * 4096

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
        3 : {"name": "INP", "func": lambda a, b, c: write(a, (yield)), "width": 2},
        4 : {"name": "OUT", "func": lambda a, b, c: (yield a), "width": 2},
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

        if op == 3:
            REQ_INP = True

        result = task["func"](a, b, c)

        if op in {3, 4}:
            yield from result

        if op == 9:
            BASE = BASE + result
            if DEBUG:
                print("New Base", BASE)

        if op in {5, 6}:
            i = result
        else:
            i = i + task["width"]

        # if DEBUG:
        #     import time
        #     time.sleep(1)

def count_blocks():
    count = 0
    for j in range(HEIGHT):
        for i in range(WIDTH):
            if SCREEN[j][i] == "1":
                count = count + 1
    return count

def get_pos(symbol):
    """Assumes only one instance of the symbol on the board"""
    for j in range(HEIGHT):
        for i in range(WIDTH):
            if SCREEN[j][i] == symbol:
                return (i, j)
    return None


def get_best_move():
    paddle_pos = get_pos("-")
    ball_pos = get_pos("*")
    if ball_pos is None:
        return 0

    if paddle_pos[0] == ball_pos[0]:
        return 0
    if paddle_pos[0] < ball_pos[0]:
        return 1
    if paddle_pos[0] > ball_pos[0]:
        return -1


def main():
    global REQ_INP
    # print_program(program)

    computer = run()
    # raw_code = [i for i in computer]
    # n = 3
    # instructions = [raw_code[i:i + n] for i in range(0, len(raw_code), n)]
    def advance():
        next(computer)

    SCORE = 0
    i = 0
    while True:
        try:
            x = next(computer)
            if REQ_INP == True:
                x = computer.send(get_best_move())
                REQ_INP = False

            y = next(computer)
            t = next(computer)

            if x == -1 and y == 0:
                SCORE = t
            else:
                draw_tile(x, y, t)
        except StopIteration:
            break

    print_screen()
    print("Result", SCORE)

main()