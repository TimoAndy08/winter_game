from .tile_info import TOOL_REQUIRED, TOOL_EFFICIENCY, RESISTANCE
from .tile_class import Tile
from .ui_rendering import INVENTORY_SIZE

def calculate_damage(mining_type, inventory, inventory_number):
    damage = 1 - RESISTANCE.get(mining_type, 0)
    if len(inventory) > inventory_number:
        inventory_words = list(inventory.keys())[inventory_number].split()
        if len(inventory_words) == 2 and mining_type in TOOL_REQUIRED:
            if TOOL_REQUIRED[mining_type] == inventory_words[1]:
                damage += TOOL_EFFICIENCY[inventory_words[0]]
    return max(damage, 0)

def right_click(
    chunks,
    grid_position: tuple[tuple[int, int], tuple[int, int]],
    inventory: dict[str, int],
    inventory_number: int,
    location: dict,
    machine_ui: str,
):
    machine_ui = "game"
    if grid_position[1] not in chunks[location["room"]][grid_position[0]]:
        return (chunks, location, machine_ui)
    mining_tile = chunks[location["room"]][grid_position[0]][grid_position[1]]
    mining_kind = mining_tile.kind
    delete_mining_tile = False
    player_tile = chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]]
    location["mined"] = (grid_position[0], grid_position[1])
    if mining_tile.unbreak == False and isinstance(mining_kind, str):
        mining_tile.health -= calculate_damage(mining_kind, inventory, inventory_number)
        if mining_tile.health <= 0:
            if mining_kind != "player":
                junk_inventory = {}
                if "no_pickup" not in mining_tile.attributes:
                    inventory[mining_kind] = inventory.get(mining_kind, 0) + 1
                for item, amount in mining_tile.inventory.items():
                    if item in player_tile.inventory:
                        player_tile.inventory[item] += amount
                        if inventory[item] > 64:
                            junk_inventory[item] = player_tile.inventory[item] - 64
                            player_tile.inventory[item] = 64
                    else:
                        if len(inventory) < INVENTORY_SIZE:
                            player_tile.inventory[item] = amount
                        else:
                            junk_inventory[item] = amount
                if "enter" in mining_tile.attributes and (*grid_position[0], *grid_position[1]) in chunks:
                    del chunks[(*grid_position[0], *grid_position[1])]
                if isinstance(mining_tile.floor, str):
                    mining_tile = Tile(floor = mining_tile.floor, floor_unbreak = mining_tile.floor_unbreak)
                else:
                    delete_mining_tile = True
                if len(junk_inventory) > 0:
                    mining_tile = Tile("junk", junk_inventory, mining_tile.floor, floor_unbreak = mining_tile.floor_unbreak)
            else:
                chunks[location["room"]][grid_position[0]][grid_position[1]] = Tile("corpse", inventory, mining_tile.floor, floor_unbreak = mining_tile.floor_unbreak)
                chunks[(0, 0, 0, 0)][(0, 0)][(0, 2)] = Tile("player", floor = "void")
                location["tile"] = [0, 0, 0, 2]
                location["real"] = [0, 0, 0, 2]
                location["room"] = (0, 0, 0, 0)
                return (chunks, location, machine_ui)
    elif mining_tile.floor_unbreak == False and isinstance(mining_tile.floor, str):
        mining_tile.floor_health -= calculate_damage(mining_tile.floor, inventory, inventory_number)
        broke = False
        if mining_tile.floor_health <= 0:
            if mining_tile.floor in inventory:
                if inventory[mining_tile.floor] < 64:
                    broke = True
            elif len(inventory) < INVENTORY_SIZE:
                broke = True
        if broke:
            player_tile.inventory[mining_tile.floor] = player_tile.inventory.get(mining_tile.floor, 0) + 1
            delete_mining_tile = True
    chunks[location["room"]][location["tile"][0], location["tile"][1]][location["tile"][2], location["tile"][3]] = player_tile
    if delete_mining_tile:
        del chunks[location["room"]][grid_position[0]][grid_position[1]]
    else:
        chunks[location["room"]][grid_position[0]][grid_position[1]] = mining_tile
    return (chunks, location, machine_ui)