from collections import deque
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

ELF = "E"
GOBLIN = "G"

class Player:
    """ parent class player """
    def __init__(self, x, y):
        """ hp = hit points, ap = attack power """
        self.hp = 200
        self.ap = 3
        self.x = x
        self.y = y
    def move(self, coords):
        """ updates player position"""
        self.x = coords[0]
        self.y = coords[1]

    def attack(self, other):
        """ attacks another player """
        if (self.__class__.__bases__ == other.__class__.__bases__):
            other.hp -= self.ap
            print(other.hp)
            return other.hp
        else:
            print("Can not attack non-Player!")
            return None
    def __str__(self):
        return ("P")
class Elf(Player):
    def __str__(self):
        #return "Elf(hp:" + str(self.hp) + ", ap:" + str(self.ap) + ")"
        return "E"
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        return(
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y
        )
    pass

class Goblin(Player):
    def __str__(self):
        #return "Goblin(hp:" + str(self.hp) + ", ap:" + str(self.ap) + ")"
        return "G"
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return(
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y
        )
    pass

def bfs(player, map_):
    """ uses bfs to find best path
    to closest target """
    if isinstance(player, Elf):
        ignore = ELF
    elif isinstance(player, Goblin):
        ignore = GOBLIN
    queue = deque()
    queue.appendleft([[player.x, player.y], []])
    visited = list()
    while True:
        if not queue:
            return None
        node = queue.pop()
        [x, y], path = node
        new_path = list(path)
        new_path.append([x, y])
        visited.append([x, y])
        up = [x, y+1]
        down = [x, y-1]
        left = [x-1, y]
        right = [x+1, y]
        search_nodes = [up, left, right, down]
        # reverses prefered order
        filtered_nodes = [direction for direction in search_nodes
                    if str(map_[direction[1]][direction[0]]) not in (ignore, '#') and
                    direction not in visited]
        # Keep search order u,l,r,d
        list.reverse(filtered_nodes)

        for direction in filtered_nodes:
            obj = map_[direction[1]][direction[0]]
            if isinstance(player, Elf) and isinstance(obj, Goblin) or \
               isinstance(player, Goblin) and isinstance(obj, Elf):
                q_item = [direction, new_path]
                return q_item


        for n in filtered_nodes:
            q_item = [n, new_path]
            queue.appendleft(q_item)


def play_round(map_):
    """ plays a complete round """
    moved_players = []
    for i, row in enumerate(map_):
        for j, col in enumerate(row):
            if col not in ('.', '#') and col not in moved_players:
                # check if opposite player around
                # if there is one attack instead of search for move
                # check list of adjacent players - pick lowest one
                # up left right down 
                adjacent = [map_[i+1][j], map_[i][j-1], map_[i][j+1], map_[i-1][j]]
                if isinstance(col, Elf):
                    enemies = [enemy for enemy in adjacent if isinstance(enemy, Goblin)]
                elif isinstance(col, Goblin):
                    enemies = [enemy for enemy in adjacent if isinstance(enemy, Elf)]
                if enemies:
                    # look for weakest enemy in enemies
                    lowest = enemies[0]
                    for enemy in enemies:
                        if enemy.hp < lowest.hp:
                            lowest = enemy
                    hp = col.attack(lowest)
                    if hp <= 0:
                        map_[lowest.y][lowest.x] = "."
                    print("attack")
                else:
                    bfs_node = bfs(col, map_)
                    if bfs_node is None:
                        print("stand still")
                    else:
                        print("bfs_node: " + str(bfs_node))
                        if len(bfs_node[1]) > 1:
                            move = bfs_node[1][1]
                            old_obj = map_[move[1]][move[0]]
                            map_[move[1]][move[0]] = col
                            map_[i][j] = old_obj
                            # update player position
                            col.move(move)
                            moved_players.append(col)

    for r in map_:
        print(r)

def put_players(init_map):
    """ scan the map and put players where
    there are E's and G's
    """
    for i, row in enumerate(init_map):
        for j, col in enumerate(row):
            if col == ELF:
                obj = Elf(j, i)
            elif col == GOBLIN:
                obj = Goblin(j, i)
            else:
                # copy old object
                obj = init_map[i][j]
            init_map[i][j] = obj
    return init_map

if __name__ == "__main__":
    bfs_inp = read_and_strip(file_name="test_bfs.txt")
    bfs_inp = [list(col) for col in bfs_inp]
    put_players(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
    play_round(bfs_inp)
