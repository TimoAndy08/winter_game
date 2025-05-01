from .tile_info import TOOL_REQUIRED, TOOL_EFFICIENCY, TILE_RESISTANCE, FLOOR_RESISTANCE
from .tile_class import Tile
from .ui_rendering import INVENTORY_SIZE

def right_click(
    chunks,
    grid_position: tuple[tuple[int, int], tuple[int, int]],
    inventory: dict[str, int],
    inventory_number: int,
    location: dict,
    machine_ui: str,
):
    if grid_position[1] not in chunks[location["room"]][grid_position[0]]:
        return (chunks, location, machine_ui)
    mining_tile = chunks[location["room"]][grid_position[0]][grid_position[1]]
    location["mined"] = (grid_position[0], grid_position[1])
    if "unbreak" not in mining_tile.attributes and isinstance(mining_tile.kind, str):
        damage = 1 - TILE_RESISTANCE.get(mining_tile.kind, 0)
        if len(inventory) > inventory_number:
            inventory_words = list(inventory.keys())[inventory_number].split()
            if len(inventory_words) == 2 and mining_tile.kind in TOOL_REQUIRED:
                if TOOL_REQUIRED[mining_tile.kind] == inventory_words[1]:
                    damage += TOOL_EFFICIENCY[inventory_words[0]]
        chunks[location["room"]][grid_position[0]][grid_position[1]].health -= max(damage, 0)
        if chunks[location["room"]][grid_position[0]][grid_position[1]].health <= 0:
            if mining_tile.kind != "player":
                junk_inventory = {}
                if "no_pickup" not in mining_tile.attributes:
                    chunks[location["room"]][grid_position[0]][grid_position[1]].inventory[mining_tile.kind] = mining_tile.inventory.get(mining_tile.kind, 0) + 1
                for item, amount in chunks[location["room"]][grid_position[0]][
                    grid_position[1]].inventory.items():
                    if item in chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].inventory:
                        chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].inventory[item] += amount
                        if inventory[item] > 64:
                            junk_inventory[item] = chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].inventory[item] - 64
                            chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].inventory[item] = 64
                    else:
                        if len(inventory) < INVENTORY_SIZE:
                            chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].inventory[item] = amount
                        else:
                            junk_inventory[item] = amount
                if "enter" in chunks[location["room"]][grid_position[0]][grid_position[1]].attributes and (*grid_position[0], *grid_position[1]) in chunks:
                    del chunks[(*grid_position[0], *grid_position[1])]
                if isinstance(mining_tile.floor, str):
                    chunks[location["room"]][grid_position[0]][grid_position[1]] = Tile(floor = mining_tile.floor, floor_break = mining_tile.floor_break)
                else:
                    del chunks[location["room"]][grid_position[0]][grid_position[1]]
                if len(junk_inventory) > 0:
                    chunks[location["room"]][grid_position[0]][grid_position[1]] = Tile("junk", junk_inventory, mining_tile.floor, floor_break = mining_tile.floor_break)
                machine_ui = "game"
            else:
                chunks[location["room"]][grid_position[0]][grid_position[1]] = Tile("corpse", inventory, mining_tile.floor, floor_break = mining_tile.floor_break)
                chunks[(0, 0, 0, 0)][(0, 0)][(0, 2)] = Tile("player", floor = "void")
                location["tile"] = [0, 0, 0, 2]
                location["real"] = [0, 0, 0, 2]
                location["room"] = (0, 0, 0, 0)
    elif mining_tile.floor_break and isinstance(mining_tile.floor, str):
        damage = 1 - FLOOR_RESISTANCE.get(mining_tile.floor, 0)
        if len(inventory) > inventory_number:
            inventory_words = list(inventory.keys())[inventory_number].split()
            if len(inventory_words) == 2 and mining_tile.floor in TOOL_REQUIRED:
                if TOOL_REQUIRED[mining_tile.floor] == inventory_words[1]:
                    damage += TOOL_EFFICIENCY[inventory_words[0]]
        chunks[location["room"]][grid_position[0]][grid_position[1]].floor_health -= max(damage, 0)
        broke = False
        if chunks[location["room"]][grid_position[0]][grid_position[1]].floor_health <= 0:
            if mining_tile.floor in inventory:
                if inventory[mining_tile.floor] < 64:
                    broke = True
            elif len(inventory) < INVENTORY_SIZE:
                broke = True
        if broke:
            chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].inventory[mining_tile.floor] = chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]].inventory.get(mining_tile.floor, 0) + 1
            del chunks[location["room"]][grid_position[0]][grid_position[1]]
    return (chunks, location, machine_ui)