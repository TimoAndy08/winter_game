from random import randint, choice

from .tile_class import Tile

def find_empty_place(tile, chunk, chunks):
    empty_places = []
    for x in range(-1, 2):
        for y in range(-1, 2):
            tile_pos = ((tile[0] + x) % 16, (tile[1] + y) % 16)
            chunk_pos = (chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16)
            if tile_pos not in chunks[chunk_pos] or chunks[chunk_pos][tile_pos].kind == None:
                empty_places.append((x, y))
    if len(empty_places) >= 1:
        return choice(empty_places)
    return None

def update_tiles(chunks, tile_location, room_location):
    delete_tiles = []
    create_tiles = []
    for chunk_x in range(-3, 4):
        for chunk_y in range(-3, 4):
            chunk = (chunk_x + tile_location[0], chunk_y + tile_location[1])
            if chunk in chunks[room_location]:
                for tile in chunks[room_location][chunk]:
                    current_tile = chunks[room_location][chunk][tile]
                    if isinstance(current_tile.kind, str):
                        if "grow" in current_tile.attributes:
                            chunks[room_location][chunk][tile] = current_tile.grow()
                        elif current_tile.kind == "left":
                            if ((tile[0] - 1) % 16, tile[1]) not in chunks[room_location][chunk[0] + (tile[0] - 1) // 16, chunk[1]]:
                                delete_tiles.append((chunk, tile))
                            elif chunks[room_location][chunk[0] + (tile[0] - 1) // 16, chunk[1]][(tile[0] - 1) % 16, tile[1]].kind == None:
                                chunks[room_location][chunk][tile].kind = None
                        elif current_tile.kind == "up":
                            if ((tile[0], (tile[1] - 1) % 16)) not in chunks[room_location][chunk[0], chunk[1] + (tile[1] - 1) // 16]:
                                delete_tiles.append((chunk, tile))
                            elif chunks[room_location][chunk[0], chunk[1] + (tile[1] - 1) // 16][tile[0], (tile[1] - 1) % 16].kind == None:
                                chunks[room_location][chunk][tile].kind = None
                        elif current_tile.kind == "rabbit hole":
                            if randint(0, 10000) == 0:
                                animal = choice((Tile("rabbit adult", {"rabbit meat": 2, "rabbit fur": 1}, spawn = (chunk[0] * 16 + tile[0], chunk[1] * 16 + tile[1])), Tile("rabbit child", spawn = (chunk[0] * 16 + tile[0], chunk[1] * 16 + tile[1]))))
                                if animal.kind in current_tile.inventory:
                                    empty_place = find_empty_place(tile, chunk, chunks[room_location])
                                    if empty_place != None:
                                        x, y = empty_place
                                        current_tile.inventory[animal.kind] -= 1
                                        if current_tile.inventory[animal.kind] <= 0:
                                            del current_tile.inventory[animal.kind]
                                        create_tiles.append(((chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16), ((tile[0] + x) % 16, (tile[1] + y) % 16), animal))
                        elif "rabbit" in current_tile.attributes:
                            if randint(0, 100) == 0:
                                empty_place = find_empty_place(tile, chunk, chunks[room_location])
                                if empty_place != None:
                                    x, y = empty_place
                                    if abs(chunk[0] * 16 + tile[0] + x - current_tile.spawn[0]) <= 8 and abs(chunk[1] * 16 + tile[1] + y - current_tile.spawn[1]) <= 8:
                                        create_tiles.append(((chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16), ((tile[0] + x) % 16, (tile[1] + y) % 16), Tile(current_tile.kind, current_tile.inventory, health = current_tile.health, max_health = current_tile.max_health, spawn = current_tile.spawn)))
                                        delete_tiles.append((chunk, tile))
    for chunk_pos, tile_pos, tile_data in create_tiles:
        if tile_pos in chunks[room_location][chunk_pos]:
            current_tile = chunks[room_location][chunk_pos][tile_pos]
            floor_info = (current_tile.floor, current_tile.floor_health, current_tile.floor_unbreak)
            chunks[room_location][chunk_pos][tile_pos] = tile_data
            chunks[room_location][chunk_pos][tile_pos].floor = floor_info[0]
            chunks[room_location][chunk_pos][tile_pos].floor_health = floor_info[1]
            chunks[room_location][chunk_pos][tile_pos].floor_unbreak = floor_info[2]
        else:
            chunks[room_location][chunk_pos][tile_pos] = tile_data
    for chunk_pos, tile_pos in delete_tiles:
        if chunks[room_location][chunk_pos][tile_pos].floor != None:
            current_tile = chunks[room_location][chunk_pos][tile_pos]
            floor_info = (current_tile.floor, current_tile.floor_health, current_tile.floor_unbreak)
            chunks[room_location][chunk_pos][tile_pos] = Tile(floor = floor_info[0], floor_health = floor_info[1], floor_unbreak = floor_info[2])
        else:
            del chunks[room_location][chunk_pos][tile_pos]
    return chunks
