from random import random


def structure_dungeon(dungeon = [], tile = (0, 0), origin = (0, 0), distanse = 0):
    dungeon.append(tile)
    for pos in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        if random() < 0.9 ** distanse and (tile[0] + pos[0], tile[1] + pos[1]) not in dungeon:
            structure_dungeon(dungeon, (tile[0] + pos[0], tile[1] + pos[1]), origin, distanse + 1)
    return dungeon