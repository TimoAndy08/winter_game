from random import randint, choice

from ..tile_systems.tile_class import Tile
from ..game_state import Game_State

def find_empty_place(tile, chunk, chunks):
    empty_places = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            tile_pos = ((tile[0] + x) % 16, (tile[1] + y) % 16)
            chunk_pos = (chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16)
            if tile_pos not in chunks.get(chunk_pos, {}) or chunks[chunk_pos][tile_pos].kind is None:
                empty_places.append((x, y))
    return choice(empty_places) if empty_places else None

def update_tiles(state: Game_State, chunks):
    delete_tiles = []
    create_tiles = []
    tile_location = state.location["tile"]

    for chunk_dx in range(-3, 4):
        for chunk_dy in range(-3, 4):
            chunk = (chunk_dx + tile_location[0], chunk_dy + tile_location[1])
            if chunk in chunks:
                for tile in list(chunks[chunk]):
                    current_tile = chunks[chunk][tile]

                    if isinstance(current_tile.kind, str):
                        if "grow" in current_tile.attributes:
                            chunks[chunk][tile] = current_tile.grow()

                        elif current_tile.kind == "left":
                            left_chunk = (chunk[0] + (tile[0] - 1) // 16, chunk[1])
                            left_tile = ((tile[0] - 1) % 16, tile[1])
                            if left_tile not in chunks.get(left_chunk, {}):
                                delete_tiles.append((chunk, tile))
                            elif chunks[left_chunk][left_tile].kind is None:
                                chunks[chunk][tile].kind = None

                        elif current_tile.kind == "up":
                            up_chunk = (chunk[0], chunk[1] + (tile[1] - 1) // 16)
                            up_tile = (tile[0], (tile[1] - 1) % 16)
                            if up_tile not in chunks.get(up_chunk, {}):
                                delete_tiles.append((chunk, tile))
                            elif chunks[up_chunk][up_tile].kind is None:
                                chunks[chunk][tile].kind = None

                        elif current_tile.kind == "rabbit hole" and randint(0, 10000) == 0:
                            spawn_pos = (chunk[0] * 16 + tile[0], chunk[1] * 16 + tile[1])
                            animal = choice((
                                Tile("rabbit adult", {"rabbit meat": 2, "rabbit fur": 1}, spawn=spawn_pos),
                                Tile("rabbit child", spawn=spawn_pos)
                            ))
                            if animal.kind in current_tile.inventory:
                                empty = find_empty_place(tile, chunk, chunks)
                                if empty:
                                    x, y = empty
                                    current_tile.inventory[animal.kind] -= 1
                                    if current_tile.inventory[animal.kind] <= 0:
                                        del current_tile.inventory[animal.kind]
                                    create_tiles.append((
                                        (chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16),
                                        ((tile[0] + x) % 16, (tile[1] + y) % 16),
                                        animal
                                    ))

                        elif "rabbit" in current_tile.attributes and randint(0, 100) == 0:
                            empty = find_empty_place(tile, chunk, chunks)
                            if empty:
                                x, y = empty
                                if abs(chunk[0] * 16 + tile[0] + x - current_tile.spawn[0]) <= 8 and \
                                   abs(chunk[1] * 16 + tile[1] + y - current_tile.spawn[1]) <= 8:
                                    create_tiles.append((
                                        (chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16),
                                        ((tile[0] + x) % 16, (tile[1] + y) % 16),
                                        Tile(
                                            current_tile.kind,
                                            current_tile.inventory,
                                            health=current_tile.health,
                                            max_health=current_tile.max_health,
                                            spawn=current_tile.spawn
                                        )
                                    ))
                                    delete_tiles.append((chunk, tile))

    for chunk_pos, tile_pos, tile_data in create_tiles:
        chunk_tiles = chunks.setdefault(chunk_pos, {})
        if tile_pos in chunk_tiles:
            current_tile = chunk_tiles[tile_pos]
            tile_data.floor = current_tile.floor
            tile_data.floor_health = current_tile.floor_health
            tile_data.floor_unbreak = current_tile.floor_unbreak
        chunk_tiles[tile_pos] = tile_data

    for chunk_pos, tile_pos in delete_tiles:
        tile = chunks[chunk_pos][tile_pos]
        if tile.floor is not None:
            chunks[chunk_pos][tile_pos] = Tile(
                floor=tile.floor,
                floor_health=tile.floor_health,
                floor_unbreak=tile.floor_unbreak
            )
        else:
            del chunks[chunk_pos][tile_pos]
    return chunks