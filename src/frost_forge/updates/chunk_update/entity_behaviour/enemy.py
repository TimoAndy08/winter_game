from .entity_movement import move_entity


def enemy(chunks, chunk, tile, current_tile, create_tiles, delete_tiles, location):
    create_tiles, delete_tiles = move_entity(
        chunks, chunk, tile, current_tile, create_tiles, delete_tiles, 1, location
    )
    return create_tiles, delete_tiles
