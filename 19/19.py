#!/usr/bin/env python3

def stripe_search(stripes, towel):
    if len(towel) == 0: return True

    for stripe in stripes:
        if towel.startswith(stripe):
            towel = towel[len(stripe):]
            return stripe_search(stripes, towel)

    return False

if __name__ == '__main__':
    with open('test_input') as fd:
        towels = []
        stripes = []

        for line in fd:
            line = line.strip()
            if ',' in line:
                stripes = set([l.strip() for l in line.split(',')])
            elif line:
                towels += [line]
        print(stripes)
        print(towels)

        print([stripe_search(stripes, towel) for towel in towels])
        print(sum([stripe_search(stripes, towel) for towel in towels]))
