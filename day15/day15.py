import copy
from collections import deque
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

ELF = "E"
GOBLIN = "G"
GAME_DONE = "D"

class Player:
    """ parent class player """
    def __init__(self, x, y, ap=3, hp=200):
        """ hp = hit points, ap = attack power """
        self.hp = hp
        self.ap = ap
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
        new_path = list(path)
        new_path.append((x, y))

        visited.add((x, y))

        up = (x, y-1)
        down = (x, y+1)
        left = (x-1, y)
        right = (x+1, y)
        search_nodes = [up, left, right, down]

        # reverses prefered order
        filtered_nodes = [direction for direction in search_nodes
                    if str(map_[direction[1]][direction[0]]) not in (ignore, '#') and
                    direction not in visited]

        for element in filtered_nodes:
            obj = map_[element[1]][element[0]]
            q_item = [element, new_path]
            if isinstance(player, Elf) and isinstance(obj, Goblin) or \
               isinstance(player, Goblin) and isinstance(obj, Elf):
                return q_item
            else:
                duplicates = [item[0] for item in queue if item[0] == element]
                if not duplicates:
                    queue.appendleft(q_item)

def try_attack(player, map_, players):
    """attacks lowest hp nearby player if there is one """
    i = player.y
    j = player.x
    adjacent = [map_[i-1][j], map_[i][j-1], map_[i][j+1], map_[i+1][j]]
    if isinstance(player, Elf):
        enemies = [enemy for enemy in adjacent if isinstance(enemy, Goblin)]
    elif isinstance(player, Goblin):
        enemies = [enemy for enemy in adjacent if isinstance(enemy, Elf)]
    else:
        return False
    if enemies:
        lowest = enemies[0]
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

def print_map(map_):
    # prints map nicely
    for r in map_:
        string = ""
        for c in r:
            string = string + str(c)
        print(string)


def play_round(map_, players):
    """ plays a complete round """
    moved_players = []
    for i, row in enumerate(map_):
        for j, col in enumerate(row):
            if col not in ('.', '#') and col not in moved_players:
                if not try_attack(col, map_, players):
                    bfs_node = bfs(col, map_)
                    if bfs_node is not None:
                        if len(bfs_node[1]) > 1:
                            move = bfs_node[1][1]
                            old_obj = map_[move[1]][move[0]]
                            map_[move[1]][move[0]] = col
                            map_[i][j] = old_obj
                            col.move(move)
                            try_attack(col, map_, players)
                            moved_players.append(col)
    print_map(map_)

    if (all(isinstance(p, Elf) for p in players) or \
        all(isinstance(p, Goblin) for p in players)):
        return GAME_DONE
    else:
        return None

def put_players(init_map, elf_ap=3, goblin_ap=3):
    """ scan the map and put players where
    there are E's and G's
    """
    players = []
    for i, row in enumerate(init_map):
        for j, col in enumerate(row):
            if col == ELF:
                obj = Elf(j, i, ap=elf_ap)
                players.append(obj)
            elif col == GOBLIN:
                obj = Goblin(j, i)
                players.append(obj)
            else:
                # copy old object
                obj = init_map[i][j]
            init_map[i][j] = obj
    print(players)
    goblins = [goblin for goblin in players if isinstance(goblin, Goblin)]
    elves = [elf for elf in players if isinstance(elf, Elf)]
    print("amount of goblins: " + str(len(goblins)))
    print("amount of elves: " + str(len(elves)))
    return init_map, players

def play_rounds(inp, players, rounds=None):
    round_ = 0
    if rounds is None:
        # play rounds until one race left
        while True:
            print("Round: " + str(round_))
            round_result = play_round(inp, players)
            if round_result is not None:
                winner_hp = sum([player.hp for player in players])
                winner_race = str(players[0])
                winner_ap = str(players[0].ap)
                print("Winners("  + winner_race + "(ap:" + winner_ap + ")" \
                      + ") won with " + \
                      str(winner_hp) + "hp remaining.")
                print(str(winner_race) + " left:" + str(len(players)))
                return winner_race, winner_hp, players
            round_ += 1
    else:
        for r in range(rounds):
            play_round(inp, players)
            #print(players)

def play_game():
    inp = read_and_strip(file_name="test_bfs.txt")
    inp = [list(col) for col in inp]
    # Part one - run event
    part_one = copy.deepcopy(inp)
    _, players_one = put_players(part_one)
    play_rounds(part_one, players_one)

    # Part two - Ensure elvish victory
    nr_of_elves = len([player for player in put_players(copy.deepcopy(inp))[1] if isinstance(player, Elf)]) # fix horrendous 1-liner
    part_two = copy.deepcopy(inp)
    elvish_death = True
    elf_ap = 3
    #exit()
    while elvish_death:
        _, players_two = put_players(part_two, elf_ap=elf_ap)
        winner_race, _, winners = play_rounds(part_two, players_two)
        if winner_race == GOBLIN or (winner_race == ELF and len(winners) < nr_of_elves):
            elf_ap += 1
            part_two = copy.deepcopy(inp)
            print_map(part_two)
        else:
            elvish_death = False



if __name__ == "__main__":
    play_game()
    #_, players = put_players(bfs_inp)
    #play_rounds(bfs_inp, players)
    #print(players)
