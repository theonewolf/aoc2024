#!/usr/bin/env python3

from re import findall

if __name__ == '__main__':
    raw_re = r'mul\((\d+),(\d+)\)'

    with open('input') as fd:
        data = fd.read()
        matches = findall(raw_re, data)
        pairs = [(int(x), int(y)) for x, y in matches]
        print(sum([x*y for x,y in pairs]))
