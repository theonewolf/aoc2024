#!/usr/bin/env python3

def valid_update(rules, update):
    for i,value1 in enumerate(update):
        for value2 in update[i+1:]:
            try:
                if value2 not in rules[value1]:
                    print(f'{value2} not in rules for {value1}')
                    return False
            except:
                print(f'{value1} not in rules dictionary...')
                if value1 == update[-1]:
                    print(f'But it is in last position, this is fine.')
                    return True
                return False

    return True

if __name__ == '__main__':
    with open('input') as fd:
        rules = {}
        updates = []
        valid = []

        # Parse input
        for line in fd:
            if '|' in line:
                before, after = line.split('|')
                before = int(before)
                after = int(after)
                brule = rules.get(before, set())
                brule.add(after)
                rules[before] = brule
            if ',' in line:
                updates.append([int(i) for i in line.split(',')])

        # Get valid updates
        for update in updates:
            if valid_update(rules, update):
                valid.append(update)

        # Compute sum of middle pages
        accumulator = 0
        for update in valid:
            accumulator += update[len(update) // 2]

        print(rules)
        print(updates)
        print(valid)
        print(accumulator)
