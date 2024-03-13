from __future__ import annotations
from scan_print_map import scan_map
from typing import Generator, List

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

    def show(self):
        if (self.maxBridges == 10):
            print("a", end="")
        elif (self.maxBridges == 11):
            print("b", end="")
        elif (self.maxBridges == 12):
            print("c", end="")
        else:
            print(f"{self.maxBridges}", end="")

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
                print('|', end="")
            if (self.count == 2):
                print('"', end="")
            if (self.count == 3):
                print("#", end="")
        if (self.direction == 'horizontal'):
            if (self.count == 1):
                print('-', end="")
            if (self.count == 2):
                print('=', end="")
            if (self.count == 3):
                print("E", end="")

    def __eq__(self, other: Bridge):
        return ((self.from_island == other.from_island and
                 self.to_island == other.to_island) or
                (self.from_island == other.to_island and
                 self.to_island == other.from_island)
                ) and \
            self.count == other.count


class Game:
    def __init__(self, nrows:int, ncols:int, islands: List[Island]):
        self.nrows = nrows
        self.ncols = ncols
        self.islands = islands

    def show_game(self, bridges: List[Bridge], solved: bool):
        print("\n")
        for row in range(self.nrows):
            for col in range(self.ncols):
                if (not solved):
                    island_val = next((island for island in self.islands if island.row == row and island.col == col), None)

                    if (island_val):
                        island_val.show()
                    else:
                        print(".", end="")
                if (solved):
                    island_val = next((island for island in self.islands if island.row == row and island.col == col), None)
                    if (island_val):
                        island_val.show()
                    else:
                        bridge_pos = self.find_bridge_at_point(row, col, bridges)
                        if (bridge_pos):
                            self.draw_bridge(bridge_pos)
                        else:
                            print(" ", end="")
            print("\n")
        # for bridge in bridges:
        #     print(f"Bridge weight: {bridge.count}")

    def solve(self):
        self.getNeighbours()
        # for island in self.islands:
        #     print(f"Neighbours for BEFORE {island.maxBridges}")
        #     for neighbour in island.neighbours:
        #         print(f"{neighbour.maxBridges}: ({neighbour.row},{neighbour.col})", end=", ")
        #     print("\n")
        islands: List[Island] = self.sort_islands_by_constraints()
        # print()
        # for island in islands:
        #     print(f"Neighbours for {island.maxBridges}")
        #     for neighbour in island.neighbours:
        #         print(f"{neighbour.maxBridges}: ({neighbour.row},{neighbour.col})", end=", ")
        #     print("\n")
        # for island in islands:
        #     print(f"{island.maxBridges}, ", end="")
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
        count = 0
        for i, island in enumerate(remaining_islands):
            print(f"Checking permutations at island {island.maxBridges}: ({island.row},{island.col})")
            print("[", end="")
            for bridge in built_bridges:
                print(f"[From: ({bridge.from_island.row},{bridge.from_island.col}) -> {bridge.count} -> To: ({bridge.to_island.row},{bridge.to_island.col})] , ", end="")
            print("]")

            possible_perms = self.get_island_permutations(island, built_bridges)
            possible_bridges = self.get_possible_island_bridges(island, possible_perms, built_bridges)

            for bridges in possible_bridges:
                intersecting = False
                #If a bridge intersects with already built bridges, skip the perm
                for bridge in bridges:
                    if(self.do_bridges_intersect(bridge, built_bridges)):
                        intersecting = True
                        break
                if (intersecting):
                    # print("Removing intersecting bridge")
                    possible_bridges.remove(bridges)
                elif (not intersecting):
                    solved, b = self.solve_it(remaining_islands[i+1:], built_bridges + bridges)
                    if solved:
                        return True, b
            count += 1
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
                print("-", end="")
            elif bridge.count == 2:
                print("=", end="")
            elif bridge.count == 3:
                print("E", end="")
        elif (bridge.direction == "vertical"):
            if bridge.count == 1:
                print("|", end="")
            elif bridge.count == 2:
                print("\"", end="")
            elif bridge.count == 3:
                print("#", end="")


    def do_bridges_intersect(self, bridge: Bridge, bridges: List[Bridge]) -> bool:
        x1 = bridge.from_island.row
        y1 = bridge.from_island.col

        x2 = bridge.to_island.row
        y2 = bridge.to_island.col

        for b2 in bridges:
            x3 = b2.from_island.row
            y3 = b2.from_island.col

            x4 = b2.to_island.row
            y4 = b2.to_island.col

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
                # print(f"Bridges from {x1},{y1} to {x2},{y2} and from {x3},{y3} to {x4}, {y4} intersect at {intersect_x}, {intersect_y}")
                return True
            else:
                return False

    def does_bridge_exist(self, islandA: Island, islandB: Island, bridges: List[Bridge]) -> Bridge:
        for bridge in bridges:
            if ((bridge.to_island == islandA and bridge.from_island == islandB) or \
                (bridge.from_island == islandA and bridge.to_island == islandB)):
                return bridge
        return None

    def get_possible_island_bridges(self, island: Island, possible_perms: List[List[int]], existing_bridges: List[Bridge]) -> List[List[Bridge]]:
        possible_bridges: List[List[Bridge]] = []

        for perm in possible_perms:
            perm_bridges: List[Bridge] = []
            for weight, neighbour in zip(perm, island.neighbours):
                if self.does_bridge_exist(island, neighbour, existing_bridges):
                    continue
                if not self.can_add_bridge_with_weight(neighbour, weight, existing_bridges):
                    break
                # print(f"Drawing bridge from {island.maxBridges}:({island.row},{island.col}) with weight {weight} to neighbour {neighbour.maxBridges}:({neighbour.row},{neighbour.col})")
                if (neighbour.row == island.row):
                    if (weight > 0):
                        perm_bridges.append(Bridge(weight, "horizontal", island, neighbour))
                if (neighbour.col == island.col):
                    if (weight > 0):
                        perm_bridges.append(Bridge(weight, "vertical", island, neighbour))
                if (len(perm_bridges) > 0):
                    if ([perm_bridges not in possible_bridges]):
                        possible_bridges.append(perm_bridges)
        return possible_bridges

    def can_add_bridge_with_weight(self, island: Island, weight: int, existing_bridges: List[Bridge]) -> bool:
        count = 0
        for bridge in existing_bridges:
            if (bridge.from_island == island or bridge.to_island == island):
                count += bridge.count
        return (count + weight <= island.maxBridges)

    def get_permutations_to_sum(self, sum: int, num_neighbours: int, perms: List[List[int]]) -> Generator[list[int]]:
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

    def get_island_permutations(self, island:Island, existing_bridges: List[Bridge]) -> List[List[int]]:
        all_perms = list(self.get_permutations_to_sum(island.maxBridges, len(island.neighbours), []))
        if (len(island.neighbours) == 1):
            # print([[island.maxBridges]])
            return [[island.maxBridges]]
        elif (len(island.neighbours) == 2 and island.maxBridges == 6):
            # print([[3,3]])
            return [[3,3]]
        elif (len(island.neighbours) == 3 and island.maxBridges == 9):
            print([[3,3,3]])
            return [[3,3,3]]
        elif (len(island.neighbours) == 4 and island.maxBridges == 12):
            # print([[3,3,3,3]])
            return [[3,3,3,3]]

        perms: List[List[int]] = []
        for perm in all_perms:
            valid = True
            for i, neighbour in enumerate(island.neighbours):
                existing_bridge = self.does_bridge_exist(island, neighbour, existing_bridges)
                if (existing_bridge and perm[i] != existing_bridge.count):
                    valid = False
                    break
            if valid:
                perms.append(perm)

        # for perm in perms:
        #     print(perm)
        return perms


    def sort_islands_by_constraints(self):
        # for island in self.islands:
        #     print(f"Neighbours for Unsorted {island.maxBridges} at ({island.row},{island.col}) -> ", end="")
        #     for neighbour in island.neighbours:
        #         print(f"{neighbour.maxBridges}: ({neighbour.row},{neighbour.col})", end=", ")
        #     print("\n")
        sortedIslands = []

        #Prioritise maxed islands
        for island in self.islands:
            #Check for maxed corners
            if (((island.col == 0 and \
                island.row == 0) or \
                (island.col == 0 and \
                island.row == self.nrows-1) or \
                (island.col == self.ncols-1 and \
                island.row == 0) or \
                (island.col == self.ncols-1 and \
                island.row == self.nrows-1)) and \
                (island.maxBridges == 6)):
                    # print(f"Appending corner: {island.maxBridges}")
                    sortedIslands.append(island)

            #Check for maxed edges
            if ((island.col == 0 or \
                island.col == self.ncols-1 or \
                island.row == 0 or \
                island.row == self.nrows-1) and \
                island.maxBridges == 9):
                    # print(f"Appending edge: {island.maxBridges}")
                    sortedIslands.append(island)

            #Check for maxed centers
            if (not (island.col == 0 or \
                island.col == self.ncols-1 or \
                island.row == 0 or \
                island.row == self.nrows-1) and \
                island.maxBridges == 12):
                    # print(f"Appending middle: {island.maxBridges}")
                    sortedIslands.append(island)

        #Next, islands with only one neighbour
        for island in self.islands:

            if (island.neighbours == 1):
                # print(f"Appending one neighbour: {island.maxBridges}")
                sortedIslands.append(island)

        #Next, add rest
        for island in self.islands:
            if (island not in sortedIslands):
                # print(f"Appending rest: {island.maxBridges}")
                sortedIslands.append(island)




        # for island in sortedIslands:
        #     print(f"Neighbours for Sorted {island.maxBridges} at ({island.row},{island.col}) -> ", end="")
        #     for neighbour in island.neighbours:
        #         print(f"{neighbour.maxBridges}: ({neighbour.row},{neighbour.col})", end=", ")
        #     print("\n")
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

    ''''
    For every island in game, fill the neighbours list
    Search right, left, up, down until either first island is found or map ends
    Append the islands neighbours list with found islands
    '''
    def getNeighbours(self):
        #First check x neighbours

        ##First check leftwards
        for island in self.islands:
            for col in range(island.col-1, -1, -1):
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == island.row and neighbour.col == col), None)
                # print(f"Searching left from {island.row},{island.col}")
                # maybeIsland = self.coordIsIsland(island.row, col)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

            ##Then check rightwards
            for col in range(island.col + 1, self.ncols):
                # print(f"Searching right from {island.row},{island.col}")
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == island.row and neighbour.col == col), None)
                # maybeIsland = self.coordIsIsland(island.row, col)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

            #Then check y neighbours

            #First check up
            for row in range(island.row - 1, -1, -1):
                # print(f"Searching up from {island.row},{island.col}")
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == row and neighbour.col == island.col), None)
                # maybeIsland = self.coordIsIsland(row, island.col)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

            #Then check down
            for row in range(island.row + 1, self.nrows,):
                # print(f"Searching down from {island.row},{island.col}")
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