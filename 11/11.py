#!/usr/bin/env python3

# If the stone is engraved with the number 0, it is replaced by a stone
# engraved with the number 1.

# If the stone is engraved with a number that has an even number of digits, it
# is replaced by two stones. The left half of the digits are engraved on the
# new left stone, and the right half of the digits are engraved on the new
# right stone. (The new numbers don't keep extra leading zeroes: 1000 would
# become stones 10 and 0.)

# If none of the other rules apply, the stone is replaced by a new stone; the
# old stone's number multiplied by 2024 is engraved on the new stone.

def update_stones(stones):
    newstones = []
    
    for stone in stones:
        if stone == 0:
            newstones.append(1)
        else:
            strstone = str(stone)
            if len(strstone) % 2 == 0:
                split = len(strstone) // 2
                l,r = strstone[:split], strstone[split:]
                newstones.append(int(l))
                newstones.append(int(r))
            else:
                newstones.append(stone * 2024)
    return newstones

if __name__ == '__main__':
    with open('test_input') as fd:
        for line in fd:
            stones = [int(n) for n in line.split()]

        for i in range(1):
            stones = update_stones(stones)

        print(stones)

    with open('test_input2') as fd:
        for line in fd:
            stones = [int(n) for n in line.split()]

        for i in range(6):
            stones = update_stones(stones)

        print(stones)

    with open('input') as fd:
        for line in fd:
            stones = [int(n) for n in line.split()]

        for i in range(25):
            stones = update_stones(stones)

        print(stones)
        print(len(stones))
