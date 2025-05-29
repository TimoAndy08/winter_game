import pygame as pg

from .player_move import move_player
from .tile_class import Tile
from .world_generation import generate_chunk
from .mouse_update import button_press

def update_game(location, controls, velocity, noise_offset, chunks, menu_placement, zoom, target_zoom, camera, position, machine_ui, machine_inventory, tick, inventory_number, recipe_number, run = True):
    health = chunks[location["room"]][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])].health
    max_health = chunks[location["room"]][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])].max_health

    location["old"] = [*location["tile"],]
    inventory = chunks[location["room"]][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])].inventory
    key = pg.key.get_pressed()
    location, velocity = move_player(key, controls, velocity, location)

    if location["room"] == (0, 0, 0, 0):
        for x in range(-4, 5):
            for y in range(-4, 5):
                generate_chunk(location["tile"][0] + x, location["tile"][1] + y, chunks[location["room"]], noise_offset)
                
    room = location["room"]
    tile_chunk_coords = (location["tile"][0], location["tile"][1])
    tile_coords = (location["tile"][2], location["tile"][3])
    old_chunk_coords = (location["old"][0], location["old"][1])
    old_tile_coords = (location["old"][2], location["old"][3])

    chunk = chunks[room][tile_chunk_coords]
    old_chunk = chunks[room][old_chunk_coords]
    old_tile = old_chunk[old_tile_coords]

    if tile_coords not in chunk:
        chunk[tile_coords] = Tile("player", inventory, health = health, max_health = max_health)
    elif chunk[tile_coords].kind == None:
        exist_tile = chunk[tile_coords]
        chunk[tile_coords] = Tile("player", inventory, exist_tile.floor, health, max_health, exist_tile.floor_health, exist_tile.floor_unbreak)
    elif chunk[tile_coords].kind != "player":
        location["real"] = [*location["old"],]
        location["tile"] = [*location["old"]]
        velocity = [0, 0]

    if location["old"] != location["tile"]:
        if isinstance(old_tile.floor, str):
            old_chunk[old_tile_coords] = Tile(floor = old_tile.floor, floor_health = old_tile.floor_health, floor_unbreak = old_tile.floor_unbreak)
        else:
            del old_chunk[old_tile_coords]

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            chunks, location, machine_ui, machine_inventory, tick, recipe_number, inventory_number = button_press(event.button, position, zoom, chunks, location, machine_ui, inventory, health, max_health, machine_inventory, tick, inventory_number, recipe_number, camera)
        elif event.type == pg.KEYDOWN:
            key = pg.key.get_pressed()
            if key[controls[4]]:
                if machine_ui == "game": 
                    machine_ui = "player"
                else:
                    machine_ui = "game"
                    recipe_number = 0
            elif key[controls[5]] or key[controls[6]]:
                target_zoom += (key[controls[5]] - key[controls[6]]) / 4
                target_zoom = min(max(target_zoom, 0.5), 2)
            elif key[pg.K_TAB]:
                menu_placement = "options_game"
    return location, velocity, chunks, menu_placement, target_zoom, run, health, max_health, inventory, machine_ui, machine_inventory, tick, inventory_number, recipe_number