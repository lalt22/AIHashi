#!/usr/bin/python3
from helpers import makeGame

'''
Data Structures:
- Game - provides the structure of the map and islands. Majority of methods to solve the game are part of this object
- Island - has co-ordinates (row, col), its max_bridges and a list of neighbours. Neighbours is filled once the game starts
- Bridge - has count (number of planks), direction (vertical or horizontal) and to_island and from_island Island objects corresponding to the islands it connects to
    - the coordinates of to_island and from_island are used for checking bridge equality, bridges existing on islands and linear intersection of bridges

Algorithm:
A recursive backtracking DFS-based algorithm is used. The game starts in solve_it by sorting the islands into descending order of constraints, prioritising highly constrained islands first to get to the solution more efficiently.
For every island in the sorted list of islands, we get the possible combinations of bridges that could be added to solve the game. For each of these permutations, we add it to the list of built bridges in the game and recursively call the solve_it method again moving to the next island in the sorted list with the newly built bridges also provided in the method.
With each recursive call, if we come across an island that has no possible combination of bridges but isn't already full or we have reached the final island and not solved the game we backtrack to the previous island and try a new combination. This continues until there are no more remaining islands and the game has been solved.

Design Decisions:
- Initially there was an Ocean object that had a Bridge object attribute and a pair of co-ordinates. This allowed me to directly reference a (row,col) coordinate for each bridge when building since I was updating an Ocean object however this added a lot of overhead and became very inefficient when checking bridge equality. Thus I chose to remove the Ocean object and make a Bridge object that had no coordinates and required very little data to instantiate, just the islands it connects to, its direction and its count. This made it much easier to add and remove bridges from the solution as necessary
'''
game = makeGame()
game.solve()
