from random import randint

from ...info import GROW_CHANCE, GROW_TILES
from ...tile_systems.tile_class import Tile

def grow(tile):
    if randint(0, GROW_CHANCE[tile.kind]) == 0:
            grow_tile = GROW_TILES[tile.kind]
            tile = Tile(grow_tile[0], grow_tile[1], tile.floor, floor_health = tile.floor_health, spawn = tile.spawn)
    return tile