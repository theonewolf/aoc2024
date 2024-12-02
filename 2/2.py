#!/usr/bin/env python3

if __name__ == '__main__':
    with open('input') as fd:
        safe = 0
        for line in fd:
            numbers = [int(i) for i in line.split()]
            numbers2 = numbers[1:]

            diffs = [a - b for a,b in zip(numbers, numbers2)]
            absdiffs = [abs(a - b) for a,b in zip(numbers, numbers2)]

            if not (all(diff > 0 for diff in diffs) or all(diff < 0 for diff in diffs)): continue

            if not (max(absdiffs) <= 3 and min(absdiffs) >= 1): continue

            safe += 1

        print(safe)
