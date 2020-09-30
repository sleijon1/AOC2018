import sys
import time
sys.path.append("../")
from day1.day1part2 import read_and_strip
from blist import *

def marble_game(players, points):
    """ Plays a game of Elfish marble
    Keyword args:
    players: amount of players
    points: amount of marbles(value of last marble)
    """
    # populate player dict
    players_dict = {}
    for player in range(players):
        players_dict[player] = 0

    current_marble = 0
    circle = blist([]) # list implementation - O(logn) insertion
    circle.append(current_marble)
    player_index = 0
    index = 0
    for marble in range(1, points+1):
        # each round each player takes turn
        player = players_dict[player_index]
        circle_length = len(circle)
        if marble != 0 and marble % 23 == 0:
            players_dict[player_index] += marble
            index_removal = index-7
            if index_removal < 0:
                index_removal = circle_length+index_removal

            marble_index = index_removal
            # marble 7 steps to the left
            players_dict[player_index] += circle[marble_index]
            if marble_index+1 == circle_length:
                current_marble = circle[0]
                index = 0
            else:
                current_marble = circle[marble_index+1]
            circle.pop(marble_index)
            index = marble_index
        else:
            insert_index = index+2
            if insert_index > circle_length:
                insert_index = insert_index-circle_length
            circle.insert(insert_index, marble)
            current_marble = marble
            index = insert_index

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
    players_amount, points = format_input(inp)
    start = time.time()
    circle, players = marble_game(players_amount, points*100)
    end = time.time()
    print("Runtime: " + str(end-start))
    player_scores = [players[player] for player in players]
    print("Player with highest score: " + str(max(player_scores)))
    print("(Players: " + str(players_amount) + ". Marbles: " + str(points) + ".)")
