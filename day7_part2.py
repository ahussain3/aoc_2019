import sys
import itertools
from enum import Enum

# program = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
# signal = [4,3,2,1,0]

# program = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
# signal = [0,1,2,3,4]

# program = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
# signal = [1,0,4,3,2]

program = "3,8,1001,8,10,8,105,1,0,0,21,38,47,64,89,110,191,272,353,434,99999,3,9,101,4,9,9,102,3,9,9,101,5,9,9,4,9,99,3,9,1002,9,5,9,4,9,99,3,9,101,2,9,9,102,5,9,9,1001,9,5,9,4,9,99,3,9,1001,9,5,9,102,4,9,9,1001,9,5,9,1002,9,2,9,1001,9,3,9,4,9,99,3,9,102,2,9,9,101,4,9,9,1002,9,4,9,1001,9,4,9,4,9,99,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,99"

#           "0, 1,   2, 3, 4, 5,6, 7,  8,  9,10,11,12,13,14,15,16,17,  18,19,20,21,  22,23,24,25,26 27,28"
# program = "3,26,1001,26,-4,26,3,27,1002,27, 2,27, 1,27,26,27, 4,27,1001,28,-1,28,1005,28, 6,99, 5, 5, 5"

# program="3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"

# program = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"

class ParamMode(Enum):
    POSITION = 0
    IMMEDIATE = 1

def run(name):
    i = 0
    memory = [int(v) for v in program.split(",")]

    def read(i:int, mode:ParamMode = ParamMode.POSITION.value):
        if mode == ParamMode.POSITION.value:
            return memory[i]
        elif mode == ParamMode.IMMEDIATE.value:
            return i
        else:
            assert False, f"Unrecognized param mode: {mode}"

    def write(i, val):
        memory[i] = val

    while i < len(memory):
        raw = str(memory[i]).rjust(5, "0")
        op = int(raw[3:])
        p1_mode = int(raw[2])
        p2_mode = int(raw[1])
        p3_mode = int(raw[0])

        # So ugly; I apologise. Will clean up later.
        if op == 1:  # add
            result = read(memory[i+1], p1_mode) + read(memory[i+2], p2_mode)
            write(memory[i+3], result)
            i = i + 4
        elif op == 2:  # multiply
            result = read(memory[i+1], p1_mode) * read(memory[i+2], p2_mode)
            write(memory[i+3], result)
            i = i + 4
        elif op == 3:  # input
            result = (yield)
            # print(f"({name}) Requested Input, recieved:", result)
            write(memory[i+1], int(result))
            i = i + 2
        elif op == 4:  # output
            # print(f"({name}) Output:", read(memory[i+1], p1_mode))
            # print(f"({name}) Counter:", memory[-1])
            yield read(memory[i+1], p1_mode)
            i = i + 2
        elif op == 5: # jump-if-true
            signal = read(memory[i+1], p1_mode)
            if signal != 0:
                i = read(memory[i+2], p2_mode)
            else:
                i = i + 3
        elif op == 6: # jump-if-false
            signal = read(memory[i+1], p1_mode)
            if signal == 0:
                i = read(memory[i+2], p2_mode)
            else:
                i = i + 3
        elif op == 7: # less than
            if read(memory[i+1], p1_mode) < read(memory[i+2], p2_mode):
                write(read(memory[i+3], 1), 1)
            else:
                write(read(memory[i+3], 1), 0)
            i = i + 4
        elif op == 8: # equals
            if read(memory[i+1], p1_mode) == read(memory[i+2], p2_mode):
                write(read(memory[i+3], 1), 1)
            else:
                write(read(memory[i+3], 1), 0)
            i = i + 4
        elif op == 99:
            # print("PROGRAM FINISHED!")
            return
        else:
            i = i + 1
    print("I ESCAPED THE WHILE LOOP!")

if __name__ == "__main__":
    max_thrust = 0
    answer = None

    for signal in itertools.permutations([5,6,7,8,9]):
        print(signal)
        try:
            computers = [run("a"), run("b"), run("c"), run("d"), run("e")]

            carry = 0

            for i, computer in enumerate(computers):
                next(computer)
                computer.send(signal[i])

            for computer in computers:
                out = computer.send(carry)
                carry = out

            for computer in itertools.cycle(computers):
                next(computer)
                out = computer.send(carry)
                carry = out

        except StopIteration:
            print(out)
            if out > max_thrust:
                max_thrust = out
                answer = signal
            continue

    print("Max Thrust", max_thrust)
    print("Answer", answer)


