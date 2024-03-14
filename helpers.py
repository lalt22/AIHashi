#!/usr/bin/python3

from __future__ import annotations
from scan_print_map import scan_map
from typing import Generator, List
import logging
import timeit
import time

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger("Game")

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
        self.bridges = {}

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

    def show_game(self, bridges: List[Bridge]):
        for row in range(self.nrows):
            row_empty = True
            for col in range(self.ncols):
                island_val = next((island for island in self.islands if island.row == row and island.col == col), None)
                if (island_val):
                    island_val.show()
                    row_empty = False
                else:
                    bridge_pos = self.find_bridge_at_point(row, col, bridges)
                    if (bridge_pos):
                        self.draw_bridge(bridge_pos)
                    else:
                        print(" ", end="")
                        row_empty = False
            # logger.debug("ROW EMPTY")
            if (not row_empty):
                print("\n", end="")
    def solve(self):
        logger.debug("I AM HERE!")
        self.getNeighbours()
        # islands: List[Island] = self.sort_islands_by_constraints(self.islands, [])
        start = time.process_time()
        solved, bridges = self.solve_it(self.islands, [])
        logging.debug(f"Time: {time.process_time() - start}")
        if solved:
            self.show_game(bridges)
        else:
            raise ValueError("Game cannot be solved!")

    def solve_it(self, remaining_islands: List[Island], built_bridges: List[Bridge]) -> tuple[bool, List[Bridge]]:
        remaining_islands = self.sort_islands_by_constraints(remaining_islands, built_bridges)
        if not remaining_islands and self.isGameComplete(built_bridges):
            return True, built_bridges

        for i, island in enumerate(remaining_islands):
            if (logging.root.level <= logging.INFO):
                logging.info(f"Checking permutations at island {island.maxBridges}: ({island.row},{island.col})")
                logging.info("[")
                for bridge in built_bridges:
                    logging.info(f"[From: ({bridge.from_island.row},{bridge.from_island.col}) -> {bridge.count} -> To: ({bridge.to_island.row},{bridge.to_island.col})] , ")
                logging.info("]")

            start = time.process_time()
            possible_perms = self.get_island_permutations(island, built_bridges)
            out = time.process_time()
            # if (out - start > 0.0):
            #     print(f"Time in island permutations: {out - start}")

            start = time.process_time()
            possible_bridges = self.get_possible_island_bridges(island, possible_perms, built_bridges)
            out = time.process_time()
            # if (out - start > 0.0):
            #     # print(f"Time in island bridges: {out - start}")

            #If no possible bridges, backtrack. every island must be able to build or already have at least one bridge
            logging.info(f"Invalid path made to {island.maxBridges}: ({island.row}, {island.col}). Backtracking")
            if len(possible_bridges) == 0 and self.get_number_of_bridges_at_island(island, built_bridges) < island.maxBridges:
                return False, []

            for bridges in possible_bridges:
                solved, b = self.solve_it(remaining_islands[i+1:], built_bridges + bridges)
                if solved:
                    return True, b
        logging.debug(f"No valid perms: BACKTRACKING. {len(remaining_islands)} islands remaining")
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
                return True
            else:
                return False

    def does_bridge_exist(self, islandA: Island, islandB: Island, bridges: List[Bridge]) -> Bridge:
        possible_bridge = [bridge for bridge in bridges if ((bridge.to_island == islandA and bridge.from_island == islandB) or (bridge.from_island == islandA and bridge.to_island == islandB))]
        if possible_bridge:
            return possible_bridge[0]
        else:
            return None
        # for bridge in bridges:
        #     if ((bridge.to_island == islandA and bridge.from_island == islandB) or \
        #         (bridge.from_island == islandA and bridge.to_island == islandB)):
        #         return bridge
        # return None

    def get_possible_island_bridges(self, island: Island, possible_perms: List[List[int]], existing_bridges: List[Bridge]) -> List[List[Bridge]]:
        possible_bridges: List[List[Bridge]] = []

        for perm in possible_perms:
            perm_bridges: List[Bridge] = []
            for weight, neighbour in zip(perm, island.neighbours):
                if self.does_bridge_exist(island, neighbour, existing_bridges):
                    continue
                if not self.can_add_bridge_with_weight(neighbour, weight, existing_bridges):
                    break
                if (neighbour.row == island.row):
                    if (weight > 0):
                        new_bridge = Bridge(weight, "horizontal", island, neighbour)
                        if (not self.do_bridges_intersect(new_bridge, existing_bridges)):
                            perm_bridges.append(new_bridge)
                        else:
                            break
                if (neighbour.col == island.col):
                    if (weight > 0):
                        new_bridge = Bridge(weight, "vertical", island, neighbour)
                        if (not self.do_bridges_intersect(new_bridge, existing_bridges)):
                            perm_bridges.append(new_bridge)
                        else:
                            break
                if (len(perm_bridges) > 0):
                    if ([perm_bridges not in possible_bridges]):
                        possible_bridges.append(perm_bridges)
        return possible_bridges

    def can_add_bridge_with_weight(self, island: Island, weight: int, existing_bridges: List[Bridge]) -> bool:
        count = self.get_number_of_bridges_at_island(island, existing_bridges)
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
                for perm in self.get_permutations_to_sum(sum - value, num_neighbours - 1, perms):
                    if (any(num > 3 or num < 0 for num in perm)):
                        continue
                    yield [value] + perm

    def get_island_permutations(self, island:Island, existing_bridges: List[Bridge]) -> List[List[int]]:
        all_perms = list(self.get_permutations_to_sum(island.maxBridges, len(island.neighbours), []))
        if (len(island.neighbours) == 1):
            return [[island.maxBridges]]
        elif (len(island.neighbours) == 2 and island.maxBridges == 6):
            return [[3,3]]
        elif (len(island.neighbours) == 3 and island.maxBridges == 9):
            return [[3,3,3]]
        elif (len(island.neighbours) == 4 and island.maxBridges == 12):
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
        return perms

    def get_number_of_bridges_at_island(self, island:Island, built_bridges: List[Bridge]) -> int:
        count = sum([bridge.count for bridge in built_bridges if (bridge.to_island == island or bridge.from_island == island)])
        # count = sum(bridge.count for bridge in attached_bridges)
        return count

    def get_unfilled_neighbours_count(self, island:Island, built_bridges: List[Bridge]) -> int:

        count = 0
        for neighbour in island.neighbours:
            logging.debug(f"Checking number of bridges at: {neighbour.maxBridges}:({neighbour.row}, {neighbour.col})")
            if neighbour.maxBridges == self.get_number_of_bridges_at_island(neighbour, built_bridges):
                logging.debug(f"Skipping at: {neighbour.maxBridges}:({neighbour.row}, {neighbour.col})")
                continue
            count += 1
        return count

    def sort_islands_by_constraints(self, remaining_islands: List[Island], built_bridges: List[Bridge]):
        sortedIslands = []
        #Prioritise maxed islands
        for island in remaining_islands:
            remaining_weight = island.maxBridges - self.get_number_of_bridges_at_island(island, built_bridges)
            # open_neighbours = self.get_unfilled_neighbours_count(island, built_bridges)
            open_neighbours = len([neighbour for neighbour in island.neighbours if self.get_number_of_bridges_at_island(neighbour, built_bridges) == neighbour.maxBridges])
            #Check for maxed corners
            if (open_neighbours == 2 and \
                (remaining_weight == 6)):
                    sortedIslands.append(island)
            #Check for maxed edges
            if (open_neighbours == 3 and \
                remaining_weight == 9):
                    sortedIslands.append(island)
            #Check for maxed centers
            if (open_neighbours == 4 and \
                remaining_weight == 12):
                    sortedIslands.append(island)
        #Next, islands with only one neighbour
            if (open_neighbours == 1):
                sortedIslands.append(island)
        #Next, add rest
        for island in remaining_islands:
            if (island not in sortedIslands):
                sortedIslands.append(island)
        for island in sortedIslands:
            logging.debug(f"{island.maxBridges}:({island.row}, {island.col})")
        return sortedIslands

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
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

            ##Then check rightwards
            for col in range(island.col + 1, self.ncols):
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == island.row and neighbour.col == col), None)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

            #Then check y neighbours

            #First check up
            for row in range(island.row - 1, -1, -1):
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == row and neighbour.col == island.col), None)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

            #Then check down
            for row in range(island.row + 1, self.nrows,):
                maybeIsland = next((neighbour for neighbour in self.islands if neighbour.row == row and neighbour.col == island.col), None)
                if (maybeIsland is not None and maybeIsland not in island.neighbours):
                    island.neighbours.append(maybeIsland)
                    break

def map_to_lists(nrows, ncols, map):
    islandList = []
    for row in range(nrows):
        for col in range(ncols):
            if(not map[row][col] == 0):
                islandList.append(Island(row, col, map[row][col]))
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