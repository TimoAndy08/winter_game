from ..left_click import recipe
from .connection import connect_machine
from .mana import mana_level
from .transport import output_transport
from ...info import RUNES_USER, PROCESSING_TIME, CONNECTIONS, FPS


def machine(tick, current_tile, kind, attributes, tile, chunk, chunks):
    if "inventory" not in current_tile:
        machine_inventory = {}
    else:
        machine_inventory = current_tile["inventory"]
    if "harvester" in attributes:
        chunks[chunk][tile]["recipe"] = 0
    if tick % PROCESSING_TIME.get(kind, FPS) == 0 and current_tile.get("recipe", -1) >= 0:
        efficiency = 1
        connection = True
        if "drill" in attributes and "floor" in current_tile:
            if current_tile["floor"].split(" ")[-1] == "mineable":
                machine_inventory[current_tile["floor"]] = 1
        if kind in RUNES_USER:
            machine_inventory, efficiency = mana_level(chunks, chunk, tile, kind, current_tile, machine_inventory, efficiency)
        if kind in CONNECTIONS:
            connection, efficiency = connect_machine(chunks, chunk, tile, kind, attributes, connection, efficiency)
        if connection:
            for _ in range(0, efficiency):
                machine_inventory = recipe(kind, current_tile["recipe"], machine_inventory, (20, 64))
        machine_inventory, chunks = output_transport(chunks, chunk, tile, current_tile, kind, {"transport"})
    return machine_inventory