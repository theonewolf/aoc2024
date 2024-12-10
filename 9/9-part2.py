#!/usr/bin/env python3

# The digits alternate between indicating the length of a file and the length of free space.
# Each file on disk also has an ID number based on the order of the files as
# they appear before they are rearranged, starting with ID 0.

# Position = file ID
# Even positions == file lengths
# Odd positions == free space in between files

# The amphipod would like to move file blocks one at a time from the end of the
# disk to the leftmost free space block (until there are no gaps remaining
# between file blocks).

# The final step of this file-compacting process is to update the filesystem
# checksum. To calculate the checksum, add up the result of multiplying each of
# these blocks' position with the file ID number it contains. The leftmost
# block is in position 0. If a block contains free space, skip it instead.

FREE_ID = -1

def pprint_disk(disk):
    ret = ''
    for fid, block_count in disk:
        ret += str(fid if fid != FREE_ID else '.') * block_count
    return ret

def iscompact(disk):
    gap = False
    for fid, _ in disk:
        if fid != FREE_ID and gap: return False
        if fid == FREE_ID: gap = True
    return True

def last_fid_block(disk):
    last_i = 0
    for i, (fid, _) in enumerate(disk):
        if fid != FREE_ID:
            last_i = i
    return last_i

def first_free_block(disk):
    for i, (fid, _) in enumerate(disk):
        if fid == FREE_ID:
            return i

def find_free_space(disk, max_i, bc):
    for i, (fid, space) in enumerate(disk):
        if i >= max_i: break
        if fid == FREE_ID and space >= bc:
            return i
    raise Exception('No free space.')

def find_block(disk, bid):
    for i, (fid, _) in enumerate(disk):
        if fid == bid:
            return i

def compact_disk(disk):
    di = last_fid_block(disk)
    fi = first_free_block(disk)
    free_fid, free_bc = disk[fi]
    last_fid, last_bc = disk[di]

    free_bc -= 1
    last_bc -= 1

    disk[fi] = (free_fid, free_bc)
    disk[di] = (last_fid, last_bc)

    # Update data first as it is later in the disk, so the indexes are still
    # valid.
    disk.insert(di + 1, (FREE_ID, 1))
    if last_bc == 0:
        del disk[di]

    # Update free space last as it is earlier in the disk, and will change
    # later indexes.
    disk.insert(fi, (last_fid, 1))
    if free_bc == 0:
        del disk[fi + 1]

    return disk

def compact_block(disk, block):
    """
    This time, attempt to move whole files to the leftmost span of free
    space blocks that could fit the file. Attempt to move each file exactly
    once in order of decreasing file ID number starting with the file with the
    highest file ID number. If there is no span of free space to the left of a
    file that is large enough to fit the file, the file does not move.
    """
    di = find_block(disk, block)
    last_fid, last_bc = disk[di]

    fi = -1
    try:
        fi = find_free_space(disk, di, last_bc)
    except:
        return disk

    free_fid, free_bc = disk[fi]

    free_bc -= last_bc

    # Update data first as it is later in the disk, so the indexes are still
    # valid.
    disk.insert(di + 1, (FREE_ID, last_bc))
    del disk[di]

    # Update free space last as it is earlier in the disk, and will change
    # later indexes.
    disk.insert(fi, (last_fid, last_bc))
    if free_bc == 0:
        del disk[fi + 1]
    else:
        disk[fi + 1] = (free_fid, free_bc)

    return disk

def compute_checksum(disk):
    raw_index = 0
    accumulator = 0
    for fid, bc in disk:
        if fid != FREE_ID:
            for i in range(raw_index, raw_index + bc):
                accumulator += i * fid
        raw_index += bc
    return accumulator

if __name__ == '__main__':
    with open('input') as fd:
        disk = []
        fid = 0
        for line in fd:
            for i,c in enumerate(line.strip()):
                c = int(c)
                if i % 2 == 0 and c:
                    disk += [(fid, int(c))]
                    fid += 1
                elif c:
                    disk += [(FREE_ID, int(c))]


        for i in range(fid - 1, 0, -1):
            compact_block(disk, i)

        print(compute_checksum(disk))
