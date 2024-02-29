# import sys
# import numpy as np
# import random

# MAX_ROW = 100
# MAX_COL = 100
# MAX_HUB = 500
# MAX_BRIDGE = 1000

# NONE = -1
# HORIZONTAL = 0
# VERTICAL = 1

# EAST = 0
# NORTH = 1
# WEST = 2
# SOUTH = 3


# ### PRINT THE INPUT MAP
# def print_map(numRows, numCols, hashiArr):
#     for i in range(numRows):
#         for j in range(numCols):
#             if (hashiArr[i][j] > 0 and hashiArr[i][j] <= 9):
#                 print(" {value} ".format(value=hashiArr[i][j]),  end="")
#             else: print(" . ", end="")
#         print("\n")

# ### RETURN TRUE IF (x,y) IS NEXT TO AN EXISTING ISLAND
# def island_neighbour(x, y, numRows, numCols, hashiArr):
#     if ((y < numCols-1 and hashiArr[x][y+1] > 0)
#         or (x > 0 and hashiArr[x-1][y] > 0)
#         or (y > 0 and hashiArr[x][y-1] > 0)
#         or (x < numRows-1 and hashiArr[x+1][y] > 0)
#     ):
#         return True
#     else: return False

# ### FIND A RANDOM START AND END LOCATION TO ADD A NEW BRIDGE
# def add_bridge(mapEmpty, numRows, numCols, maxPlanks, hashiArr, dirn, numPlank):
#     return "poo"

# hashiArr = [[random.randint(0, 9) for _ in range(MAX_COL)] for _ in range(MAX_ROW)]
# # print(hashiArr)
# # print_map(3, 4, hashiArr)
# print_map(10, 10, hashiArr)