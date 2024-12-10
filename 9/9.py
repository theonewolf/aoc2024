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

def compute_checksum(disk):
    raw_index = 0
    accumulator = 0
    for fid, bc in disk:
        if fid == FREE_ID: continue
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

        counter = 0
        while not iscompact(disk):
            disk = compact_disk(disk)

        print(compute_checksum(disk))
