from .tile_info import TILE_ATTRIBUTES, MULTI_TILES, FOOD, STORAGE, RECIPES
from .tile_class import Tile
from .room_generation import generate_room
from .crafting_system import recipe

def left_click(machine_ui, grid_position, chunks, inventory_number, health, max_health, DAY_LENGTH, position, SCREEN_SIZE, UI_SCALE, INVENTORY_SIZE, recipe_number, tile_location, real_location, last_mined_location, room_location, last_opened_location, inventory):
    if machine_ui == "game":
        if grid_position[1] not in chunks[room_location][grid_position[0]]:
            if len(inventory) > inventory_number:
                can_place = True
                inventory_key = list(inventory.keys())[inventory_number]
                if "eat" in TILE_ATTRIBUTES.get(inventory_key, ()):
                    if health < max_health:
                        chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].health = min(health + FOOD[inventory_key], max_health)
                        can_place = False
                        inventory[inventory_key] -= 1
                        if inventory[inventory_key] == 0:
                            del inventory[inventory_key]
                if "multi" in TILE_ATTRIBUTES.get(inventory_key, ()):
                    for x in range(0, MULTI_TILES[inventory_key][0]):
                        for y in range(0, MULTI_TILES[inventory_key][1]):
                            if ((grid_position[1][0] + x) % 16, (grid_position[1][1] + y) % 16) in chunks[room_location][(grid_position[0][0] + (grid_position[1][0] + x) // 16, grid_position[0][1] + (grid_position[1][1] + y) // 16)]:
                                can_place = False
                if can_place:
                    inventory[inventory_key] -= 1
                    if "multi" in TILE_ATTRIBUTES.get(inventory_key, ()):
                        for x in range(0, MULTI_TILES[inventory_key][0]):
                            chunks[room_location][(grid_position[0][0] + (grid_position[1][0] + x) // 16, grid_position[0][1])][((grid_position[1][0] + x) % 16, grid_position[1][1])] = Tile("left", 1, 1, {})
                            for y in range(1, MULTI_TILES[inventory_key][1]):
                                chunks[room_location][(grid_position[0][0] + (grid_position[1][0] + x) // 16, grid_position[0][1] + (grid_position[1][1] + y) // 16)][((grid_position[1][0] + x) % 16, (grid_position[1][1] + y) % 16)] = Tile("up", 1, 1, {})
                    chunks[room_location][grid_position[0]][grid_position[1]] = Tile(inventory_key, 4, 0, {})
                    if inventory[inventory_key] == 0:
                        del inventory[inventory_key]
        elif "open" in chunks[room_location][grid_position[0]][grid_position[1]].attributes:
            machine_ui = chunks[room_location][grid_position[0]][grid_position[1]].kind
            last_opened_location = (grid_position[0], grid_position[1])
        elif "enter" in chunks[room_location][grid_position[0]][grid_position[1]].attributes and room_location == ():
            room_location = (*grid_position[0], *grid_position[1],)
            real_location = [0, 0, 0, 0]
            last_mined_location = [0, 0, 0, 0]
            if room_location in chunks:
                chunks[room_location][(0, 0)][(0, 0)] = chunks[()][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                del chunks[()][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                tile_location = [0, 0, 0, 0]
            else:
                if chunks[()][grid_position[0]][grid_position[1]].kind == "wooden cabin":
                    chunks[room_location] = generate_room("wood", (-5, -4), (8, 6))
                    chunks[room_location][(0, 0)][(0, 1)] = Tile("wooden door", 1, 1, {})
                    chunks[room_location][(0, 0)][(0, 0)] = chunks[()][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                    del chunks[()][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                    tile_location = [0, 0, 0, 0]
        elif "exit" in chunks[room_location][grid_position[0]][grid_position[1]].attributes:
            chunks[()][(room_location[0] + (room_location[2] - 1) // 16, room_location[1])][((room_location[2] - 1) % 16, room_location[3])] = chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
            del chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
            i = -1
            real_location = [room_location[0] + (room_location[2] + i) // 16, room_location[1], (room_location[2] + i) % 16, room_location[3]]
            tile_location = [*real_location,]
            last_mined_location = [*real_location,]
            room_location = ()
            machine_ui = "game"
        elif "sleep" in chunks[room_location][grid_position[0]][grid_position[1]].attributes:
            if 9 / 16 <= (tick / DAY_LENGTH) % 1 < 15 / 16:
                tick = (tick // DAY_LENGTH + 9 / 16) * DAY_LENGTH
    elif "store" in TILE_ATTRIBUTES.get(machine_ui, ()):
        position[0] -= SCREEN_SIZE[0] // 2
        machine_inventory = chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory
        if position[1] >= SCREEN_SIZE[1] - 32 * UI_SCALE and abs(position[0]) <= 16 * INVENTORY_SIZE * UI_SCALE:
            slot_number = (position[0] - 16 * UI_SCALE * (INVENTORY_SIZE % 2)) // (32 * UI_SCALE) + INVENTORY_SIZE // 2 + INVENTORY_SIZE % 2
            if slot_number < len(inventory):
                item = list(inventory.items())[slot_number]
                machine_item = machine_inventory.get(item[0], 0)
                if not (machine_item == 0 and len(machine_inventory) == STORAGE[machine_ui][0]):
                    if machine_item + item[1] <= STORAGE[machine_ui][1]:
                        chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory[item[0]] = machine_item + item[1]
                        del chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item[0]]
                    else:
                        chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory[item[0]] = STORAGE[machine_ui][1]
                        chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item[0]] = machine_item + item[1] - STORAGE[machine_ui][1]
        elif SCREEN_SIZE[1] - 144 * UI_SCALE <= position[1] <= SCREEN_SIZE[1] - 80 * UI_SCALE and abs(position[0]) <= 112 * UI_SCALE:
            slot_number = (position[0] + 112 * UI_SCALE) // (32 * UI_SCALE) + (position[1] - SCREEN_SIZE[1] + 144 * UI_SCALE) // (32 * UI_SCALE) * 7
            if slot_number < len(machine_inventory):
                item = list(machine_inventory.items())[slot_number]
                inventory_item = inventory.get(item[0], 0)
                if not (inventory_item == 0 and len(inventory) == INVENTORY_SIZE):
                    if inventory_item + item[1] <= 64:
                        chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item[0]] = inventory_item + item[1]
                        del chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory[item[0]]
                    else:
                        chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item[0]] = 64
                        chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory[item[0]] = inventory_item + item[1] - 64
    elif "craft" in TILE_ATTRIBUTES.get(machine_ui, ()):
        inventory = recipe(RECIPES[machine_ui][recipe_number][0], RECIPES[machine_ui][recipe_number][1], inventory, (INVENTORY_SIZE, 64))
    return (machine_ui, chunks, tile_location, real_location, last_mined_location, room_location, last_opened_location)