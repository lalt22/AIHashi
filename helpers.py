from scan_print_map import scan_map

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
        self.neighbours = []

    def addBridge(self):
        self.bridgeCount+=1

    def isComplete(self):
        if (self.bridgeCount == self.maxBridges):
            return True
        return False

    def addNeighbour(self, island):
        self.neighbours.append(island)

    def show(self):
        print(f" {self.maxBridges} ", end="")

'''
Attributes
- coordinates
- num of planks
- direction
'''
class Bridge:
    def __init__(self, planks: int, row:int, col:int, direction):
        self.row = row
        self.col = col
        self.planks = planks
        self.direction = direction

    def addPlank(self):
        self.planks += 1

    def show(self):
        if (self.direction == 'vertical'):
            if (self.planks == 1):
                print(' | ', end="")
            if (self.planks == 2):
                print(' " ', end="")
            if (self.planks == 3):
                print(" # ", end="")
        if (self.direction == 'horizontal'):
            if (self.planks == 1):
                print(' - ', end="")
            if (self.planks == 2):
                print(' = ', end="")
            if (self.planks == 3):
                print(" E ", end="")

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
    def __init__(self, gameMap, nrows:int, ncols:int):
        self.nrows = nrows
        self.ncols = ncols
        self.gameMap = gameMap

    def getConnections(self, node:Island):
        pass

    def showGame(self):
        for node in self.gameMap:
            if (node.col == self.ncols-1):
                node.show()
                print("\n")
            else:
                node.show()


    def canBridgeIslands(self, islandA:Island, islandB:Island):
        pass

    def addBridge(self, islandA:Island, islandB:Island):
        #Check direction of bridge
        if (islandA.row == islandB.row):
            direction = "horizontal"
        else:
            direction = "vertical"

        if (direction == "horizontal"):
            #Check whether going left or right
            if (islandA.col > islandB.col):
                #Going left
                self.drawBridges(islandA.col - 1, islandB.col, islandA.row, -1, direction)
            else:
                #going right
                self.drawBridges(islandA.col + 1, islandB.col, islandA.row, 1, direction)
        if (direction == "vertical"):
            if (islandA.row > islandB.row):
                #Going up
                self.drawBridges(islandA.row - 1, islandB.row, islandA.col, -1, direction)
            else:
                #going down
                self.drawBridges(islandA.row + 1, islandB.row, islandA.col, 1, direction)

        pass

    def drawBridges(self, start, end, const, step, direction):
        if (direction == "horizontal"):
            for col in range(start, end, step):
                ocean = self.getOceanAtCoord(const, col)
                if (ocean != None):
                    ocean.addBridge(Bridge(1, const, col, direction))
        else:
            for row in range(start, end, step):
                ocean = self.getOceanAtCoord(row, const)
                if (ocean != None):
                    ocean.addBridge(Bridge(1, row, const, direction))


    def isGameComplete(self):
        for node in self.gameMap:
            if(type(node) is Island and not node.isComplete()):
               return False
        return True

    # def sortIslandsByHighestConstrant(self):
    #     return sorted(self.islands, key=lambda island:(island.maxBridges - island.bridgeCount))

    def getNeighbours(self, island:Island):
        #First check x neighbours

        ##First check leftwards
        for col in range(island.col - 1, -1, -1):
            maybeIsland = self.coordIsIsland(island.row, col)
            if (maybeIsland != None and maybeIsland not in island.neighbours):
                island.neighbours.append(maybeIsland)
                break

        ##Then check rightwards
        for col in range(island.col + 1, self.ncols):
            maybeIsland = self.coordIsIsland(island.row, col)
            if (maybeIsland != None and maybeIsland not in island.neighbours):
                island.neighbours.append(maybeIsland)
                break

        #Then check y neighbours

        #First check up
        for row in range(island.row - 1, -1, -1):
            maybeIsland = self.coordIsIsland(row, island.col)
            if (maybeIsland != None and maybeIsland not in island.neighbours):
                island.neighbours.append(maybeIsland)
                break

        #Then check down
        for row in range(island.row + 1, self.nrows,):
            maybeIsland = self.coordIsIsland(row, island.col)
            if (maybeIsland != None and maybeIsland not in island.neighbours):
                island.neighbours.append(maybeIsland)
                break


    #If coord is island, return the island, otherwise return Ocean
    def coordIsIsland(self, row, col):
        for node in self.gameMap:
            if (type(node) is Island):
                if (node.row == row and node.col == col):
                    return node
        return None

    def getOceanAtCoord(self, row, col):
        for node in self.gameMap:
            if (type(node) is Ocean):
                if (node.row == row and node.col == col):
                    return node
        return None


def map_to_lists(nrows, ncols, map):
    gameMap = []
    for row in range(nrows):
        for col in range(ncols):
            if(map[row][col] == 0):
                gameMap.append(Ocean(row, col))
            else:
                gameMap.append(Island(row, col, map[row][col]))
    return gameMap

def makeGame():
    nrows, ncols, map = scan_map()
    gameMap = map_to_lists(nrows, ncols, map)

    return Game(gameMap, nrows, ncols)
