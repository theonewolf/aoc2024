#!/usr/bin/env python3

from functools import lru_cache
from math import floor, log10
from operator import add, mul
from pprint import pprint

@lru_cache(maxsize=None)  # Cache results for all inputs
def concatenate_integers(a, b):
    # Calculate the number of digits in `b`
    length = floor(log10(b)) + 1 if b > 0 else 1

    # Shift `a` and add `b`
    return a * (10 ** length) + b

def concat(v1, v2):
    return int(str(v1) + str(v2))

def is_satisfiable(equation):
    result = equation[0]
    values = equation[1:]
    ops = [add, mul, concatenate_integers]

    for operator in range(4**(len(values)-1)):
        accumulator = values[0]
        for i in range(len(values) - 1):
            if (operator >> (2 * i)) & 0b11 == 0b11: continue
            accumulator = ops[(operator >> (2 * i)) % 3](accumulator, values[i+1])
        if accumulator == result:
            return True
    return False

if __name__ == '__main__':
    with open('input') as fd:
        equations = [eq.split(':') for eq in fd.read().splitlines()]
        equations = [[int(result)] + [int(v) for v in values.split()] for result, values in equations]
        
        satisfiable_values = []
        for equation in equations:
            if is_satisfiable(equation):
                satisfiable_values.append(equation[0])
                pprint(equation)
                pprint(satisfiable_values)

        print(sum(satisfiable_values))

