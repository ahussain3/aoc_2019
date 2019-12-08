from enum import Enum
WIDTH = 25
HEIGHT = 6

def main():
    with open('day8_input.txt') as f:
        input = f.read()

        n = WIDTH * HEIGHT
        input = input.strip()
        layers = [input[i:i + n] for i in range(0, len(input), n)]

        collapsed = list(zip(*layers))
        result = []

        for pixel in collapsed:
            val = next(i for i in pixel if i != '2')
            if val == "0":
                result.append(" ")
            else:
                result.append("*")

        blah = [result[i:i+25] for i in range(0,150,25)]
        print("\n".join("".join(i) for i in blah))

main()

*     **  *   **  * ***
*    *  * *   **  * *  *
*    *     * * **** ***
*    * **   *  *  * *  *
*    *  *   *  *  * *  *
****  ***   *  *  * ***
