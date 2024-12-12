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
    newstones = {}
    for stone in stones.keys():
        if stone == 0:
            newstones[1] = newstones.get(1, 0) + stones[0]
        else:
            strstone = str(stone)
            if len(strstone) % 2 == 0:
                split = len(strstone) // 2
                l,r = int(strstone[:split]), int(strstone[split:])
                newstones[l] = newstones.get(l, 0) + stones[stone]
                newstones[r] = newstones.get(r, 0) + stones[stone]
            else:
                newstones[stone * 2024] = newstones.get(stone * 2024, 0) + stones[stone]
    return newstones

if __name__ == '__main__':
    with open('input') as fd:
        for line in fd:
            raw = [int(n) for n in line.split()]
            stones = {}
            for num in raw:
                stones[num] = stones.get(num, 0) + 1

        for i in range(75):
            stones = update_stones(stones)
            print(f'Iteration {i}: # of stones is {sum(stones.values())}')

        print(stones)
        print(sum(stones.values()))
