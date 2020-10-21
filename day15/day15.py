import copy
from collections import deque
import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

ELF = "E"
GOBLIN = "G"
GAME_DONE = "D"
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_map(map_):
    # prints map nicely
    for i, r in enumerate(map_):
        string = ""
        for j, c in enumerate(r):
            string = string +  bcolors.OKGREEN + str(c) + bcolors.ENDC
        string += " " + str(i)
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

    def coords(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self, other):
        return(
            self.__class__ == other.__class__ and
            self.id_num == other.id_num
        )

class Elf(Player):
    def __str__(self):
        return "E"
    def __repr__(self):
        return str(self)
    def opponent(self):
        return GOBLIN
    
class Goblin(Player):
    def __str__(self):
        return "G"
    def __repr__(self):
        return str(self)
    def opponent(self):
        return ELF
    
def breadth_first_search(player, map_):
    """ uses breadth_first_search to find closest path
    to target (reading order) """
    queue = deque()
    queue.appendleft([[player.x, player.y], []])
    visited = set()
    possible_nodes = []
    possible_paths = list()
    while True:
        if not queue:
            return None
        node = queue.pop()
        (x, y), path = node
        new_path = list(path)
        new_path.append((x, y))
        visited.add((x, y))
        search_nodes = [(x, y-1), (x-1, y), (x+1, y), (x, y+1)]
        possible_nodes = [direction for direction in search_nodes
                    if str(map_[direction[1]][direction[0]]) not in (str(player), '#') and
                    direction not in visited]

        for p_node in possible_nodes:
            obj = map_[p_node[1]][p_node[0]]
            q_item = [p_node, new_path]
            if str(obj) == player.opponent():
                return q_item[1][1]
            else:
                duplicates = [item[0] for item in queue if item[0] == p_node]
                if not duplicates:
                    queue.appendleft(q_item)
        
def try_attack(player, map_, players):
    """attacks lowest hp nearby player if there is one """
    adjacent = [map_[player.y-1][player.x], map_[player.y][player.x-1], \
                map_[player.y][player.x+1], map_[player.y+1][player.x]]
    enemies = [enemy for enemy in adjacent if str(enemy) == player.opponent()]
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
    for row in map_:
        for player in row:
            if player not in made_move and player not in ("#", "."):
                reachable_targets = try_attack(player, map_, players)
                if not reachable_targets:
                    breadth_first_search_node = breadth_first_search(player, map_)
                    if breadth_first_search_node is not None:
                        new_x, new_y = breadth_first_search_node
                        map_[new_y][new_x] = player
                        map_[player.y][player.x] = "."
                        player.move([new_x, new_y])
                        try_attack(player, map_, players)
                    elif breadth_first_search_node is None \
                         and (all(isinstance(p, Elf) for p in players) or \
                                                   all(isinstance(p, Goblin) for p in players)):
                        return GAME_DONE
                made_move.append(player)

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

def play_rounds(inp, players):
    round_ = 1
    while True:
        print_map(inp)
        round_result = play_round(inp, players)
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
        #for player in players:
        #    print(str(player) + str(player.coords()) + "- HP: " +str(player.hp))
        round_ += 1

def play_game():
    inp = read_and_strip(file_name="test_bfs.txt")
    inp = [list(col) for col in inp]
    # Part one - run event
    part_one = copy.deepcopy(inp)
    _, players_one = put_players(part_one)
    play_rounds(part_one, players_one)
    exit()
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
