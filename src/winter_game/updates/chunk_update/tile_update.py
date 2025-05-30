from .point import left, up
from .rabbit import rabbit_hole, rabbit_entity

def update_tile(current_tile, chunks, chunk, tile, delete_tiles, create_tiles):
    if "grow" in current_tile.attributes:
        chunks[chunk][tile] = current_tile.grow()

    elif current_tile.kind == "left":
        chunks, delete_tiles = left(chunks, chunk, tile, delete_tiles)

    elif current_tile.kind == "up":
        chunks, delete_tiles = up(chunks, chunk, tile, delete_tiles)

    elif current_tile.kind == "rabbit hole":
        chunks, create_tiles = rabbit_hole(chunks, chunk, tile, current_tile, create_tiles)

    elif "rabbit" in current_tile.attributes:
        create_tiles, delete_tiles = rabbit_entity(chunks, chunk, tile, current_tile, create_tiles, delete_tiles)
    return chunks, create_tiles, delete_tiles