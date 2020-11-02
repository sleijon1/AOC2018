depth = 11109
target_x, target_y= (9,731)

geologic_index = {
    (0, 0): 0,
    (target_x, target_y): 0,
}

erosion_levels = {
    (0, 0): depth%20183,
    (target_x, target_y): 0,
}

for x in range(target_x+1):
    print(x)
    for y in range(target_y+1):
        if y == 0:
            geologic_index[(x, y)] = x*16807
        elif x == 0:
            geologic_index[(x, y)] = y*48271
        else:
            geologic_index[(x, y)] = erosion_levels[(x-1, y)] * erosion_levels[(x, y-1)]
        erosion_levels[(x, y)] = (geologic_index[(x, y)] + depth) % 20183

print(sum([erosion % 3 for erosion in erosion_levels.values()]))
