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
        self.bridgeCount = 0
        self.neighbours: List[Island] = []

    def changeBridgeCount(self, planks):
        self.bridgeCount += planks

    def isComplete(self):
        if (self.bridgeCount == self.maxBridges):
            return True
        return False

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
class Ocean:
    def __init__(self, row:int, col:int):
        self.row = row
        self.col = col
        self.bridge = None

    def addBridge(self, bridge:Bridge):
        self.bridge = bridge

    def hasBridge(self):
        return self.bridge

    def show(self):
        if (self.bridge == None):
            print(" . ", end="")
        else:
            self.bridge.show()

class Game:
    def __init__(self, nrows:int, ncols:int, oceans: List[Ocean], islands: List[Island]):
        self.nrows = nrows
        self.ncols = ncols
        self.oceans = oceans
        self.islands = islands
        self.bridges = {}

    def show_game(self):
        for row in range(self.nrows):
            for col in range(self.ncols):
                ocean_val = next((ocean for ocean in self.oceans if ocean.row == row and ocean.col == col), None)
                island_val = next((island for island in self.islands if island.row == row and island.col == col), None)
                if (ocean_val):
                    ocean_val.show()
                if (island_val):
                    island_val.show()
            print("\n")


    def solve(self):
        self.getNeighbours()
        islands = self.sort_islands_by_constraints()
        solved, bridges = self.solve_it(islands, [])
        if solved:
            pass
        else:
            raise ValueError("Game cannot be solved!")

    def solve_it(self, remaining_islands: List[Island], built_bridges: List[Bridge]) -> tuple[bool, List[Bridge]]:
        if not remaining_islands and self.isGameComplete():
            return True, built_bridges
        for i, island in enumerate(remaining_islands):
            possible_bridges = self.get_possible_island_bridges(island)
            # print(possible_bridges)
            # for bridges in possible_bridges:
            #     print(f"Bridge with weight {bridges.count} from {bridges.from_island.maxBridges} to {bridges.to_island.maxBridges}")
            for bridges in possible_bridges:
                solved, b = self.solve_it(remaining_islands[i+1:], built_bridges + bridges)
                if solved:
                    return True, b
        return False, []


    def get_possible_island_bridges(self, island:Island) -> List[List[Bridge]]:
        # print(f"Getting possible bridges for {len(island.neighbours)} neighbours with {island.maxBridges} planks")
        possible_bridges = []

        perms = list(self.get_permutations_to_sum(island.maxBridges, len(island.neighbours), []))
        for perm in perms:
            perm_bridges = []
            for weight, neighbour in zip(perm, island.neighbours):
                if (neighbour.row == island.row):
                    if (weight > 0):
                        perm_bridges.append(Bridge(weight, "horizontal", island, neighbour))
                if (neighbour.col == island.col):
                    if (weight > 0):
                        perm_bridges.append(Bridge(weight, "vertical", island, neighbour))
                if (len(perm_bridges) > 0):
                    possible_bridges.append(perm_bridges)
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
                if (value > 3):
                    continue
                for perm in self.get_permutations_to_sum(sum - value, num_neighbours - 1, perms):
                    if (any(num > 3 or num < 0 for num in perm)):
                        continue
                    yield [value] + perm



    def add_bridge(self, from_island:Island, to_island:Island, weight:int):
        pass

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

    # def addBridge(self, islandA:Island, islandB:Island, weight:int):
    #     #Check direction of bridge
    #     if (islandA.row == islandB.row):
    #         direction = "horizontal"
    #     else:
    #         direction = "vertical"

    #     if (direction == "horizontal"):
    #         #Check whether going left or right
    #         if (islandA.col > islandB.col):
    #             #Going left
    #             self.drawBridges(islandA.col - 1, islandB.col, islandA.row, -1, direction, weight, islandA, islandB)
    #             islandA.changeBridgeCount(weight)
    #             islandB.changeBridgeCount(weight)
    #         else:
    #             #going right
    #             self.drawBridges(islandA.col + 1, islandB.col, islandA.row, 1, direction, weight, islandA, islandB)
    #             islandA.changeBridgeCount(weight)
    #             islandB.changeBridgeCount(weight)
    #     if (direction == "vertical"):
    #         if (islandA.row > islandB.row):
    #             #Going up
    #             self.drawBridges(islandA.row - 1, islandB.row, islandA.col, -1, direction, weight, islandA, islandB)
    #             islandA.changeBridgeCount(weight)
    #             islandB.changeBridgeCount(weight)
    #         else:
    #             #going down
    #             self.drawBridges(islandA.row + 1, islandB.row, islandA.col, 1, direction, weight, islandA, islandB)
    #             islandA.changeBridgeCount(weight)
    #             islandB.changeBridgeCount(weight)

    #     pass

    # def drawBridges(self, start, end, const, step, direction, weight, nodeA, nodeB):
    #     if (direction == "horizontal"):
    #         for col in range(start, end, step):
    #             ocean = self.getOceanAtCoord(const, col)
    #             if (ocean != None):
    #                 ocean.addBridge(Bridge(weight, const, col, direction, nodeA, nodeB))
    #     else:
    #         for row in range(start, end, step):
    #             ocean = self.getOceanAtCoord(row, const)
    #             if (ocean != None):
    #                 ocean.addBridge(Bridge(weight, const, col, direction, nodeA, nodeB))

    # def getMostConstrainedNode(self):
    #     for node in self.gameMap:
    #         if(type(node) is Island):
    #             if (self.nodeIsCorner(node) and node.maxBridges == 6):
    #                 return node
    #             if (self.nodeIsEdge(node) and node.maxBridges == 9):
    #                 return node
    #             if (node.maxBridges == 12):
    #                 return node
    #     return self.getFirstIsland()

    # def getFirstIsland(self):
    #     for node in self.gameMap:
    #         if (type(node) is Island):
    #             return node

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


    def isGameComplete(self):
        for island in self.islands:
            if(not island.isComplete()):
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


    # #If coord is island, return the island, otherwise return Ocean
    # def coordIsIsland(self, row, col):
    #     for node in self.islands:
    #         if (type(node) is Island):
    #             if (node.row == row and node.col == col):
    #                 return node
    #     return None

    # def getOceanAtCoord(self, row, col):
    #     for node in self.gameMap:
    #         if (type(node) is Ocean):
    #             if (node.row == row and node.col == col):
    #                 return node
    #     return None

    def solveFromNode(self, node:Island):
        for island in node.neighbours:
            print(f"Old bridge counts:\n {node.maxBridges}: {node.row}, {node.col} = {node.bridgeCount}\n {island.maxBridges}: {island.row}, {island.col} = {island.bridgeCount}")
            if (node.bridgeCount + 3 <= node.maxBridges and island.bridgeCount + 3 <= island.maxBridges):
                self.addBridge(node, island, 3)
                print(f"New bridge counts:\n {node.maxBridges}: {node.row}, {node.col} = {node.bridgeCount}\n {island.maxBridges}: {island.row}, {island.col} = {island.bridgeCount}")
            elif (node.bridgeCount + 2 <= node.maxBridges and island.bridgeCount + 2 <= island.maxBridges):
                self.addBridge(node, island, 2)
            elif (node.bridgeCount + 1 <= node.maxBridges and island.bridgeCount + 1 <= island.maxBridges):
                self.addBridge(node, island, 1)
            if (island.bridgeCount == island.maxBridges):
                break
            self.solveFromNode(island)

def map_to_lists(nrows, ncols, map):
    islandList = []
    oceanList = []
    for row in range(nrows):
        for col in range(ncols):
            if(map[row][col] == 0):
                oceanList.append(Ocean(row, col))
            else:
                islandList.append(Island(row, col, map[row][col]))
    return oceanList, islandList

def makeGame():
    nrows, ncols, map = scan_map()
    oceans, islands = map_to_lists(nrows, ncols, map)

    return Game(nrows, ncols, oceans, islands)
