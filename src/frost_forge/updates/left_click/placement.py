from ...info import FOOD, FLOOR, HEALTH
from ...other_systems.tile_placement import place_tile
from ...other_systems.tile_placable import is_placable


def place(inventory, inventory_number, is_not_tile, is_kind, health, max_health, grid_position, chunks):
    if len(inventory) > inventory_number:
        inventory_key = list(inventory.keys())[inventory_number]
        if inventory_key not in FLOOR:
            if is_not_tile or not is_kind:
                if inventory_key in FOOD and health < max_health:
                    health = min(health + FOOD[inventory_key], max_health)
                elif is_placable(inventory_key, grid_position, chunks):
                    chunks = place_tile(inventory_key, grid_position, chunks)
                    inventory[inventory_key] -= 1
        elif is_not_tile:
            inventory[inventory_key] -= 1
            chunks[grid_position[0]][grid_position[1]] = {"floor": inventory_key}
        if inventory[inventory_key] == 0:
            del inventory[inventory_key]
    return chunks