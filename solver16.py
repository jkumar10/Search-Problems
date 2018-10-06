#!/usr/bin/env python
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
# This code has been constructed based on the structure given by Dr. David Crandall
# We have constructed two heuristic fnctions:
# a) Number of misplaced tiles
# b) Circular manhattan distance
# Based on the observations obtained by running the code on the Indiana Burrow server,
# the code solves board 2 to board6 within 2 seoonds and board 8 in 10-15 seconds while board 12 takes around 25+ minutes.

from Queue import PriorityQueue
from random import randrange, sample
import sys
import string


# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row * 4):(row * 4 + 4)]
    return (state[:(row * 4)] + change_row[-dir:] + change_row[:-dir] + state[(row * 4 + 4):],
            ("L" if dir == -1 else "R") + str(row + 1))



# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col + 1))


# print board state
def print_board(row):
    for j in range(0, 16, 4):
        print '%3d %3d %3d %3d' % (row[j:(j + 4)])

#Using number of misplaced tiles as heuristic.
#Here in this method we are comparing our board with the goal board (which is obtained by sorting in ascending order)
# Each element in our state is compared with the corresponding element in the goal state. If there is a match then
# we increment count by 1. The total number of misplaced elements are obtained by subtracting count from 16.
# This heuristic does not seem to work beyond board 4.
def heuristic1(state):
    goal = sorted(state)
    arr = []
    count = 0
    for i in state:
        arr.append(i)
    for i in range(0, 16):
        if arr[i] == goal[i]:
            count += 1
    misplaced = 16 - count
    return misplaced

# Using Manhattan Distance
#Here in this method we are calculating the circular manhattan distance. So for our reference and ease we
# have visualized a single list as two-dimensional matrix with both x-value and y-value. The goal state is otained
# sorting the intial state in ascending order. The x-value and y-value of both the goal state and the successor state is
#obtained by mapping the single list to the dictionary of coordinates. The key of the dictionary denotes the index position of
#single list while its value denotes the x and y positions.
def heuristic2(state):
    goal = sorted(state)
    #https://stackoverflow.com/questions/16318757/calculating-manhattan-distance-in-python-in-an-8-puzzle-game
    coordinates = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (0, 3),
                   4: (1, 0), 5: (1, 1), 6: (1, 2), 7: (1, 3),
                   8: (2, 0), 9: (2, 1), 10: (2, 2), 11: (2, 3),
                   12: (3, 0), 13: (3, 1), 14: (3, 2), 15: (3, 3)}

    # We will be calculating the circular manhattan distance using the below function and use it for our heuristic calculation
    # Comparing the position of the current element against its location in the desired goal state
    # x and y value of both the goal state and current successor state is obtained by
    #mapping the values from the list of dictionary.
    manhattanDist = 0
    for i in range(0, 16):
        element = state[i]
        pos = goal.index(element)
        xvalue, yvalue = coordinates[i]
        xgoal, ygoal = coordinates[pos]

        #following if and else conditions takes care of the borderline cases
        #The first if loop compares first row elements and last row elements to the corresponding elements in the goal state.
        #If the difference of x coordinates in goal state and intial state is 3 then we are comparing first and last row elements
        #and in addition, if x coordinate is equal to y coordinate of goal state and vice versa then we are comparing the top right most and bottom
        #left most elements of board, thereby increasing the distance by +2. Else we are calculating the simple manhattan distance.

        if ((xvalue == 0 and xgoal == 3) or (xvalue == 3 and xgoal == 0)):
            if (xvalue == ygoal) and (yvalue == xgoal):
                manhattanDist += 2
            elif ((xvalue == 0 and xgoal == 3) and (yvalue == 0 and ygoal == 3)):
                manhattanDist += 2
            else:
                manhattanDist += (1 + abs(yvalue - ygoal))
        elif ((yvalue == 0 and ygoal == 3) or (yvalue == 3 and ygoal == 0)):
            manhattanDist += (1 + abs(xvalue - xgoal))

        else:
            manhattanDist += (abs(xvalue - xgoal) + abs(yvalue - ygoal))
    return float(manhattanDist) / 4


# return a list of possible successor states
been_state = []


def successors1(state):
    successor = []
    for i in range(0, 4):
        for d in (-1, 1):
            successor.append(shift_row(state, i, d))

    for i in range(0, 4):
        for d in (-1, 1):
            successor.append(shift_col(state, i, d))
    # Here we attempted to eliminate duplicate states from entering the fringe so as to optiimize and reduce the time taken by board 12,
    # however we have commented this part because our board 8 did not seem to work.
    # for success in been_state:
    #     for success1 in successor:
    #         if (success == success1[0]):
    #             successor.remove(success1)
    #
    # for success in successor:
    #     been_state.append(success)

    return successor




# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))


# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)


# Here we have taken a priority queue so that the state with the minimum manhattan ditance + distance
# from the initial state is always popped from the list first.
def solve(initial_board):
    a = PriorityQueue()
    a.put((0, (initial_board, "")))

    while not (a.empty()):
        (p, (state, route_so_far)) = a.get()
        for (succ, move) in successors1(state):
            if is_goal(succ):
                return (route_so_far + " " + move)
            l = len(route_so_far.split())
            a.put((heuristic2(state) + l, (succ, route_so_far + " " + move)))

    return False


# inputting the board from the command line.
filename=(sys.argv[1])
start_state = []
with open(filename, 'r') as file:
    for line in file:
        start_state += [int(i) for i in line.split()]

if len(start_state) != 16:
    print "Error: couldn't parse start state file"

print "Start state: "
print_board(tuple(start_state))

print "Solving..."
route = solve(tuple(start_state))


print "Solution found in " + str(len(route) / 3) + " moves:" + "\n" + route