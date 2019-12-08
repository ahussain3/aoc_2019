from enum import Enum
WIDTH = 25
HEIGHT = 6

def main():
    with open('day8_input.txt') as f:
        input = f.read()

        n = WIDTH * HEIGHT
        input = input.strip()
        layers = [input[i:i + n] for i in range(0, len(input), n)]

        layer = min(layers, key=lambda l: l.count('0'))
        print(layer.count('1') * layer.count('2'))

main()