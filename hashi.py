# from typing import List
from helpers import Island, Ocean, Game, makeGame


game = makeGame()

print(game.isGameComplete())

sortedIslands = game.sortIslandsByHighestConstrant()

for island in sortedIslands:
    print(f"{island.maxBridges}, {island.x}, {island.y}\n")
