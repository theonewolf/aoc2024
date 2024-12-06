#!/usr/bin/env python3

from itertools import permutations
from functools import cmp_to_key

def valid_update(rules, update):
    for i,value1 in enumerate(update):
        for value2 in update[i+1:]:
            try:
                if value2 not in rules[value1]:
                    #print(f'{value2} not in rules for {value1}')
                    return False
            except:
                #print(f'{value1} not in rules dictionary...')
                if value1 == update[-1]:
                    print(f'But it is in last position, this is fine.')
                    return True
                return False

    return True

# Way too many :-)
# Some lists had 24+ elements...24! is large.
# Heat death of Universe return?
def fix_update(rules, update):
    for permutation in permutations(update):
        if valid_update(rules, permutation):
            return permutation
    raise Exception('OMG not possible!?')

# Custom comparison function
def create_custom_compare(rules):
    def custom_compare(x, y):
        if x not in rules:
            return 1
        
        if y not in rules:
            return -1
        
        if y in rules[x]:
            return -1 # x comes before y
        elif x in rules[y]:
            return 1   # x comes after y
        elif x == y:
            return 0   # x and y are equal
        else:
            raise Exception(f'Failed on {x} {y}')
    return custom_compare

# Sub-second return
def fix_update2(rules, update):
    return sorted(update, key=cmp_to_key(create_custom_compare(rules)))

if __name__ == '__main__':
    with open('input') as fd:
        rules = {}
        updates = []
        valid = []
        invalid = []

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
            else:
                invalid.append(update)


        # Fixup invalids
        newly_valid = []
        for update in invalid:
            newly_valid.append(fix_update2(rules, update))

        # Compute sum of middle pages
        accumulator = 0
        for update in newly_valid:
            accumulator += update[len(update) // 2]

        print(rules)
        print(updates)
        print(invalid)
        print(newly_valid)
        print(accumulator)
