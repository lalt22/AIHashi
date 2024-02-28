from typing import List
from scan_print_map import scan_map

class Node:
    def __init__(self, x:int, y:int, maxBridges:int):
        self.x = x
        self.y = y
        self.maxBridges = maxBridges
        self.bridgeCount = 0

    def addBridge(self, otherNode):
        self.bridgeCount+=1
        pass

    def isComplete(self):
        if (self.bridgeCount == self.maxBridges):
            return True
        return False


class Game:
    def __init__(self, nodes:List[Node]):
        self.nodes = nodes

    def getConnections(self, node:Node):
        pass


    def canBridgeIslands(self, nodeA:Node, nodeB:Node):
        pass

    def addBridge(self, nodeA:Node, nodeB:Node):
        pass

    def isGameComplete(self):
        for node in self.nodes:
            if(not node.isComplete()):
               return False
        return True

nrows, ncols, map = scan_map()
print(map)