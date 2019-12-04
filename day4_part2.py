from typing import List, Tuple

# input = [111111, 223450, 123789, 112233, 123444, 111122]

input = range(284639, 748759)

def parse_groups(password: str) -> List[str]:
    groups = []
    group = password[0]
    for x, y in zip(password[1:], password[:-1]):
        if x == y:
            group = group + x
        else:
            groups.append(group)
            group = x

    groups.append(group)
    return groups


def is_valid(password: str) -> Tuple[bool, str]:
    if len(password) != 6:
        return False, "Not 6 digits"

    for x, y in zip("0" + password, password + "9"):
        if int(y) < int(x):
            return False, "Not monotonically increasing"

    groups = parse_groups(password)
    if any(len(group) == 2 for group in groups):
        return True, "OK"
    elif all(len(group) == 1 for group in groups):
        return False, "No duplicated digit"
    else:
        return False, "Repeated digit is part of a larger group"

    return True, "OK"

def run():
    count_good_pws = 0
    count_total_pws = len(input)

    for i, password in enumerate(input):
        # if i % 10_000 == 0:
        #     print(f"{i}/{count_total_pws} checked")

        is_ok, reason = is_valid(str(password))
        # print(f"{password}: {reason}")
        if is_ok:
            count_good_pws = count_good_pws + 1

    print(f"{count_good_pws} out of {count_total_pws} are good.")

if __name__ == "__main__":
    # import pdb; pdb.set_trace()
    run()