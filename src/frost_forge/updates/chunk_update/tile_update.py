from .point import left, up
from ..entity_behaviour.animal import animal
from ..entity_behaviour.enemy import enemy
from .growth import grow
from ..left_click import recipe
from ...info import ATTRIBUTES, GROW_TILES, FPS, PROCESSING_TIME


def update_tile(
    current_tile,
    chunks,
    chunk,
    tile,
    delete_tiles,
    create_tiles,
    tick,
    location,
    inventory_key,
    health,
):
    if current_tile["kind"] == "left":
        chunks, delete_tiles = left(chunks, chunk, tile, delete_tiles)
    elif current_tile["kind"] == "up":
        chunks, delete_tiles = up(chunks, chunk, tile, delete_tiles)
    elif tick % (FPS // 6) == 0:
        if "machine" in ATTRIBUTES.get(current_tile["kind"], ()) and tick % PROCESSING_TIME[current_tile["kind"]] == 0:
            chunks[chunk][tile]["inventory"] = recipe(current_tile["kind"], current_tile.get("recipe", 0), current_tile.get("inventory", {}))
        elif current_tile["kind"] in GROW_TILES:
            chunks[chunk][tile] = grow(current_tile)
            if chunks[chunk][tile] == {}:
                delete_tiles.append((chunk, tile))
        elif "animal" in ATTRIBUTES.get(current_tile["kind"], ()):
            create_tiles, delete_tiles = animal(
                chunks,
                chunk,
                tile,
                current_tile,
                create_tiles,
                delete_tiles,
                location,
                inventory_key,
            )
        elif "enemy" in ATTRIBUTES.get(current_tile["kind"], ()):
            create_tiles, delete_tiles, health = enemy(
                chunks,
                chunk,
                tile,
                current_tile,
                create_tiles,
                delete_tiles,
                location,
                health,
            )
    return chunks, create_tiles, delete_tiles, health
