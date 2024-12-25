#!/usr/bin/env python3

def compute_heights(grid):
    target = '.'
    heights = [None] * len(grid[0])

    if '#' not in grid[0]:
        target = '#'

    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == target and heights[j] is None:
                heights[j] = i - 1

                if target == '#':
                    heights[j] = len(grid) - heights[j] - 2

    return heights

def fit(key, lock, maxtotal):
    return all(k + l < maxtotal for k,l in zip(key, lock))

if __name__ == '__main__':
    with open('input') as fd:
        keys = []
        locks = []

        key = None
        lock = None
        for line in fd:
            line = line.strip()
            row = [c for c in line]

            if key and line:
                key.append(row)
            
            if lock and line:
                lock.append(row)

            if not key and not lock:
                if '#' in line:
                    lock = []
                    lock.append(row)
                    locks.append(lock)
                else:
                    key = []
                    key.append(row)
                    keys.append(key)

            if not line:
                key = None
                lock = None

        keys_heights = [compute_heights(k) for k in keys]
        locks_heights = [compute_heights(l) for l in locks]

        tests = []
        for key in keys_heights:
            for lock in locks_heights:
                tests.append(fit(key, lock, len(keys[0]) - 1))

        print(sum(tests))
