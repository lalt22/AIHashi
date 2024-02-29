# from typing import List
from helpers import Island, Ocean, Game, makeGame


game = makeGame()

# sortedIslands = game.sortIslandsByHighestConstrant()
game.showGame()
for node in game.gameMap:
    if (type(node) is Island):
        print(f"Checking from: {node.maxBridges}, {node.row}, {node.col}")
        game.getNeighbours(node)
        for island in node.neighbours:
            game.addBridge(node, island)
        game.showGame()
