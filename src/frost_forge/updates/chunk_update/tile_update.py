from random import randint

from .point import left, up
from .rabbit import rabbit_hole, rabbit_entity
from .machine import machine
from ...info import GROW_CHANCE, GROW_TILES
from ...tile_systems.tile_class import Tile

def update_tile(current_tile, chunks, chunk, tile, delete_tiles, create_tiles, tick):
    if "grow" in current_tile.attributes:
        if randint(0, GROW_CHANCE[current_tile.kind]) == 0:
            grow_tile = GROW_TILES[current_tile.kind]
            chunks[chunk][tile] = Tile(grow_tile[0], grow_tile[1], current_tile.floor, floor_health = current_tile.floor_health, floor_unbreak = current_tile.floor_unbreak, spawn = current_tile.spawn)
    elif current_tile.kind == "left":
        chunks, delete_tiles = left(chunks, chunk, tile, delete_tiles)
    elif current_tile.kind == "up":
        chunks, delete_tiles = up(chunks, chunk, tile, delete_tiles)
    elif current_tile.kind == "rabbit hole":
        chunks, create_tiles = rabbit_hole(chunks, chunk, tile, current_tile, create_tiles)
    elif "rabbit" in current_tile.attributes:
        create_tiles, delete_tiles = rabbit_entity(chunks, chunk, tile, current_tile, create_tiles, delete_tiles)
    elif "machine" in current_tile.attributes:
        chunks = machine(chunks, chunk, tile, current_tile, tick)
    return chunks, create_tiles, delete_tiles