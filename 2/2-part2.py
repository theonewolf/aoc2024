#!/usr/bin/env python3

def check_level(level):
    level2 = level[1:]
    diffs = [a - b for a,b in zip(level, level2)]
    absdiffs = [abs(a - b) for a,b in zip(level, level2)]

    if not (all(diff > 0 for diff in diffs) or all(diff < 0 for diff in diffs)): return False
    if not (max(absdiffs) <= 3 and min(absdiffs) >= 1): return False

    return True


if __name__ == '__main__':
    with open('input') as fd:
        safe = 0
        for line in fd:
            numbers = [int(i) for i in line.split()]
            numbers2 = numbers[1:]

            if check_level(numbers): safe += 1
            else:
                for i in range(len(numbers)):
                    numbers_copy = numbers[:]
                    del numbers_copy[i]
                    if check_level(numbers_copy):
                        safe += 1
                        break


        print(safe)
