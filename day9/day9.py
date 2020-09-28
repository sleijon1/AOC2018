import sys
sys.path.append("../")
from day1.day1part2 import read_and_strip

def marble_game(players, points):
    """ Plays a game of Elvish marble
    Keyword args:
    players: amount of players
    points: amount of marbles(value of last marble)
    """
    # populate player dict
    players_dict = {}
    for player in range(players):
        players_dict[player] = []

    current_marble = 0
    circle = []
    circle.append(current_marble)
    player_index = 0
    for marble in range(1, points+1):
        # each round each player takes turn
        player = players_dict[player_index]
        if marble != 0 and marble % 23 == 0:
            player.append(marble)
            index_removal = circle.index(current_marble)-7
            if index_removal < 0:
                index_removal = len(circle)+index_removal
            
            marble_index = index_removal
            # marble 7 steps to the left
            player.append(circle[marble_index])
            if marble_index+1 == len(circle):
                current_marble = circle[0]
            else:
                current_marble = circle[marble_index+1]
            circle.pop(marble_index)
        else:
            insert_index = circle.index(current_marble)+2
            if insert_index > len(circle):
                insert_index = insert_index-len(circle)
            circle.insert(insert_index, marble)
            current_marble = marble

        # cycle players
        if player_index < players-1:
            player_index += 1
        else:
            player_index = 0

    return circle, players_dict

def format_input(inp):
    """ return players,points of input"""
    split = inp[0].split(" ")
    players = int(split[0])
    points = int(split[-2])
    return players, points

if __name__ == "__main__":
    inp = read_and_strip()
    players, points = format_input(inp)
    circle, players = marble_game(players, points)
    player_scores = [sum(players[player]) for player in players]
    print(player_scores)
    print(max(player_scores))
    #print("circle: " + str(circle))
    
    print(inp)
