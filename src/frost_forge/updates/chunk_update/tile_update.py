from .point import left, up
from .entity_behaviour import move_entity
from .machine import machine
from .growth import grow
from ...info import ATTRIBUTES, GROW_TILES


def update_tile(current_tile, chunks, chunk, tile, delete_tiles, create_tiles, tick, location):
    if current_tile["kind"] in GROW_TILES:
        chunks[chunk][tile] = grow(current_tile)
        if chunks[chunk][tile] == {}:
            delete_tiles.append((chunk, tile))
    elif current_tile["kind"] == "left":
        chunks, delete_tiles = left(chunks, chunk, tile, delete_tiles)
    elif current_tile["kind"] == "up":
        chunks, delete_tiles = up(chunks, chunk, tile, delete_tiles)
    elif "rabbit" in ATTRIBUTES.get(current_tile["kind"], ()):
        create_tiles, delete_tiles = move_entity(chunks, chunk, tile, current_tile, create_tiles, delete_tiles, 0, location)
    elif "machine" in ATTRIBUTES.get(current_tile["kind"], ()):
        chunks = machine(chunks, chunk, tile, current_tile, tick)
    return chunks, create_tiles, delete_tiles