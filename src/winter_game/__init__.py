from os import path

import pygame as pg

from .menu_rendering import render_menu
from .menu_updates import update_menu
from .tile_rendering import render_tiles, FPS, IMAGES, window
from .ui_rendering import render_ui
from .tile_updates import update_tiles
from .game_updates import update_game

pg.init()
pg.mouse.set_visible(False)

def main() -> None:
    SETTINGS_FILE = "src/settings.txt"
    if path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            controls = [int(i) for i in file.read().split(";")[0].split(":") if i]
    else:
        controls = [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_e, pg.K_z, pg.K_x]
    clock = pg.time.Clock()
    location = {"mined": ((0, 0), (0, 2)), "opened": ((0, 0), (0, 0))}
    run = True
    zoom = 1
    target_zoom = 1
    inventory_number = 0
    recipe_number = 0
    save_file_name = ""
    menu_placement = "main_menu"    
    velocity = [0, 0]
    machine_ui = "game"
    control_adjusted = 0
    machine_inventory = {}
    camera = (0, 0)
    chunks = {}
    tick = 0
    while run:
        position = pg.mouse.get_pos()
        if menu_placement != "main_game":
            location, controls, menu_placement, run, noise_offset, chunks, tick, save_file_name = update_menu(position, location, controls, menu_placement, chunks, tick, save_file_name)
            render_menu(menu_placement, save_file_name, control_adjusted, controls)
            window.blit(pg.transform.scale(IMAGES["cursor"], (32, 32)), (position[0] - 16, position[1] - 16))
        else:
            location, velocity, chunks, menu_placement, target_zoom, run, health, max_health, inventory, machine_ui, machine_inventory, tick, inventory_number, recipe_number = update_game(location, controls, velocity, noise_offset, chunks, menu_placement, zoom, target_zoom, camera, position, machine_ui, machine_inventory, tick, inventory_number, recipe_number)
            zoom = 0.05 * target_zoom + 0.95 * zoom
            chunks = update_tiles(chunks, location["tile"], location["room"])
            camera = render_tiles(chunks[location["room"]], location, zoom, target_zoom, inventory, inventory_number, tick, camera, position)
            render_ui(inventory_number, inventory, machine_ui, recipe_number, health, max_health, machine_inventory)
            tick += 1
            window.blit(pg.transform.scale(IMAGES["cursor"], (32 * zoom, 32 * zoom)), (position[0] - 16 * zoom, position[1] - 16 * zoom))
        pg.display.update()
        clock.tick(FPS)
    pg.quit()
    control_str = ""
    for i in controls:
        control_str += f"{i}:"
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        file.write(f"{control_str}")