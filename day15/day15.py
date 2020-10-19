import copy
from collections import deque
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

ELF = "E"
GOBLIN = "G"
GAME_DONE = "D"


def print_map(map_):
    # prints map nicely
    for r in map_:
        string = ""
        for c in r:
            string = string + str(c)
        print(string)

class Player:
    """ parent class player """
    def __init__(self, x, y, id_, ap=3, hp=200):
        """ hp = hit points, ap = attack power """
        self.hp = hp
        self.ap = ap
        self.x = x
        self.y = y
        self.id_num = id_
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
        return "E"
    def __repr__(self):
        return str(self)
    def __eq__(self, other):
        return(
            self.__class__ == other.__class__ and
            self.id_num == other.id_num
        )
    pass

class Goblin(Player):
    def __str__(self):
        return "G"
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return(
            self.__class__ == other.__class__ and
            self.id_num == other.id_num
        )
    pass

def breadth_first_search(player, map_):
    """ uses breadth_first_search to find closest path
    to target (reading order) """
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
        (x, y), path = node
        new_path = list(path)
        new_path.append((x, y))

        visited.add((x, y))

        up = (x, y-1)
        down = (x, y+1)
        left = (x-1, y)
        right = (x+1, y)
        search_nodes = [up, left, right, down]
        possible_nodes = [direction for direction in search_nodes
                    if str(map_[direction[1]][direction[0]]) not in (ignore, '#') and
                    direction not in visited]

        for p_node in possible_nodes:
            obj = map_[p_node[1]][p_node[0]]
            q_item = [p_node, new_path]
            if isinstance(player, Elf) and isinstance(obj, Goblin) or \
               isinstance(player, Goblin) and isinstance(obj, Elf):
                return q_item
            else:
                duplicates = [item[0] for item in queue if item[0] == p_node]
                if not duplicates:
                    queue.appendleft(q_item)

def try_attack(player, map_, players):
    """attacks lowest hp nearby player if there is one """
    adjacent = [map_[player.y-1][player.x], map_[player.y][player.x-1], \
                map_[player.y][player.x+1], map_[player.y+1][player.x]]
    if isinstance(player, Elf):
        enemies = [enemy for enemy in adjacent if isinstance(enemy, Goblin)]
    elif isinstance(player, Goblin):
        enemies = [enemy for enemy in adjacent if isinstance(enemy, Elf)]

    if enemies:
        lowest = enemies[0]
        for enemy in enemies:
            if enemy.hp < lowest.hp:
                lowest = enemy
        remaining_hp = player.attack(lowest)
        if remaining_hp <= 0:
            map_[lowest.y][lowest.x] = "."
            players.remove(lowest)

        return True

    return False

def play_round(map_, players):
    """ plays a complete round """
    made_move = []
    for i, row in enumerate(map_):
        for j, col in enumerate(row):
            if col not in ('.', '#') and col not in made_move:
                reachable_targets = try_attack(col, map_, players)
                if not reachable_targets:
                    breadth_first_search_node = breadth_first_search(col, map_)
                    if breadth_first_search_node is not None:
                        move = breadth_first_search_node[1][1]
                        old_obj = map_[move[1]][move[0]]
                        map_[move[1]][move[0]] = col
                        map_[i][j] = old_obj
                        col.move(move)
                        try_attack(col, map_, players)
                    elif breadth_first_search_node is None \
                         and (all(isinstance(p, Elf) for p in players) or \
                                                   all(isinstance(p, Goblin) for p in players)):
                        return GAME_DONE
                made_move.append(col)

def put_players(init_map, elf_ap=3, goblin_ap=3):
    """ scan the map and put players where
    there are E's and G's
    """
    players = []
    id_ = 0
    for i, row in enumerate(init_map):
        for j, col in enumerate(row):
            if col == ELF:
                obj = Elf(j, i, ap=elf_ap, id_=id_)
                players.append(obj)
            elif col == GOBLIN:
                obj = Goblin(j, i, id_=id_)
                players.append(obj)
            else:
                # copy old object
                obj = init_map[i][j]
            id_ += 1
            init_map[i][j] = obj

    return init_map, players

def play_rounds(inp, players, rounds=None):
    round_ = 1
    if rounds is None:
        while True:
            round_result = play_round(inp, players)
            print_map(inp)
            if round_result == GAME_DONE:
                winner_hp = sum(player.hp for player in players)
                winner_race = str(players[0])
                winner_ap = str(players[0].ap)
                print(players[0])
                print("Winners("  + winner_race + "(ap:" + winner_ap + ")" \
                      + ") won with " + \
                      str(winner_hp) + "hp remaining.")
                print("Full rounds of combat: " + str(round_-1))
                print("outcome:" + str((round_-1)*winner_hp))
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
    #part_one = copy.deepcopy(inp)
    #_, players_one = put_players(part_one)
    #play_rounds(part_one, players_one)

    # Part two - Ensure elvish victory
    nr_of_elves = len([player for player in put_players(copy.deepcopy(inp))[1] if isinstance(player, Elf)]) 
    part_two = copy.deepcopy(inp)
    elf_ap = 3
    winners = []
    winner_race = None
    while True:
        print("Game starting " "(elf_ap: " + str(elf_ap) + ") ->")
        _, players_two = put_players(part_two, elf_ap)
        winner_race, _, winners = play_rounds(part_two, players_two)

        if winner_race == ELF and len(winners) == nr_of_elves:
            break

        elf_ap += 1
        part_two = copy.deepcopy(inp)

if __name__ == "__main__":
    play_game()
    #_, players = put_players(breadth_first_search_inp)
    #play_rounds(breadth_first_search_inp, players)
    #print(players)