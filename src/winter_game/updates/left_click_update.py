from ..info import TILE_ATTRIBUTES, DAY_LENGTH
from .left_click import recipe, place, storage, machine_storage

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
        is_not_tile = (grid_position[1] not in chunks[grid_position[0]])
        if not is_not_tile:
            is_kind = isinstance(chunks[grid_position[0]][grid_position[1]].kind, str)
        else:
            is_kind = True
        if is_not_tile or not is_kind:
            chunks = place(inventory, inventory_number, is_not_tile, is_kind, health, max_health, grid_position, location, chunks)
        elif "open" in chunks[grid_position[0]][grid_position[1]].attributes:
            machine_ui = chunks[grid_position[0]][grid_position[1]].kind
            location["opened"] = (grid_position[0], grid_position[1])
            machine_inventory = chunks[grid_position[0]][grid_position[1]].inventory
        elif "sleep" in chunks[grid_position[0]][grid_position[1]].attributes:
            if 9 / 16 <= (tick / DAY_LENGTH) % 1 < 15 / 16:
                tick = (tick // DAY_LENGTH + 9 / 16) * DAY_LENGTH
    elif "machine" in TILE_ATTRIBUTES.get(machine_ui, ()):
        chunks = machine_storage(position, chunks, location, inventory, machine_ui)
    elif "store" in TILE_ATTRIBUTES.get(machine_ui, ()):
        chunks = storage(position, chunks, location, inventory, machine_ui)
    elif "craft" in TILE_ATTRIBUTES.get(machine_ui, ()):
        inventory = recipe(machine_ui, recipe_number, inventory)
    return machine_ui, chunks, location, machine_inventory, tick
