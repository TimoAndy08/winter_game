from ...tile_systems.room_generation import generate_room
from ...tile_systems.tile_class import Tile
from ...info import ROOMS

def enter_room(location, grid_position, chunks, health, max_health, inventory):
    location["room"] = (*grid_position[0], *grid_position[1],)
    location["real"] = [0, 0, 0, 0]
    location["mined"] = ((0, 0), (0, 0))
    if location["room"] in chunks:
        chunks[location["room"]][0, 0][0, 0] = Tile("player", inventory, chunks[location["room"]][0, 0][0, 0].floor, health, max_health, chunks[location["room"]][0, 0][0, 0].floor_health, chunks[location["room"]][0, 0][0, 0].floor_unbreak)
        chunks[0, 0, 0, 0][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]] = Tile(floor = chunks[0, 0, 0, 0][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].floor)
        location["tile"] = [0, 0, 0, 0]
    else:
        room_generating = ROOMS[chunks[0, 0, 0, 0][grid_position[0]][grid_position[1]].kind]
        chunks[location["room"]] = {}
        for room_info in room_generating:
            room = generate_room(room_info[0], room_info[1], room_info[2], room_info[3])
            for chunk_pos in room:
                if chunk_pos not in chunks[location["room"]]:
                    chunks[location["room"]][chunk_pos] = {}
                for tile_pos in room[chunk_pos]:
                    chunks[location["room"]][chunk_pos][tile_pos] = room[chunk_pos][tile_pos]
        chunks[location["room"]][0, 0][0, 0] = Tile("player", inventory, chunks[location["room"]][0, 0][0, 0].floor, health, max_health, chunks[location["room"]][0, 0][0, 0].floor_health, chunks[location["room"]][0, 0][0, 0].floor_unbreak)
        chunks[0, 0, 0, 0][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])] = Tile(floor = chunks[0, 0, 0, 0][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].floor)
        location["tile"] = [0, 0, 0, 0]
    return chunks, location