#!/usr/bin/env python3

# Find XMAS such that it is:
# horizontal, vertical, diagonal, written backwards, or even overlapping other words

class NoNegativeIndexList(list):
    def __getitem__(self, index):
        if isinstance(index, int) and index < 0:
            raise IndexError("Negative indexing is not allowed.")
        return super().__getitem__(index)

def count_xmas(grid, x, y):
    count = 0

    print(f'Checking: {x},{y}')

    if grid[y][x] == 'M':
        # n
        try:
            if (grid[y - 2][x    ] == 'S' and \
                grid[y - 1][x + 1] == 'A' and \
                grid[y    ][x + 2] == 'M' and \
                grid[y - 2][x + 2] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in North direction.')
        except:
            print('Not in North direction.')

        # e
        try:
            if (grid[y    ][x + 2] == 'S' and \
                grid[y + 1][x + 1] == 'A' and \
                grid[y + 2][x    ] == 'M' and \
                grid[y + 2][x + 2] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in East direction.')
        except:
            print('Not in East direction.')

        # s
        try:
            if (grid[y + 2][x    ] == 'S' and \
                grid[y + 1][x + 1] == 'A' and \
                grid[y    ][x + 2] == 'M' and \
                grid[y + 2][x + 2] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in South direction.')
        except:
            print('Not in South direction.')


        # w
        try:
            if (grid[y    ][x - 2] == 'S' and \
                grid[y + 1][x - 1] == 'A' and \
                grid[y + 2][x    ] == 'M' and \
                grid[y + 2][x - 2] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in West direction.')
        except:
            print('Not in West direction.')

        # Are these possible?
        # ne
        # se
        # sw
        # nw

    return count

if __name__ == '__main__':
    with open('input') as fd:
        data = fd.read().split()
        newdata = NoNegativeIndexList([])
        

        for row in data:
            newdata.append(NoNegativeIndexList(row))

        print(newdata)
        total_count = 0
        for x in range(len(newdata[0])):
            for y in range(len(newdata)):
                total_count += count_xmas(newdata, x, y)

        print(total_count)
