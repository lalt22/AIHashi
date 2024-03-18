# AIHashi

## What is Hashiwokakero?
![Val42-Bridge1n](https://github.com/lalt22/AIHashi/assets/71425918/b83d4364-172f-4d33-994e-25a2fc9587c8) ![Val42-Bridge1](https://github.com/lalt22/AIHashi/assets/71425918/548abee8-f155-4cd6-bb94-c47c0c853be9)


A logic puzzle, also known as Bridges or Chopsticks in English. The puzzle typically consists of a grid of islands, each represented by a circle, with numbers indicating how many bridges must be connected to each island. The objective is to connect all the islands with bridges in such a way that:

- The number of bridges connected to each island matches the number specified on the island.
- Bridges cannot cross one another.
- Bridges can only be horizontal or vertical and cannot cross islands or other bridges.
- Every island must be accessible from every other island through a series of connected bridges.
  
The difficulty of the puzzle increases with the size of the grid and the complexity of the islands' configurations. 

The rendition of the game solved by this algorithm has two deviations from standard requirements:
- Bridges may have up to 3 planks rather than just 2
- The islands do not all have to be accessible to each other

## How To Run

### Compilation

```console
    $ gcc bridgen.c -o bridgen
```

### Passing Generated Map to Program

```console
    $ ./bridgen | python3 hashi.py
```

## How The Program Works
The input to the program will be a rectangular array of numbers and dots entered to the command line:

![image](https://github.com/lalt22/AIHashi/assets/71425918/4315c2ea-63e6-4bac-aa23-17ab73f55f3e)

This input can be automatically generated with the bridgen.c file. This will always output a valid game. 
From there, helpers.py will convert the array into a game as detailed below:

### Data Structures
- Game - provides the structure of the map and islands. The majority of methods to solve the game are part of this object
- Island - has coordinates (row, col), its max_bridges and a list of neighbours. Neighbours is filled once the game starts
- Bridge - has count (number of planks), direction (vertical or horizontal), and to_island and from_island Island objects corresponding to the islands it connects to
    - the coordinates of to_island and from_island are used for checking bridge equality, bridges existing on islands, and linear intersection of bridges

### Algorithm:
A recursive backtracking DFS-based algorithm is used. The game starts in solve_it by sorting the islands into descending order of constraints, prioritizing highly constrained islands first to get to the solution more efficiently.
For every island in the sorted list of islands, we get the possible combinations of bridges that could be added to solve the game. For each of these permutations, we add it to the list of built bridges in the game and recursively call the solve_it method again moving to the next island in the sorted list with the newly built bridges also provided in the method.
With each recursive call, if we come across an island that has no possible combination of bridges but isn't already full or we have reached the final island and not solved the game we backtrack to the previous island and try a new combination. This continues until there are no more remaining islands and the game has been solved.

### Design Decisions:
- Initially, there was an Ocean object that had a Bridge object attribute and a pair of co-ordinates. This allowed me to directly reference a (row, col) coordinate for each bridge when building since I was updating an Ocean object however this added a lot of overhead and became very inefficient when checking bridge equality. Thus I chose to remove the Ocean object and make a Bridge object that had no coordinates and required very little data to instantiate, just the islands it connects to, its direction, and its count. This made it much easier to add and remove bridges from the solution as necessary
'''
## Future Changes
Currently the program is quite inefficient as it is using a List object to store all the bridges in the game. This requires a lot of blind iteration over the list which is very time-intensive and causes the program to be unable to solve games greater than size 9x9. To optimise the program, I intend to change the implementation to use a Dict of the format (Island : List[Bridge]). This dict format will allow each Island to have a list of Bridges associated with it, so when searching for bridges associated with islands we can simply index the dict directly rather than iterating over one large list.
