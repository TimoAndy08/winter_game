import ast
import json

import pygame as pg

from .world_generation import generate_chunk
from .tile_class import Tile
from .serialize import serialize_chunks, deserialize_chunks
from .tile_info import RECIPES, TILE_ATTRIBUTES
from .menu_rendering import render_menu
from .tile_rendering import render_tiles
from .UI_rendering import render_UI
from .tile_updates import update_tiles
from .player_move import move_player
from .left_click_updates import left_click
from .right_click_updates import right_click

pg.init()
SCREEN_SIZE = (pg.display.Info().current_w, pg.display.Info().current_h)
FPS = 60
DAY_LENGTH = 60 * 24 * FPS
UI_SCALE = 2
INVENTORY_SIZE = 12
MENU_FONT = pg.font.SysFont("Lucida Console", 50)
UI_FONT = pg.font.SysFont("Lucida Console", 10 * UI_SCALE)
BIG_UI_FONT = pg.font.SysFont("Lucida Console", 20 * UI_SCALE)
WINDOW = pg.display.set_mode((0, 0), pg.FULLSCREEN)
CLOCK = pg.time.Clock()
CONTROL_NAMES = ["Move up ", "Move left ", "Move down ", "Move right", "Inventory ", "Zoom in", "Zoom out"]
TILE_SIZE = 64
CHUNK_SIZE = 16 * TILE_SIZE

def main() -> None:
    location = {"mined": [0, 0, 0, 2], "opened": ((0, 0), (0, 0))}
    run = True
    zoom = 1
    inventory_number = 0
    recipe_number = 0
    save_file_name = ""
    menu_placement = "main_menu"
    controls = [pg.K_w, pg.K_a, pg.K_s, pg.K_d, pg.K_e, pg.K_z, pg.K_x]
    velocity = [0, 0]
    machine_ui = "game"
    control_adjusted = 0
    machine_inventory = {}
    while run:
        WINDOW.fill((206, 229, 242))
        if menu_placement != "main_game":
            for event in pg.event.get():
                position = pg.mouse.get_pos()
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if menu_placement == "load_save":
                        if 100 <= position[1] <= 150:
                            menu_placement = "save_selection"
                        elif 200 <= position[1] <= 250:
                            menu_placement = "save_creation"
                    elif menu_placement.split("_")[0] == "save" and len(save_file_name) > 0:
                        if 200 <= position[1] <= 250:
                            if menu_placement == "save_creation":
                                menu_placement = "main_game"
                                chunks = {(0, 0, 0, 0): {}}
                                location["tile"] = [0, 0, 0, 2]
                                location["real"] = [0, 0, 0, 2]
                                location["room"] = (0, 0, 0, 0)
                                generate_chunk(0, 0, chunks[location["room"]])
                                chunks[location["room"]][(0, 0)] = {(0, 0): Tile("obelisk", 1, {}), (0, 1): Tile("up", 1, {}), (0, 2): Tile("player", 20, {})}
                                tick = 0
                            elif menu_placement == "save_selection":
                                menu_placement = "main_game"
                                with open(f"src/saves/{save_file_name}.txt", "r", encoding="utf-8") as file:
                                    file_content = file.read().split(";")
                                chunks = deserialize_chunks(file_content[0])
                                location["tile"] = ast.literal_eval(file_content[1])
                                tick = int(file_content[2])
                                location["room"] = ast.literal_eval(file_content[3])
                                location["real"] = [*location["tile"],]
                    elif menu_placement.split("_")[0] == "options":
                        if menu_placement == "options_game":
                            if 0 <= position[1] <= 50:
                                menu_placement = "main_game"
                            elif 100 <= position[1] <= 150:
                                menu_placement = "main_menu"
                                with open(f"src/saves/{save_file_name}.txt", "w", encoding="utf-8") as file:
                                    chunks_json = json.dumps(serialize_chunks(chunks))
                                    file.write(f"{chunks_json};{location["tile"]};{tick};{location["room"]}")
                                save_file_name = ""
                        elif menu_placement == "options_main":
                            if 0 <= position[1] <= 50:
                                menu_placement = "main_menu"                  
                        if 200 <= position[1] <= 250:
                            menu_placement = "controls_options"
                    elif menu_placement == "main_menu":
                        if 0 <= position[1] <= 50:
                            menu_placement = "load_save"
                        elif 100 <= position[1] <= 150:
                            menu_placement = "options_main"
                        elif 200 <= position[1] <= 250:
                            run = False
                    elif menu_placement == "controls_options":
                        if 0 <= position[1] <= 50:
                            if len(save_file_name) == 0:
                                menu_placement = "options_main"
                            else:
                                menu_placement = "options_game"
                        if event.button == 4:
                            control_adjusted = (control_adjusted - 1) % len(controls)
                        elif event.button == 5:
                            control_adjusted = (control_adjusted + 1) % len(controls)
                elif event.type == pg.KEYDOWN:
                    key = pg.key.get_pressed()
                    if menu_placement.split("_")[0] == "save":
                        for letters in range(48, 123):
                            if key[letters]:
                                save_file_name += chr(letters)
                        if key[pg.K_SPACE]:
                            save_file_name += " "
                        elif key[pg.K_BACKSPACE]:
                            save_file_name = save_file_name[:-1]
                    elif menu_placement == "controls_options":
                        for keys in range(0, len(key)):
                            if key[keys]:
                                controls[control_adjusted] = keys
            render_menu(WINDOW, MENU_FONT, menu_placement, save_file_name, CONTROL_NAMES, control_adjusted, controls)
        else:
            location["old"] = [*location["tile"],]
            inventory = chunks[location["room"]][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])].inventory
            key = pg.key.get_pressed()
            location, velocity = move_player(key, controls, velocity, location)

            if location["room"] == (0, 0, 0, 0):
                for x in range(-4, 5):
                    for y in range(-4, 5):
                        generate_chunk(location["tile"][0] + x, location["tile"][1] + y, chunks[location["room"]])
            if not (location["tile"][2], location["tile"][3]) in chunks[location["room"]][(location["tile"][0], location["tile"][1])]:
                chunks[location["room"]][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])] = chunks[location["room"]][(location["old"][0], location["old"][1])][(location["old"][2], location["old"][3])]
                del chunks[location["room"]][location["old"][0], location["old"][1]][location["old"][2], location["old"][3]]
            else:
                if chunks[location["room"]][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])].kind != "player":
                    location["real"] = [*location["old"],]
                location["tile"] = [*location["old"],]
                velocity = [0, 0]

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    position = [*pg.mouse.get_pos(),]
                    if abs(position[0] - SCREEN_SIZE[0] / 2 + 32) // (64 * zoom) <= 4 and abs(position[1] - SCREEN_SIZE[1] / 2 + 32) // (64 * zoom) <= 4 or "store" in TILE_ATTRIBUTES.get(machine_ui, ()):
                        world_x = location["tile"][0] * 16 + location["tile"][2] + (position[0] - SCREEN_SIZE[0] / 2 + 32) // (64 * zoom)
                        world_y = location["tile"][1] * 16 + location["tile"][3] + (position[1] - SCREEN_SIZE[1] / 2 + 32) // (64 * zoom)
                        grid_position = [(world_x // 16, world_y // 16), (world_x % 16, world_y % 16)]
                        if grid_position[1] in chunks[location["room"]][grid_position[0]]:
                            while "point" in chunks[location["room"]][grid_position[0]][grid_position[1]].attributes:
                                if chunks[location["room"]][grid_position[0]][grid_position[1]].kind == "left":
                                    grid_position = [(grid_position[0][0] - (grid_position[1][0] == 0), grid_position[0][1]), ((grid_position[1][0] - 1) % 16, grid_position[1][1])]
                                elif chunks[location["room"]][grid_position[0]][grid_position[1]].kind == "up":
                                    grid_position = [(grid_position[0][0], grid_position[0][1] - (grid_position[1][1] == 0)), (grid_position[1][0], (grid_position[1][1] - 1) % 16)]
                        if event.button == 1:
                            machine_ui, chunks, location, machine_inventory = left_click(machine_ui, grid_position, chunks, inventory_number, health, max_health, DAY_LENGTH, position, SCREEN_SIZE, UI_SCALE, INVENTORY_SIZE, recipe_number, location, inventory, machine_inventory)
                        elif event.button == 3:
                            chunks, location, machine_ui = right_click(chunks, grid_position, inventory, inventory_number, INVENTORY_SIZE, max_health, location, machine_ui)
                    if event.button == 4 or event.button == 5:
                        inventory_number = (inventory_number + (event.button == 5) - (event.button == 4)) % INVENTORY_SIZE
                        if "craft" in TILE_ATTRIBUTES.get(machine_ui, ()):
                            recipe_number = (recipe_number + (event.button == 5) - (event.button == 4)) % len(RECIPES[machine_ui])
                elif event.type == pg.KEYDOWN:
                    key = pg.key.get_pressed()
                    if key[controls[4]]:
                        if machine_ui == "game": 
                            machine_ui = "player"
                        else: 
                            machine_ui = "game"
                            recipe_number = 0
                    elif key[controls[5]] or key[controls[6]]:
                        zoom += (key[controls[5]] - key[controls[6]]) / 4
                        zoom = min(max(zoom, 0.5), 2)
                    elif key[pg.K_TAB]:
                        menu_placement = "options_game"

            chunks = update_tiles(chunks, location["tile"], location["room"])
            health = chunks[location["room"]][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])].health
            max_health = chunks[location["room"]][(location["tile"][0], location["tile"][1])][(location["tile"][2], location["tile"][3])].max_health

            if location["room"] != (0, 0, 0, 0):
                WINDOW.fill((19, 17, 18))
            camera = [SCREEN_SIZE[0] / 2 - ((location["tile"][2] * TILE_SIZE + location["tile"][0] * CHUNK_SIZE + 32) * zoom), SCREEN_SIZE[1] / 2 - ((location["tile"][3] * TILE_SIZE + location["tile"][1] * CHUNK_SIZE + 32) * zoom)]
            render_tiles(chunks[location["room"]], location, camera, zoom, SCREEN_SIZE, inventory, inventory_number, tick, DAY_LENGTH)
            render_UI(camera, chunks[location["room"]], zoom, location, UI_SCALE, SCREEN_SIZE, UI_FONT, BIG_UI_FONT, INVENTORY_SIZE, inventory_number, inventory, machine_ui, recipe_number, health, max_health, machine_inventory)
            tick += 1
        pg.display.update()
        CLOCK.tick(FPS)
    pg.quit()