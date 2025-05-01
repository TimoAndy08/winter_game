from .tile_info import TILE_ATTRIBUTES, MULTI_TILES, FOOD, STORAGE, RECIPES, UNBREAK_TILES, FLOOR
from .tile_class import Tile
from .room_generation import generate_room
from .crafting_system import recipe
from .ui_rendering import UI_SCALE, INVENTORY_SIZE
from .tile_rendering import DAY_LENGTH, SCREEN_SIZE

def left_click(
    machine_ui: str,
    grid_position: list[int, int],
    chunks,
    inventory_number: int,
    health: int,
    max_health: int,
    position,
    recipe_number: int,
    location: dict[str],
    inventory: dict[str, int],
    machine_inventory: dict[str, int],
    tick: int,
):
    if machine_ui == "game":
        is_not_tile = (grid_position[1] not in chunks[location["room"]][grid_position[0]])
        player_tile = chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]]
        if not is_not_tile:
            is_empty_kind = not isinstance(chunks[location["room"]][grid_position[0]][grid_position[1]].kind, str)
        else:
            is_empty_kind = False
        if is_not_tile or is_empty_kind:
            if len(inventory) > inventory_number:
                can_place = True
                inventory_key = list(inventory.keys())[inventory_number]
                if inventory_key in UNBREAK_TILES[chunks[(0, 0, 0, 0)][(location["room"][0], location["room"][1])][(location["room"][2], location["room"][3])].kind]:
                    can_place = False
                if inventory_key not in FLOOR:
                    if is_not_tile or is_empty_kind:
                        if "eat" in TILE_ATTRIBUTES.get(inventory_key, ()):
                            if health < max_health:
                                chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                                    (location["tile"][2], location["tile"][3])
                                ].health = min(health + FOOD[inventory_key], max_health)
                                can_place = False
                                inventory[inventory_key] -= 1
                        if "multi" in TILE_ATTRIBUTES.get(inventory_key, ()):
                            for x in range(0, MULTI_TILES[inventory_key][0]):
                                for y in range(0, MULTI_TILES[inventory_key][1]):
                                    if ((grid_position[1][0] + x) % 16, (grid_position[1][1] + y) % 16) in chunks[location["room"]][(grid_position[0][0] + (grid_position[1][0] + x) // 16, grid_position[0][1] + (grid_position[1][1] + y) // 16)] and isinstance(chunks[location["room"]][(grid_position[0][0] + (grid_position[1][0] + x) // 16, grid_position[0][1] + (grid_position[1][1] + y) // 16)][((grid_position[1][0] + x) % 16, (grid_position[1][1] + y) % 16)].kind, str):
                                        can_place = False
                        if can_place:
                            inventory[inventory_key] -= 1
                            if "multi" in TILE_ATTRIBUTES.get(inventory_key, ()):
                                for x in range(0, MULTI_TILES[inventory_key][0]):
                                    chunks[location["room"]][
                                        (
                                            grid_position[0][0]
                                            + (grid_position[1][0] + x) // 16,
                                            grid_position[0][1],
                                        )
                                    ][
                                        ((grid_position[1][0] + x) % 16, grid_position[1][1])
                                    ] = Tile("left")
                                    for y in range(1, MULTI_TILES[inventory_key][1]):
                                        chunks[location["room"]][
                                            (
                                                grid_position[0][0]
                                                + (grid_position[1][0] + x) // 16,
                                                grid_position[0][1]
                                                + (grid_position[1][1] + y) // 16,
                                            )
                                        ][
                                            (
                                                (grid_position[1][0] + x) % 16,
                                                (grid_position[1][1] + y) % 16,
                                            )
                                        ] = Tile("up")
                            if is_not_tile:
                                chunks[location["room"]][grid_position[0]][grid_position[1]] = Tile(inventory_key)
                            else:
                                chunks[location["room"]][grid_position[0]][grid_position[1]] = Tile(inventory_key, floor = chunks[location["room"]][grid_position[0]][grid_position[1]].floor)
                elif is_not_tile:
                    inventory[inventory_key] -= 1
                    chunks[location["room"]][grid_position[0]][grid_position[1]] = Tile(floor = inventory_key)
                if inventory[inventory_key] == 0:
                    del inventory[inventory_key]
        elif (
            "open"
            in chunks[location["room"]][grid_position[0]][grid_position[1]].attributes
        ):
            machine_ui = chunks[location["room"]][grid_position[0]][grid_position[1]].kind
            location["opened"] = (grid_position[0], grid_position[1])
            if "store" in chunks[location["room"]][grid_position[0]][grid_position[1]].attributes:
                machine_inventory = chunks[location["room"]][grid_position[0]][grid_position[1]].inventory
        elif "enter" in chunks[location["room"]][grid_position[0]][grid_position[1]].attributes and location["room"] == (0, 0, 0, 0):
            location["room"] = (*grid_position[0], *grid_position[1],)
            location["real"] = [0, 0, 0, 0]
            location["mined"] = ((0, 0), (0, 0))
            if location["room"] in chunks:
                chunks[location["room"]][0, 0][0, 0] = Tile("player", inventory, chunks[location["room"]][0, 0][0, 0].floor, health, max_health, chunks[location["room"]][0, 0][0, 0].floor_health, chunks[location["room"]][0, 0][0, 0].floor_break)
                chunks[0, 0, 0, 0][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]] = Tile(floor = chunks[0, 0, 0, 0][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].floor)
                location["tile"] = [0, 0, 0, 0]
            else:
                if chunks[0, 0, 0, 0][grid_position[0]][grid_position[1]].kind == "wooden cabin":
                    chunks[location["room"]] = generate_room("wood", (-5, -4), (8, 6), "wood floor")
                    chunks[location["room"]][0, 0][0, 1] = Tile("wooden door")
                elif chunks[0, 0, 0, 0][grid_position[0]][grid_position[1]].kind == "mushroom hut":
                    chunks[location["room"]] = generate_room("mushroom block", (-3, -2), (5, 4))
                    chunks[location["room"]][0, 0][0, 1] = Tile("wooden door")
                    chunks[location["room"]][-1, -1][14, 15] = Tile("mushroom shaper")
                chunks[location["room"]][0, 0][0, 0] = Tile("player", inventory, chunks[location["room"]][0, 0][0, 0].floor, health, max_health, chunks[location["room"]][0, 0][0, 0].floor_health, chunks[location["room"]][0, 0][0, 0].floor_break)
                chunks[0, 0, 0, 0][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])] = Tile(floor = chunks[0, 0, 0, 0][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].floor)
                location["tile"] = [0, 0, 0, 0]
        elif "exit" in chunks[location["room"]][grid_position[0]][grid_position[1]].attributes:
            chunks[0, 0, 0, 0][0, 0][0, 2] = Tile("player", inventory, "void", health, max_health)
            chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]] = Tile(floor = player_tile.floor, floor_health = player_tile.floor_health, floor_break = player_tile.floor_break)
            location["real"] = [0, 0, 0, 2]
            location["tile"] = [*location["real"],]
            location["mined"] = ((0, 0), (0, 2))
            location["room"] = (0, 0, 0, 0)
            machine_ui = "game"
        elif (
            "sleep"
            in chunks[location["room"]][grid_position[0]][grid_position[1]].attributes
        ):
            if 9 / 16 <= (tick / DAY_LENGTH) % 1 < 15 / 16:
                tick = (tick // DAY_LENGTH + 9 / 16) * DAY_LENGTH
    elif "store" in TILE_ATTRIBUTES.get(machine_ui, ()):
        position[0] -= SCREEN_SIZE[0] // 2
        machine_inventory = chunks[location["room"]][location["opened"][0]][
            location["opened"][1]
        ].inventory
        if (
            position[1] >= SCREEN_SIZE[1] - 32 * UI_SCALE
            and abs(position[0]) <= 16 * INVENTORY_SIZE * UI_SCALE
        ):
            slot_number = (
                (position[0] - 16 * UI_SCALE * (INVENTORY_SIZE % 2)) // (32 * UI_SCALE)
                + INVENTORY_SIZE // 2
                + INVENTORY_SIZE % 2
            )
            if slot_number < len(inventory):
                item = list(inventory.items())[slot_number]
                machine_item = machine_inventory.get(item[0], 0)
                if not (
                    machine_item == 0
                    and len(machine_inventory) == STORAGE[machine_ui][0]
                ):
                    if machine_item + item[1] <= STORAGE[machine_ui][1]:
                        chunks[location["room"]][location["opened"][0]][
                            location["opened"][1]
                        ].inventory[item[0]] = machine_item + item[1]
                        del chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                            (location["tile"][2], location["tile"][3])
                        ].inventory[item[0]]
                    else:
                        chunks[location["room"]][location["opened"][0]][
                            location["opened"][1]
                        ].inventory[item[0]] = STORAGE[machine_ui][1]
                        chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                            (location["tile"][2], location["tile"][3])
                        ].inventory[item[0]] = (
                            machine_item + item[1] - STORAGE[machine_ui][1]
                        )
        elif (
            SCREEN_SIZE[1] - 144 * UI_SCALE
            <= position[1]
            <= SCREEN_SIZE[1] - 80 * UI_SCALE
            and abs(position[0]) <= 112 * UI_SCALE
        ):
            slot_number = (position[0] + 112 * UI_SCALE) // (32 * UI_SCALE) + (
                position[1] - SCREEN_SIZE[1] + 144 * UI_SCALE
            ) // (32 * UI_SCALE) * 7
            if slot_number < len(machine_inventory):
                item = list(machine_inventory.items())[slot_number]
                inventory_item = inventory.get(item[0], 0)
                if not (inventory_item == 0 and len(inventory) == INVENTORY_SIZE):
                    if inventory_item + item[1] <= 64:
                        chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                            (location["tile"][2], location["tile"][3])
                        ].inventory[item[0]] = inventory_item + item[1]
                        del chunks[location["room"]][location["opened"][0]][
                            location["opened"][1]
                        ].inventory[item[0]]
                    else:
                        chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                            (location["tile"][2], location["tile"][3])
                        ].inventory[item[0]] = 64
                        chunks[location["room"]][location["opened"][0]][
                            location["opened"][1]
                        ].inventory[item[0]] = inventory_item + item[1] - 64
    elif "craft" in TILE_ATTRIBUTES.get(machine_ui, ()):
        inventory = recipe(
            RECIPES[machine_ui][recipe_number][0],
            RECIPES[machine_ui][recipe_number][1],
            inventory,
            (INVENTORY_SIZE, 64),
        )
    return (machine_ui, chunks, location, machine_inventory, tick)
