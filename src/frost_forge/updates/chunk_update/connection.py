from ..right_click.inventory_move import move_inventory
from ...info import CONNECTIONS, GROW_FROM


def connect_machine(chunks, chunk, tile, kind, attributes, craftable, connection):
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
    return craftable, connection