#!/usr/bin/env python3

from sys import maxsize

COST_A = 3
COST_B = 1

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
                machines.append([(x, y), buttons])
                buttons = {}
                continue

            if line.strip():
                raise Exception(f'Unexpected line: {line}')

        wins = []
        for machine in machines:
            min_cost = maxsize
            target_x, target_y = machine[0]

            for a in range(100):
                for b in range(100):
                    delta_a_x, delta_a_y = machine[1]['A']
                    delta_b_x, delta_b_y = machine[1]['B']

                    move_a_x, move_a_y = delta_a_x * a, delta_a_y * a
                    move_b_x, move_b_y = delta_b_x * b, delta_b_y * b
                    move_x = move_a_x + move_b_x
                    move_y = move_a_y + move_b_y

                    cost_a = COST_A * a
                    cost_b = COST_B * b
                    cost = cost_a + cost_b

                    if cost < min_cost and \
                       target_x - move_x == 0 and \
                       target_y - move_y == 0:
                           min_cost = cost
                           wins.append((cost, a, b))

        print(sum([w[0] for w in wins]))
