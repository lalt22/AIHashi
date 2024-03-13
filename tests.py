from helpers import makeGame, Game, Island, Bridge

# game = Game(4, 4, [Island(0, 0, 3), Island(0,3,3), Island(3,0,3), Island(3,3,3)])
# game.show_game([], False)
# perms = game.get_permutations_to_sum(6, 3, [])

# for perm in perms:
#     print(perm)
# game.solve()

# big_game = Game(7,7, [
#     Island(0,1,2),
#     Island(0,3,5),
#     Island(0,5,2),
#     Island(1,0,1),
#     Island(1,6,1),
#     Island(2,1,1),
#     Island(2,5,1),
#     Island(4,0,4),
#     Island(4,3,8),
#     Island(4,5,3),
#     Island(6,0,2),
#     Island(6,3,4),
#     Island(6,6,2)])
# big_game.show_game([], False)

# built_bridges = [Bridge(1, "horizontal", Island(1,0,1), Island(1,6,1)), Bridge(1, "horizontal", Island(0,1,2), Island(0,3,5))]
# # new_bridge = Bridge(1, "vertical", Island(2,1,1), Island(0,1,2))
# new_bridge = Bridge(3, "vertical", Island(4,0,4), Island(1,0,1))

# print(big_game.do_bridges_intersect(new_bridge, built_bridges))

# built_bridges.append(new_bridge)

# bridge_at_pt = big_game.find_bridge_at_point(1,1, built_bridges)

# if (bridge_at_pt):
#     print(f"Bridge with weight {bridge_at_pt.count} from {bridge_at_pt.from_island.row},{bridge_at_pt.from_island.col} to {bridge_at_pt.to_island.row},{bridge_at_pt.to_island.col}")

# big_game.getNeighbours()
# big_game.solve()

'''
4 . 4 . 2
. . . . .
9 . 7 . 5
. . . . .
5 . 6 . 6

'''

# unsolvable = Game(5, 5, [
#     Island(0,0,4),
#     Island(0,2,4),
#     Island(0,4,2),
#     Island(2,0,9),
#     Island(2,2,7),
#     Island(2,4,5),
#     Island(4,0,5),
#     Island(4,2,6),
#     Island(4,4,6),
# ])

# unsolvable.show_game([], False)
# # perms = list(unsolvable.get_permutations_to_sum(9, 3, []))
# # for perm in perms:
# #     print(perm)
# # unsolvable.getNeighbours()

# # for island in unsolvable.islands:
# #     print(f"Neighbours for {island.maxBridges} at ({island.row},{island.col}) -> ", end="")
# #     for neighbour in island.neighbours:
# #         print(f"{neighbour.maxBridges}: ({neighbour.row},{neighbour.col})", end=", ")
# #     print("\n")
# # unsolvable.solve()
# unsolvable.solve()

'''
 .  .  .  .  .  .  .

 .  3  .  .  7  .  4

 .  .  .  .  .  .  .

 .  .  .  .  .  .  .

 .  8  .  .  8  .  5

 .  .  .  .  .  .  .

 .  6  .  .  7  .  6
'''

big_game = Game(7,7, [
    Island(1,1,3),
    Island(1,4,7),
    Island(1,6,4),
    Island(4,1,8),
    Island(4,4,8),
    Island(4,6,5),
    Island(6,1,6),
    Island(6,4,7),
    Island(6,6,6)
])

big_game.show_game([], False)
big_game.solve()