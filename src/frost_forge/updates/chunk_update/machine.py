from ..left_click import recipe
from .connection import connect_machine
from .mana import mana_level
from ...info import RUNES_USER, PROCESSING_TIME, CONNECTIONS, FPS, ADJACENT_ROOMS, ATTRIBUTES


def machine(tick, current_tile, kind, attributes, tile, chunk, chunks):
    if "inventory" not in current_tile:
        machine_inventory = {}
    else:
        machine_inventory = current_tile["inventory"]
    if "harvester" in attributes:
        chunks[chunk][tile]["recipe"] = 0
    if tick % PROCESSING_TIME.get(kind, FPS) == 0 and current_tile.get("recipe", -1) >= 0:
        if "drill" in attributes and "floor" in current_tile:
            if current_tile["floor"].split(" ")[-1] == "mineable":
                machine_inventory[current_tile["floor"]] = 1
        craftable = True
        connection = True
        if kind in RUNES_USER:
            machine_inventory, craftable = mana_level(chunks, chunk, tile, kind, current_tile, machine_inventory, craftable)
        if kind in CONNECTIONS:
            craftable, connection = connect_machine(chunks, chunk, tile, kind, attributes, craftable, connection)
        if craftable and connection:
            machine_inventory = recipe(kind, current_tile["recipe"], machine_inventory, (20, 64))
        for location in ADJACENT_ROOMS:
            adjacent_tile = ((tile[0] + location[0]) % 16, (tile[1] + location[1]) % 16)
            adjacent_chunk = (chunk[0] + (tile[0] + location[0]) // 16, chunk[1] + (tile[1] + location[1]) // 16)
            if location in current_tile:
                if adjacent_tile in chunks[adjacent_chunk] and "kind" in chunks[adjacent_chunk][adjacent_tile]:
                    if "store" in ATTRIBUTES.get(chunks[adjacent_chunk][adjacent_tile]["kind"], ()):
                        if current_tile[location] == 0:
                            0 # Input from adjacent
                        else:
                            1 # Output to adjacent
    return machine_inventory