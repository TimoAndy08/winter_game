from .tile_info import TOOL_REQUIRED, TOOL_EFFICIENCY
from .tile_class import Tile

def right_click(chunks, grid_position, inventory, inventory_number, INVENTORY_SIZE, max_health, tile_location, real_location, room_location, last_mined_location, machine_ui):
    if grid_position[1] in chunks[room_location][grid_position[0]]:
        damage = 1 - chunks[room_location][grid_position[0]][grid_position[1]].resistance
        if len(inventory) > inventory_number:
            inventory_key = list(inventory.keys())[inventory_number]
            inventory_words = inventory_key.split()
            if len(inventory_words) == 2 and chunks[room_location][grid_position[0]][grid_position[1]].kind in TOOL_REQUIRED:
                if TOOL_REQUIRED[chunks[room_location][grid_position[0]][grid_position[1]].kind] == inventory_words[1]:
                    damage += TOOL_EFFICIENCY[inventory_words[0]]
        chunks[room_location][grid_position[0]][grid_position[1]].health -= max(damage, 0)
        last_mined_location = [grid_position[0][0], grid_position[0][1], grid_position[1][0], grid_position[1][1]]
        if chunks[room_location][grid_position[0]][grid_position[1]].health <= 0:
            if chunks[room_location][grid_position[0]][grid_position[1]].kind != "player":
                junk_inventory = {}
                if not "no_pickup" in chunks[room_location][grid_position[0]][grid_position[1]].attributes:
                    chunks[room_location][grid_position[0]][grid_position[1]].inventory[chunks[room_location][grid_position[0]][grid_position[1]].kind] = chunks[room_location][grid_position[0]][grid_position[1]].inventory.get(chunks[room_location][grid_position[0]][grid_position[1]].kind, 0) + 1
                for item, amount in chunks[room_location][grid_position[0]][grid_position[1]].inventory.items():
                    if item in chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory:
                        chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item] += amount
                        if inventory[item] > 64:
                            junk_inventory[item] = chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item] - 64
                            chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item] = 64
                    else:
                        if len(inventory) < INVENTORY_SIZE:
                            chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item] = amount
                        else:
                            junk_inventory[item] = amount
                if "enter" in chunks[room_location][grid_position[0]][grid_position[1]].attributes and (*grid_position[0], *grid_position[1]) in chunks:
                    del chunks[(*grid_position[0], *grid_position[1])]
                del chunks[room_location][grid_position[0]][grid_position[1]]
                if len(junk_inventory) > 0:
                    chunks[room_location][grid_position[0]][grid_position[1]] = Tile("junk", 1, 0, junk_inventory)
                machine_ui = "game"
            else:
                chunks[room_location][grid_position[0]][grid_position[1]] = Tile("corpse", 1, 0, inventory)
                i = 0
                while (i % 16, i // 16) in chunks[()][(0, 0)]:
                    i += 1
                    if i == 256:
                        i = 0
                        break
                chunks[()][(0, 0)][(i % 16, i // 16)] = Tile("player", max_health, 0, {})
                tile_location = [0, 0, i % 16, i // 16]
                real_location = [0, 0, i % 16, i // 16]
                room_location = ()
    return (chunks, tile_location, real_location, room_location, last_mined_location, machine_ui)