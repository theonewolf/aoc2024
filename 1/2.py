#!/usr/bin/env python
import aoc

if __name__ == '__main__':
    with open('input') as fd:
        l1 = []
        l2 = []
        for line in fd:
            l,r = line.strip().split()
            l,r = int(l),int(r)
            l1.append(l)
            l2.append(r)

        l1 = sorted(l1)
        l2 = sorted(l2)

        similarity = 0
        for l in l1:
            similarity += l * l2.count(l)
        print(similarity)
