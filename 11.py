from enum import Enum
from itertools import cycle

filename = "11.in"
DEBUG = False

program = open(filename).read().strip("\n")

WIDTH = 120
HEIGHT = 60
HULL = [[{"val": ".", "count": 0} for i in range(WIDTH)] for j in range(HEIGHT)]
ROBOT = (60, 30, '^')

def print_hull():
    for j in range(HEIGHT):
        for i in range(WIDTH):
            rx, ry, rdir = ROBOT
            if rx == i and ry == j:
                print(rdir, end="")
            else:
                print(HULL[j][i]["val"], end="")
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

        if DEBUG:
            import time
            time.sleep(1)

def paint_hull(color):
    global ROBOT
    x, y, _ = ROBOT
    assert color in {0, 1}
    HULL[y][x]["val"] = "#" if color == 1 else "."
    HULL[y][x]["count"] = HULL[y][x]["count"] + 1

MOVE_BY = {
    "^": (0, -1),
    "v": (0, +1),
    "<": (-1, 0),
    ">": (+1, 0),
}

def change_direction(direction):
    global ROBOT
    x, y, dir = ROBOT

    if direction == 1:
        loop = "^>v<^"
    elif direction == 0:
        loop = "^<v>^"
    else:
        assert False, "Direction must be 0 or 1"

    new_dir = loop[loop.index(dir) + 1]
    i, j = MOVE_BY[new_dir]
    ROBOT = (x + i, y + j, new_dir)

def get_color_under_robot():
    global ROBOT
    x, y, _ = ROBOT
    val = HULL[y][x]["val"]
    assert val in {".", "#"}
    return 0 if val == "." else 1

def count_cells():
    total = 0
    for j in range(HEIGHT):
        for i in range(WIDTH):
            if HULL[j][i]["count"] > 0:
                total = total + 1
    return total

def main():
    # print_program(program)

    paint_hull(1)
    computer = run()
    next(computer)
    while True:
        try:
            input = get_color_under_robot()
            color = computer.send(input)
            paint_hull(color)
            direction = next(computer)
            change_direction(direction)
            print(ROBOT)
            next(computer)
        except StopIteration:
            print("FINISHED")
            break

    print_hull()
    print(count_cells())

main()

####.###..####.###..#..#.####.####.###.....................
...#.#..#....#.#..#.#.#..#.......#.#..#....................
..#..#..#...#..#..#.##...###....#..#..#....................
.#...###...#...###..#.#..#.....#...###.....................
#....#.#..#....#....#.#..#....#....#.#..>..................
####.#..#.####.#....#..#.####.####.#..#....................