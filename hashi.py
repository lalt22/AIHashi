#!/usr/bin/python3
from helpers import makeGame
import timeit

game = makeGame()
# time = timeit.timeit(stmt=game.solve_it(game.islands,[]))
game.solve()
# game.show_game()
