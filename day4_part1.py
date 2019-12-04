from typing import Tuple

# input = [111111, 223450, 123789]

input = range(284639, 748759)

def is_valid(password: int) -> Tuple[bool, str]:
    pw = str(password)
    if len(pw) != 6:
        return False, "Not 6 digits"

    for x, y in zip(pw[1:], pw[:-1]):
        if x == y:
            break
    else:
        return False, "No duplicated digit"

    for x, y in zip("0" + pw, pw + "9"):
        if int(y) < int(x):
            return False, "Not monotonically increasing"

    return True, "OK"

def run():
    count_good_pws = 0
    count_total_pws = len(input)

    for i, password in enumerate(input):
        if i % 10_000 == 0:
            print(f"{i}/{count_total_pws} checked")

        is_ok, reason = is_valid(password)
        if is_ok:
            count_good_pws = count_good_pws + 1

    print(f"{count_good_pws} out of {count_total_pws} are good.")

if __name__ == "__main__":
    run()