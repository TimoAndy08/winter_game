from ..info import TILE_ATTRIBUTES, MULTI_TILES
from .tile_class import Tile

def place_tile(kind, grid_position, chunks):
    if "multi" in TILE_ATTRIBUTES.get(kind, ()):
        width, height = MULTI_TILES[kind]
        for x in range(width):
            for y in range(height):
                chunk_pos = (grid_position[0][0] + (grid_position[1][0] + x) // 16, grid_position[0][1] + (grid_position[1][1] + y) // 16)
                tile_pos = ((grid_position[1][0] + x) % 16, (grid_position[1][1] + y) % 16)
                tile_type = "left" if y == 0 else "up"
                old_tile = chunks[chunk_pos].get(tile_pos)
                if old_tile:
                    chunks[chunk_pos][tile_pos].kind = Tile(tile_type, floor = old_tile.floor, floor_health = old_tile.floor_health, floor_unbreak = old_tile.floor_unbreak)
                else:
                    chunks[chunk_pos][tile_pos] = Tile(tile_type)
    if grid_position[1] not in chunks[grid_position[0]]:
        chunks[grid_position[0]][grid_position[1]] = Tile(kind)
    else:
        old_tile = chunks[grid_position[0]][grid_position[1]]
        chunks[grid_position[0]][grid_position[1]] = Tile(kind, floor = old_tile.floor, floor_health = old_tile.floor_health, floor_unbreak = old_tile.floor_unbreak)
    return chunks