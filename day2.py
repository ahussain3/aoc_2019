import sys
import itertools

code_raw = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,6,19,1,9,19,23,1,6,23,27,1,10,27,31,1,5,31,35,2,6,35,39,1,5,39,43,1,5,43,47,2,47,6,51,1,51,5,55,1,13,55,59,2,9,59,63,1,5,63,67,2,67,9,71,1,5,71,75,2,10,75,79,1,6,79,83,1,13,83,87,1,10,87,91,1,91,5,95,2,95,10,99,2,9,99,103,1,103,6,107,1,107,10,111,2,111,10,115,1,115,6,119,2,119,9,123,1,123,6,127,2,127,10,131,1,131,6,135,2,6,135,139,1,139,5,143,1,9,143,147,1,13,147,151,1,2,151,155,1,10,155,0,99,2,14,0,0"
memory = [int(v) for v in code_raw.split(",")]

def reset_memory():
    global memory
    memory = [int(v) for v in code_raw.split(",")]

def read(i):
    return memory[i]

def write(i, val):
    memory[i] = val

def go(noun, verb):
    reset_memory()
    memory[1] = noun
    memory[2] = verb

    i = 0
    while i < len(memory):
        op = memory[i]
        if op == 1:
            result = read(memory[i+1]) + read(memory[i+2])
            write(memory[i+3], result)
            i = i + 4
        elif op == 2:
            result = read(memory[i+1]) * read(memory[i+2])
            write(memory[i+3], result)
            i = i + 4
        elif op == 99:
            return memory[0]
        else:
            i = i + 1


def run():
    for noun, verb in itertools.product(range(100), range(100)):
        try:
            result = go(noun, verb)
        except:
            result = "FAILED"

        if result == 19690720:
            print(f"{noun}, {verb}")


if __name__ == "__main__":
    run()