import sys
import re
sys.setrecursionlimit(3000)

WATER = "|"
CLAY = "#"
SAND = "."
REST_WATER = "~"
LEFT = (-1, 0)
RIGHT = (1, 0)
DOWN = (0, 1)

def print_map(map_):
    for row in map_:
        string = ""
        for col in row:
            string = string + col
        print(string)

def run_water(map_, x, y, direction):
    if map_[y][x] == SAND:
        map_[y][x] = WATER
    if y == len(map_) - 1:
        return
    if map_[y][x] == CLAY:
        return x
    if map_[y+1][x] == SAND:
        run_water(map_, x, y+1, 0)
    if map_[y+1][x] in CLAY+REST_WATER:
        if direction:
            return run_water(map_, x+direction, y, direction)
        else:
            left = run_water(map_, x-1, y, -1)
            right = run_water(map_, x+1, y, 1)
            if map_[y][left] == "#" and map_[y][right] == "#":
                for fill in range(left+1, right):
                    map_[y][fill] = REST_WATER
    else:
        return x

def run_ticks():
    data = []
    for line in open("input.txt").read().splitlines():
        a, b, c = map(int, re.findall('\d+', line))
        data += [(a, a, b, c)] if line[0] == 'x' else [(b, c, a, a)]

    Z = zip(*data)
    print(data)
    Z = list(Z)
    minX, maxX, minY, maxY = min(Z[0]), max(Z[1]), min(Z[2]), max(Z[3])

    map_ = [['.']*(maxX - minX + 2) for _ in range(maxY + 1)]
    for x1, x2, y1, y2 in data:
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                map_[y][x - minX + 1] = '#'
    springX, springY = 500 - minX + 1, 0
    map_[0][springX] = '+'

    x, y = springX, springY
    run_water(map_, x, y, 0)
    water = resting_water = 0
    for i in range(minY, maxY+1):
        for tile in map_[i]:
            if tile == WATER:
                water += 1
            elif tile == REST_WATER:
                resting_water += 1

    print("Water tiles: " + str(water))
    print("Resting water tiles: " + str(resting_water))
    print("sum tiles: " + str(resting_water+water))

if __name__ == "__main__":
    run_ticks()
