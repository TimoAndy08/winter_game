from random import randint

from ...info import GROW_CHANCE, GROW_TILES, HEALTH

def grow(tile):
    if randint(0, GROW_CHANCE[tile["kind"]]) == 0:
        floor = tile["floor"]
        if "spawn" in tile:
            spawn = tile["spawn"]
            tile = GROW_TILES[tile["kind"]]
            tile["spawn"] = spawn
        else:
            tile = GROW_TILES[tile["kind"]]
        tile["floor"] = floor
    return tile