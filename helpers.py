from scan_print_map import scan_map

class Island:
    def __init__(self, x:int, y:int, maxBridges:int):
        self.x = x
        self.y = y
        self.maxBridges = maxBridges
        self.bridgeCount = 0

    def addBridge(self, otherIsland):
        self.bridgeCount+=1
        pass

    def isComplete(self):
        if (self.bridgeCount == self.maxBridges):
            return True
        return False

class Ocean:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.hasBridge = False

    def addBridge(self):
        self.hasBridge = True

    def hasBridge(self):
        return self.hasBridge


class Game:
    def __init__(self, islands:list, oceans:list, nrows:int, ncols:int):
        self.islands = islands
        self.oceans = oceans

    def getConnections(self, node:Island):
        pass


    def canBridgeIslands(self, islandA:Island, islandB:Island):
        pass

    def addBridge(self, islandA:Island, islandB:Island):
        pass

    def isGameComplete(self):
        for island in self.islands:
            if(not island.isComplete()):
               return False
        return True

    def sortIslandsByHighestConstrant(self):
        return sorted(self.islands, key=lambda island:(island.maxBridges - island.bridgeCount))


def map_to_lists(nrows, ncols, map):
    islandMap = []
    oceanMap = []
    print(map)
    for r in range(nrows):
        for c in range(ncols):
            if(map[r][c] == 0):
                oceanMap.append(Ocean(r, c))
            else:
                islandMap.append(Island(r, c, map[r][c]))
    return islandMap, oceanMap

def makeGame():
    nrows, ncols, map = scan_map()
    islandMap, oceanMap = map_to_lists(nrows, ncols, map)

    return Game(islandMap, oceanMap, nrows, ncols)
