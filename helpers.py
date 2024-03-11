from __future__ import annotations
from scan_print_map import scan_map
from typing import List

'''
Attributes:
- Row and Column - coordinates
- MaxBridges - number on map
- bridgeCount - number of bridges connected
- neighbours - list of x,y adjacent neighbours. max length = 4
'''
class Island:
    def __init__(self, row:int, col:int, maxBridges:int):
        self.row = row
        self.col = col
        self.maxBridges = maxBridges
        self.neighbours: List[Island] = []

    # def changeBridgeCount(self, planks):
    #     self.bridgeCount += planks

    # def isComplete(self):
    #     if (self.bridgeCount == self.maxBridges):
    #         return True
    #     return False

    def addNeighbour(self, island):
        self.neighbours.append(island)

    def show(self):
        print(f" {self.maxBridges} ", end="")

    def __eq__(self, other: Island):
        return self.row == other.row and self.col == other.col

'''
Attributes
- coordinates
- num of planks
- direction
'''
class Bridge:
    def __init__(self, count: int, direction, from_island:Island, to_island:Island):
        self.count = count
        self.direction = direction
        self.from_island = from_island
        self.to_island = to_island

    def addPlank(self):
        self.planks += 1

    def show(self):
        if (self.direction == 'vertical'):
            if (self.count == 1):
                print(' | ', end="")
            if (self.count == 2):
                print(' " ', end="")
            if (self.count == 3):
                print(" # ", end="")
        if (self.direction == 'horizontal'):
            if (self.count == 1):
                print(' - ', end="")
            if (self.count == 2):
                print(' = ', end="")
            if (self.count == 3):
                print(" E ", end="")

    def __eq__(self, other: Bridge):
        return ((self.from_island == other.from_island and
                 self.to_island == other.to_island) or
                (self.from_island == other.to_island and
                 self.to_island == other.from_island)
                ) and \
            self.count == other.count

'''
Attributes
- row and col: coordinates
- bridge object
'''
# class Ocean:
#     def __init__(self, row:int, col:int):
#         self.row = row
#         self.col = col
#         self.bridge = None

#     def addBridge(self, bridge:Bridge):
#         self.bridge = bridge

#     def hasBridge(self):
#         return self.bridge

#     def show(self):
#         if (self.bridge == None):
#             print(" . ", end="")
#         else:
#             self.bridge.show()

class Game:
    def __init__(self, nrows:int, ncols:int, islands: List[Island]):
        self.nrows = nrows
        self.ncols = ncols
        self.islands = islands

    def show_game(self, bridges: List[Bridge], solved: bool):
        for row in range(self.nrows):
            for col in range(self.ncols):
                if (not solved):
                    island_val = next((island for island in self.islands if island.row == row and island.col == col), None)

                    if (island_val):
                        island_val.show()
                    else:
                        print(" . ", end="")
                if (solved):
                    island_val = next((island for island in self.islands if island.row == row and island.col == col), None)
                    if (island_val):
                        island_val.show()
                        continue
                    else:
                        bridge_pos = self.find_bridge_at_point(row, col, bridges)
                        # print(f"Bridge_Pos: {bridge_pos}")
                        if (bridge_pos):
                            self.draw_bridge(bridge_pos)
                        else:
                            print("   ", end="")
            print("\n")
        # for bridge in bridges:
        #     print(f"Bridge weight: {bridge.count}")

    def solve(self):
        self.getNeighbours()
        islands = self.sort_islands_by_constraints()
        solved, bridges = self.solve_it(islands, [])
        if solved:
            self.show_game(bridges, True)
        else:
            raise ValueError("Game cannot be solved!")

    def solve_it(self, remaining_islands: List[Island], built_bridges: List[Bridge]) -> tuple[bool, List[Bridge]]:
        # print(f"Num remaining islands: {len(remaining_islands)}")
        # for bridge in built_bridges:
        #     print(f"Bridge: {bridge.count}, ", end="")
        if not remaining_islands and self.isGameComplete(built_bridges):
            return True, built_bridges
        for i, island in enumerate(remaining_islands):
            # print(f"Checking permutations at island {island.maxBridges}: ({island.row},{island.col})")
            possible_bridges = self.get_possible_island_bridges(island)
            # print(f"{count} possible permutations")
            for bridges in possible_bridges:
                solved, b = self.solve_it(remaining_islands[i+1:], built_bridges + bridges)
                if solved:
                    return True, b
        # print("False, no bridge added")
        return False, []

    def find_bridge_at_point(self, row, col, bridges: List[Bridge]):
        for bridge in bridges:
            if ((bridge.from_island.row <= row <= bridge.to_island.row and bridge.from_island.col <= col <= bridge.to_island.col) or \
                (bridge.from_island.row >= row >= bridge.to_island.row and bridge.from_island.col >= col >= bridge.to_island.col)):
                return bridge
        return None

    def draw_bridge(self, bridge:Bridge):
        if bridge.direction == "horizontal":
            if bridge.count == 1:
                print(" - ", end="")
            elif bridge.count == 2:
                print(" = ", end="")
            elif bridge.count == 3:
                print(" E ", end="")
        elif (bridge.direction == "vertical"):
            if bridge.count == 1:
                print(" | ", end="")
            elif bridge.count == 2:
                print(" \" ", end="")
            elif bridge.count == 3:
                print(" # ", end="")


    def do_bridges_intersect(self, bridge: Bridge, bridges: List[Bridge]) -> bool:
        x1 = bridge.from_island.col
        y1 = bridge.from_island.row

        x2 = bridge.to_island.col
        y2 = bridge.to_island.row

        for b2 in bridges:
            x3 = b2.from_island.col
            y3 = b2.from_island.row

            x4 = b2.to_island.col
            y4 = b2.to_island.row

            slope_b1 = (y2 - y1)/(x2 - x1) if x2 - x1 != 0 else float('inf')
            slope_b2 = (y4 - y3)/(x4 - x3) if x4 - x3 != 0 else float('inf')

            if slope_b1 == slope_b2:
                return False

            if (bridge.from_island == b2.from_island or bridge.from_island == b2.to_island or bridge.to_island == b2.from_island or bridge.to_island == b2.to_island):
                return False

            intersect_x, intersect_y = intersect_points(x1, y1, x2, y2, x3, y3, x4, y4)

            if (min(x1, x2) <= intersect_x <= max(x1, x2) and
            min(y1, y2) <= intersect_y <= max(y1, y2) and
            min(x3, x4) <= intersect_x <= max(x3, x4) and
            min(y3, y4) <= intersect_y <= max(y3, y4)):
                print(f"Bridges from {x1},{y1} to {x2},{y2} and from {x3},{y3} to {x4}, {y4} intersect at {intersect_x}, {intersect_y}")
                return True
            else:
                return False



    def get_possible_island_bridges(self, island:Island) -> List[List[Bridge]]:
        # print(f"Getting possible bridges for {len(island.neighbours)} neighbours with {island.maxBridges} planks")
        possible_bridges: List[List[Bridge]] = []

        perms = list(self.get_permutations_to_sum(island.maxBridges, len(island.neighbours), []))
        # print(f"Permutations for island {island.maxBridges} with {len(island.neighbours)} neighbours")
        # for perm in perms:
        #     print(perm)
        for perm in perms:
            perm_bridges: List[Bridge] = []
            for weight, neighbour in zip(perm, island.neighbours):
                if (neighbour.row == island.row):
                    if (weight > 0):
                        perm_bridges.append(Bridge(weight, "horizontal", island, neighbour))
                if (neighbour.col == island.col):
                    if (weight > 0):
                        perm_bridges.append(Bridge(weight, "vertical", island, neighbour))
                if (len(perm_bridges) > 0):
                    intersecting = False
                    for bridge in perm_bridges:
                        for bridges in possible_bridges:
                            if (self.do_bridges_intersect(bridge, bridges)):
                                intersecting = True
                    if (intersecting == False and [perm_bridges not in possible_bridges]):
                        possible_bridges.append(perm_bridges)
        # print(possible_bridges)
        return possible_bridges

    def get_permutations_to_sum(self, sum: int, num_neighbours: int, perms: List[List[int]]):
        #Given n number of neighbours, find all permutations of length n that add up to sum
        #No number in the permutation can be more than 3
        '''
        E.G
        4 with neighbours n1, n2:
        [3, 1], [2, 2], [1, 3]

        E.G
        11 with neighbours n1, n2, n3, n4
        [3, 3, 3, 2], [3, 3, 2, 3], [3, 2, 3, 3], [2, 3, 3 ,3]

        E.G
        3 with neigbours n1, n2:
        [0, 3], [1, 2], [2, 1], [3, 0]
        '''
        if (num_neighbours == 1):
            yield [sum]

        else:
            for value in range(4):
                # if (value > 3):
                #     continue
                for perm in self.get_permutations_to_sum(sum - value, num_neighbours - 1, perms):
                    if (any(num > 3 or num < 0 for num in perm)):
                        continue
                    yield [value] + perm



    def sort_islands_by_constraints(self):
        sortedIslands = []

        #Prioritise maxed islands
        for island in self.islands:
            #Check for maxed corners
            if ((island.col == 0 and \
                island.row == 0) or \
                (island.col == 0 and \
                island.row == self.nrows-1) or \
                (island.col == self.ncols-1 and \
                island.row == 0) or \
                (island.col == self.ncols-1 and \
                island.row == self.nrows-1) and \
                island.maxBridges == 6):
                    sortedIslands.append(island)

            #Check for maxed edges
            if ((island.col == 0 or \
                island.col == self.ncols-1 or \
                island.row == 0 or \
                island.row == self.nrows-1) and \
                island.maxBridges == 9):
                    sortedIslands.append(island)

            #Check for maxed centers
            if (not (island.col == 0 or \
                island.col == self.ncols-1 or \
                island.row == 0 or \
                island.row == self.nrows-1) and \
                island.maxBridges == 12):
                    sortedIslands.append(island)

        #Next, islands with only one neighbour
        for island in self.islands:

            if (island.neighbours == 1):
                sortedIslands.append(island)

        #Next, add rest
        for island in self.islands:
            if (island not in sortedIslands):
                sortedIslands.append(island)

        return sortedIslands


    def nodeIsCorner(self, node):
        if (node.row == 0 or node.row == self.nrows - 1):
            if (node.col == 0 or node.col == self.ncols-1):
                return True
        return False

    def nodeIsEdge(self, node):
        if (node.row == 0 or node.row == self.nrows - 1 or node.col == 0 or node.col == self.ncols):
            if (not self.nodeIsCorner):
                return True
        return False


    def isGameComplete(self, bridges: List[Bridge]):
        for island in self.islands:
            island_bridges = [bridge for bridge in bridges if (
                ((bridge.from_island == island) or (
                    bridge.to_island == island)
                ))]
            count = sum([bridge.count for bridge in island_bridges])
            if count != island.maxBridges:
                return False
        return True

    def getNeighbours(self):
        #First check x neighbours

        ##First check leftwards
        for island in self.islands:
            for col in range(island.col - 1, -1, -1):
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == island.row and neighbour.col == col), None)
                # maybeIsland = self.coordIsIsland(island.row, col)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

            ##Then check rightwards
            for col in range(island.col + 1, self.ncols):
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == island.row and neighbour.col == col), None)
                # maybeIsland = self.coordIsIsland(island.row, col)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

            #Then check y neighbours

            #First check up
            for row in range(island.row - 1, -1, -1):
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == row and neighbour.col == island.col), None)
                # maybeIsland = self.coordIsIsland(row, island.col)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

            #Then check down
            for row in range(island.row + 1, self.nrows,):
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == row and neighbour.col == island.col), None)
                # maybeIsland = self.coordIsIsland(row, island.col)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break


    # def solveFromNode(self, node:Island):
    #     for island in node.neighbours:
    #         print(f"Old bridge counts:\n {node.maxBridges}: {node.row}, {node.col} = {node.bridgeCount}\n {island.maxBridges}: {island.row}, {island.col} = {island.bridgeCount}")
    #         if (node.bridgeCount + 3 <= node.maxBridges and island.bridgeCount + 3 <= island.maxBridges):
    #             self.addBridge(node, island, 3)
    #             print(f"New bridge counts:\n {node.maxBridges}: {node.row}, {node.col} = {node.bridgeCount}\n {island.maxBridges}: {island.row}, {island.col} = {island.bridgeCount}")
    #         elif (node.bridgeCount + 2 <= node.maxBridges and island.bridgeCount + 2 <= island.maxBridges):
    #             self.addBridge(node, island, 2)
    #         elif (node.bridgeCount + 1 <= node.maxBridges and island.bridgeCount + 1 <= island.maxBridges):
    #             self.addBridge(node, island, 1)
    #         if (island.bridgeCount == island.maxBridges):
    #             break
    #         self.solveFromNode(island)

def map_to_lists(nrows, ncols, map):
    islandList = []
    # oceanList = []
    for row in range(nrows):
        for col in range(ncols):

            #     oceanList.append(Ocean(row, col))
            # else:
            if(not map[row][col] == 0):
                islandList.append(Island(row, col, map[row][col]))
    # return oceanList, islandList
    return islandList

def makeGame():
    nrows, ncols, map = scan_map()
    islands = map_to_lists(nrows, ncols, map)

    return Game(nrows, ncols, islands)

def intersect_points(x1, y1, x2, y2, x3, y3, x4, y4) -> int:
    intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / \
                  ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
    intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / \
                  ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

    return intersect_x, intersect_y