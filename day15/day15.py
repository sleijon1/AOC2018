from collections import deque
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

ELF = "E"
GOBLIN = "G"
GAME_DONE = "D"

class Player:
    """ parent class player """
    def __init__(self, x, y):
        """ hp = hit points, ap = attack power """
        self.hp = 200
        self.ap = 3
        self.x = x
        self.y = y
        self.stand_still = False
    def move(self, coords):
        """ updates player position"""
        self.x = coords[0]
        self.y = coords[1]

    def attack(self, other):
        """ attacks another player """
        if (self.__class__.__bases__ == other.__class__.__bases__):
            other.hp -= self.ap
            #print(other.hp)
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
    visited = set()
    while True:
        if not queue:
            return None
        node = queue.pop()
        [x, y], path = node
        if (x, y) in visited:
            continue
        new_path = list(path)
        new_path.append((x, y))

        visited.add((x, y))

        up = (x, y+1)
        down = (x, y-1)
        left = (x-1, y)
        right = (x+1, y)
        search_nodes = [up, left, right, down]
        #print(search_nodes)
        # reverses prefered order
        filtered_nodes = [direction for direction in search_nodes
                    if str(map_[direction[1]][direction[0]]) not in (ignore, '#') and
                    direction not in visited]
        #print("current node: " + str(node[0]))
        #print("possible nodes: " + str(filtered_nodes))

        #print("\nnode: " + str(node))
        #print(visited)

        # Keep search order u,l,r,d
        list.reverse(filtered_nodes)
        for element in filtered_nodes:
            obj = map_[element[1]][element[0]]
            q_item = [element, new_path]
            if isinstance(player, Elf) and isinstance(obj, Goblin) or \
               isinstance(player, Goblin) and isinstance(obj, Elf):
                return q_item
            else:
                queue.appendleft(q_item)

def try_attack(player, map_, players):
    """attacks lowest hp nearby player if there is one """
    i = player.y
    j = player.x
    adjacent = [map_[i+1][j], map_[i][j-1], map_[i][j+1], map_[i-1][j]]
    if isinstance(player, Elf):
        enemies = [enemy for enemy in adjacent if isinstance(enemy, Goblin)]
    elif isinstance(player, Goblin):
        enemies = [enemy for enemy in adjacent if isinstance(enemy, Elf)]
    else:
        return False
    if enemies:
        list.reverse(enemies)
        lowest = enemies[0]
        #print("Enemies: " + str(enemies))
        for enemy in enemies:
            if enemy.hp < lowest.hp:
                lowest = enemy
        hp = player.attack(lowest)
        print("attacker: " + str(player) + str(player.x) + str(player.y))
        print("attacker hp: " + str(player.hp))
        print("attackee: " + str(lowest) + str(lowest.x) + str(lowest.y))
        print("attackee hp: " + str(hp))
        if hp <= 0:
            map_[lowest.y][lowest.x] = "."
            players.remove(lowest)

        return True
    return False

def play_round(map_, players):
    """ plays a complete round """
    moved_players = []
    same_state = True
    for i, row in enumerate(map_):
        for j, col in enumerate(row):
            if col not in ('.', '#') and col not in moved_players:
                if try_attack(col, map_, players):
                    #print("attacked")
                    if (all(isinstance(p, Elf) for p in players) or \
                        all(isinstance(p, Goblin) for p in players)):
                        return GAME_DONE
                else:
                    if col.stand_still and same_state:
                        #print("same state - standing still again")
                        pass
                    else:
                        #print("before bfs")
                        bfs_node = bfs(col, map_)
                       # print("after bfs")
                        if bfs_node is None:
                            #print("stand still")
                            col.stand_still = True
                        else:
                            #print("bfs_node: " + str(bfs_node))
                            if len(bfs_node[1]) > 1:
                                move = bfs_node[1][1]
                                old_obj = map_[move[1]][move[0]]
                                map_[move[1]][move[0]] = col
                                map_[i][j] = old_obj
                                # update player position
                                col.move(move)
                                col.stand_still = False
                                same_state = False
                                # try to attack if movement resulted
                                # in attack range to opponent player
                                try_attack(col,map_,players)
                                moved_players.append(col)


def put_players(init_map):
    """ scan the map and put players where
    there are E's and G's
    """
    players = []
    for i, row in enumerate(init_map):
        for j, col in enumerate(row):
            if col == ELF:
                obj = Elf(j, i)
                players.append(obj)
            elif col == GOBLIN:
                obj = Goblin(j, i)
                players.append(obj)
            else:
                # copy old object
                obj = init_map[i][j]
            init_map[i][j] = obj
    return init_map, players

def play_rounds(inp, players, rounds=None):
    round_ = 1
    if rounds is None:
        # play rounds until one race left
        while True:
            print("Round: " + str(round_))
            round_result = play_round(inp, players)
            if round_result is not None:
                winner_hp = sum([player.hp for player in players])
                winner_race = str(players[0])
                print("Winners("  + winner_race + ") won with " + \
                      str(winner_hp) + "hp remaining.")
                for player in players:
                    print(player.hp)
                return winner_race, winner_hp
            round_ += 1
    else:
        for r in range(rounds):
            play_round(inp, players)
            #print(players)

if __name__ == "__main__":
    bfs_inp = read_and_strip(file_name="test_bfs.txt")
    bfs_inp = [list(col) for col in bfs_inp]
    _, players = put_players(bfs_inp)
    play_rounds(bfs_inp, players)
    print(players)
