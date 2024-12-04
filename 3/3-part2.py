#!/usr/bin/env python3

from re import findall

if __name__ == '__main__':
    raw_re = r'mul\((\d+),(\d+)\)'

    with open('input') as fd:
        data = fd.read()
        data = data.split(r'do()')
        accumulator = 0
        for segment in data:
            segment = segment.split(r"don't()")[0]
            matches = findall(raw_re, segment)
            pairs = [(int(x), int(y)) for x, y in matches]
            accumulator += sum([x*y for x,y in pairs])
        print(accumulator)
