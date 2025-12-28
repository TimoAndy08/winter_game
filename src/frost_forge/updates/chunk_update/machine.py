from math import sqrt, log2

from ..left_click import recipe
from ..right_click.inventory_move import move_inventory
from ...info import RUNES_USER, RUNES, RECIPES, PROCESSING_TIME, CONNECTIONS, GROW_FROM, FPS


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
            mana = 0
            for x in range(-RUNES_USER[kind], RUNES_USER[kind] + 1):
                for y in range(-RUNES_USER[kind], RUNES_USER[kind] + 1):
                    if sqrt(x ** 2 + y ** 2) <= RUNES_USER[kind]:
                        rune_tile = ((tile[0] + x) % 16, (tile[1] + y) % 16)
                        rune_chunk = (chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16)
                        if rune_tile in chunks[rune_chunk] and "floor" in chunks[rune_chunk][rune_tile]:
                            rune = chunks[rune_chunk][rune_tile]["floor"]
                            if rune in RUNES:
                                if RUNES[rune][0] == 0:
                                    mana += RUNES[rune][1]
                                elif RUNES[rune][0] == 1:
                                    mana *= RUNES[rune][1]
                                    mana += RUNES[rune][2]
            if int(log2(max(mana, 0) ** 1.2 + 2)) != RECIPES[kind][current_tile["recipe"]][2]:
                craftable = False
            machine_inventory["mana_level"] = int(log2(mana ** 1.2 + 2))
        if kind in CONNECTIONS:
            x = 1
            y = 1
            connector_tile = ((tile[0] + x) % 16, tile[1])
            connector_chunk = (chunk[0] + (tile[0] + x) // 16, chunk[1])
            while chunks[connector_chunk].get(connector_tile, {}).get("kind", None) == CONNECTIONS[kind]:
                x += 1
                connector_tile = ((tile[0] + x) % 16, tile[1])
                connector_chunk = (chunk[0] + (tile[0] + x) // 16, chunk[1])
            connector_tile = (tile[0], (tile[1] + y) % 16)
            connector_chunk = (chunk[0], chunk[1] + (tile[1] + y) // 16)
            while chunks[connector_chunk].get(connector_tile, {}).get("kind", None) == CONNECTIONS[kind]:
                y += 1
                connector_tile = (tile[0], (tile[1] + y) % 16)
                connector_chunk = (chunk[0], chunk[1] + (tile[1] + y) // 16)
            for i in range(0, x + 1):
                for j in range(0, y + 1):
                    connected_tile = ((tile[0] + i) % 16, (tile[1] + j) % 16)
                    connected_chunk = (chunk[0] + (tile[0] + i) // 16, chunk[1] + (tile[1] + j) // 16)
                    if i % x == 0 and j % y == 0:
                        if chunks[connected_chunk].get(connected_tile, {}).get("kind", None) != kind:
                            connection = False
                    elif i % x == 0 or j % y == 0:
                        if chunks[connected_chunk].get(connected_tile, {}).get("kind", None) != CONNECTIONS[kind]:
                            connection = False
            if connection:
                if "harvester" in attributes:
                    print("I'm tryna harvest")
                    craftable = False
                    for i in range(0, x):
                        for j in range(0, y):
                            harvest_tile = ((tile[0] + i) % 16, (tile[1] + j) % 16)
                            harvest_chunk = (chunk[0] + (tile[0] + i) // 16, chunk[1] + (tile[1] + j) // 16)
                            if chunks[harvest_chunk].get(harvest_tile, {}).get("kind", None) in GROW_FROM:
                                harvestable = chunks[harvest_chunk][harvest_tile]
                                chunks[chunk][tile]["inventory"] = move_inventory(harvestable, chunks[chunk][tile].get("inventory", {}), (20, 64))[0]
                                if GROW_FROM[harvestable["kind"]] in chunks[chunk][tile]["inventory"]:
                                    chunks[chunk][tile]["inventory"][GROW_FROM[harvestable["kind"]]] -= 1
                                    chunks[harvest_chunk][harvest_tile]["kind"] = GROW_FROM[harvestable["kind"]]
                                else:
                                    chunks[harvest_chunk][harvest_tile] = {"floor": chunks[harvest_chunk][harvest_tile]["floor"]}
        if craftable and connection:
            machine_inventory = recipe(kind, current_tile["recipe"], machine_inventory, (20, 64))
    return machine_inventory