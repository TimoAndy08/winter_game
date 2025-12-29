from ..left_click import recipe
from .connection import connect_machine
from .mana import mana_level
from .transport import transport_item
from ...info import RUNES_USER, PROCESSING_TIME, CONNECTIONS, FPS, ADJACENT_ROOMS, ATTRIBUTES, ITEM_TICK, RECIPES, LOOT_TABLES


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
            if location in current_tile and current_tile[location] == 1:
                if adjacent_tile in chunks[adjacent_chunk] and "kind" in chunks[adjacent_chunk][adjacent_tile]:
                    adjacent = chunks[adjacent_chunk][adjacent_tile]
                    if "transport" in ATTRIBUTES.get(adjacent["kind"], ()):
                        if (-location[0], -location[1]) in adjacent and adjacent[-location[0], -location[1]] == 0:
                            if "inventory" not in adjacent:
                                adjacent["inventory"] = {}
                            item_tick = ITEM_TICK[adjacent["kind"]]
                            if kind in RECIPES:
                                output_kind = RECIPES[kind][current_tile["recipe"]][0][0]
                                if output_kind not in LOOT_TABLES:
                                    machine_inventory, adjacent["inventory"] = transport_item(output_kind, machine_inventory, adjacent["inventory"], item_tick)
                                else:
                                    for item in LOOT_TABLES[output_kind][0]:
                                        if item[1] in machine_inventory:
                                            machine_inventory, adjacent["inventory"] = transport_item(item[1], machine_inventory, adjacent["inventory"], item_tick)
                            else:
                                output_kind = list(machine_inventory)[0]
                                machine_inventory, adjacent["inventory"] = transport_item(output_kind, machine_inventory, adjacent["inventory"], item_tick)
                            chunks[adjacent_chunk][adjacent_tile] = adjacent
    return machine_inventory