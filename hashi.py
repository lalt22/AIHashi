# from typing import List
from helpers import Island, Ocean, Game, makeGame


game = makeGame()

game.showGame()
for node in game.gameMap:
    if (type(node) is Island):
        print(f"Checking from: {node.maxBridges}, {node.row}, {node.col}")
        game.getNeighbours(node)
        for island in node.neighbours:
            print(f"Old bridge counts:\n {node.maxBridges}: {node.row}, {node.col} = {node.bridgeCount}\n {island.maxBridges}: {island.row}, {island.col} = {island.bridgeCount}")
            if (node.bridgeCount + 3 <= node.maxBridges and island.bridgeCount + 3 <= island.maxBridges):
                game.addBridge(node, island, 3)
                print(f"New bridge counts:\n {node.maxBridges}: {node.row}, {node.col} = {node.bridgeCount}\n {island.maxBridges}: {island.row}, {island.col} = {island.bridgeCount}")
            elif (node.bridgeCount + 2 <= node.maxBridges and island.bridgeCount + 2 <= island.maxBridges):
                game.addBridge(node, island, 2)
            elif (node.bridgeCount + 1 <= node.maxBridges and island.bridgeCount + 1 <= island.maxBridges):
                game.addBridge(node, island, 1)
        game.showGame()
