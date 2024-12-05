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

    if grid[y][x] == 'X':
        # n
        try:
            if (grid[y - 1][x] == 'M' and \
                grid[y - 2][x] == 'A' and \
                grid[y - 3][x] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in North direction.')
        except:
            print('Not in North direction.')

        # e
        try:
            if (grid[y][x + 1] == 'M' and \
                grid[y][x + 2] == 'A' and \
                grid[y][x + 3] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in East direction.')
        except:
            print('Not in East direction.')

        # s
        try:
            if (grid[y + 1][x] == 'M' and \
                grid[y + 2][x] == 'A' and \
                grid[y + 3][x] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in South direction.')
        except:
            print('Not in South direction.')

        # w
        try:
            if (grid[y][x - 1] == 'M' and \
                grid[y][x - 2] == 'A' and \
                grid[y][x - 3] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in West direction.')
        except:
            print('Not in West direction.')


        # ne
        try:
            if (grid[y - 1][x + 1] == 'M' and \
                grid[y - 2][x + 2] == 'A' and \
                grid[y - 3][x + 3] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in Northeast direction.')
        except:
            print('Not in Northeast direction.')

        # se
        try:
            if (grid[y + 1][x + 1] == 'M' and \
                grid[y + 2][x + 2] == 'A' and \
                grid[y + 3][x + 3] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in Southeast direction.')
        except:
            print('Not in Southeast direction.')

        # sw
        try:
            if (grid[y + 1][x - 1] == 'M' and \
                grid[y + 2][x - 2] == 'A' and \
                grid[y + 3][x - 3] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in Southwest direction.')
        except:
            print('Not in Southwest direction.')

        # nw
        try:
            if (grid[y - 1][x - 1] == 'M' and \
                grid[y - 2][x - 2] == 'A' and \
                grid[y - 3][x - 3] == 'S'):
                count += 1
                print(f'Found at ({x},{y}) in Northwest direction.')
        except:
            print('Not in Northwest direction.')

    return count

if __name__ == '__main__':
    with open('input') as fd:
        data = fd.read().split()
        newdata = NoNegativeIndexList([])
        
        print(newdata)

        for row in data:
            newdata.append(NoNegativeIndexList(row))

        total_count = 0
        for x in range(len(newdata[0])):
            for y in range(len(newdata)):
                total_count += count_xmas(newdata, x, y)

        print(total_count)
