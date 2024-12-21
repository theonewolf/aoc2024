#!/usr/bin/env python3

from decimal import Decimal, getcontext
from sys import maxsize

getcontext().prec = 50
COST_A = 3
COST_B = 1
ADD = 10000000000000

# ChatGPT approach works, but needs higher precision
def solve_linear_equations(a1, b1, c1, a2, b2, c2):
    """
    Solves the system of two linear equations:
      a1 * A + b1 * B = c1
      a2 * A + b2 * B = c2

    Parameters:
        a1, b1, c1: Coefficients and result of the first equation.
        a2, b2, c2: Coefficients and result of the second equation.

    Returns:
        A tuple (A, B) representing the solution to the equations.
    """
    # Step 0: Convert to higher precision decimals
    a1, b1, c1, a2, b2, c2 = Decimal(a1), Decimal(b1), Decimal(c1), Decimal(a2), Decimal(b2), Decimal(c2)

    # Step 1: Eliminate one variable (let's eliminate A)
    factor1 = a2 / a1
    b1_prime = b1 * factor1
    c1_prime = c1 * factor1

    # Subtract the modified first equation from the second
    b_new = b2 - b1_prime
    c_new = c2 - c1_prime

    # Step 2: Solve for B
    B = c_new / b_new

    # Step 3: Substitute B into the first equation to solve for A
    A = (c1 - b1 * B) / a1

    # Step 4: Round results if very close to an integer
    A = float_round(A)
    B = float_round(B)

    return A, B

def float_round(value, epsilon=1e-9):
    if not isinstance(value, Decimal): value = Decimal(value)
    if abs(Decimal(value) - Decimal(round(value))) < epsilon:
        return round(value)
    return value

# Wolf: I derived this to check the approach ChatGPT gave me.
# Turns out, precision was the only thing we needed!
def solve_for_A(a1, b1, x, a2, b2, y):
    a1, b1, x, a2, b2, y = Decimal(a1), Decimal(b1), Decimal(x), Decimal(a2), Decimal(b2), Decimal(y)
    numerator   = x - b1 * y / b2
    denominator = a1 - a2 * b1 / b2

    return float_round(numerator / denominator)

# Wolf: I derived this to check the approach ChatGPT gave me.
# Turns out, precision was the only thing we needed!
def solve_for_B(a1, b1, x, a2, b2, y, A):
    a1, b1, x, a2, b2, y, A = Decimal(a1), Decimal(b1), Decimal(x), Decimal(a2), Decimal(b2), Decimal(y), Decimal(A)
    numerator = y - a2 * A
    denominator = b2

    return float_round(numerator / denominator)

# Luckily, testing solutions, even close ones, is easy too.
# This may have been a way to check even with loss of some precision.
def try_solution(a1, b1, x, a2, b2, y, A, B):
    x -= int(round(A)) * a1 + int(round(B)) * b1
    y -= int(round(A)) * a2 + int(round(B)) * b2

    print(f'Test: x == {x} and y == {y}')

    return x == 0 and y == 0

if __name__ == '__main__':
    with open('input') as fd:
        machines = []

        buttons = {}
        for line in fd:
            if 'Button' in line:
                button, movement = line.split(':')
                button = button.split()[1]
                x, y = movement.split(',')
                x, y = x.split('+')[1], y.split('+')[1]
                x, y = int(x), int(y)
                buttons[button] = (x, y)
                continue

            if 'Prize' in line:
                line = line.replace(',', '')
                x, y = line.split()[1:]
                x, y = x.split('=')[1], y.split('=')[1]
                x, y = int(x), int(y)
                x, y = x + ADD, y + ADD
                machines.append([(x, y), buttons])
                buttons = {}
                continue

            if line.strip():
                raise Exception(f'Unexpected line: {line}')

        wins = []
        for machine in machines:
            min_cost = maxsize
            target_x, target_y = machine[0]
            delta_a_x, delta_a_y = machine[1]['A']
            delta_b_x, delta_b_y = machine[1]['B']

            A, B = solve_linear_equations(delta_a_x, delta_b_x, target_x, delta_a_y, delta_b_y, target_y)
            A2 = solve_for_A(delta_a_x, delta_b_x, target_x, delta_a_y, delta_b_y, target_y)
            B2 = solve_for_B(delta_a_x, delta_b_x, target_x, delta_a_y, delta_b_y, target_y, A2)

            if isinstance(A, int) and isinstance(B, int): wins.append((A, B))

        print(sum([A * COST_A for A, _ in wins] + [B * COST_B for _, B in wins]))
