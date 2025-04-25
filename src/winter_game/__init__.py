from ast import literal_eval
import json

import pygame as pg

from .world_generation import generate_chunk
from .tile_class import Tile
from .serialize import serialize_chunks, deserialize_chunks
from .menu_rendering import render_menu
from .tile_rendering import render_tiles, FPS
from .ui_rendering import render_ui
from .tile_updates import update_tiles
from .player_move import move_player
from .mouse_update import button_press

pg.init()

def main() -> None:
    clock = pg.time.Clock()
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
                                chunks[location["room"]][(0, 0)] = {(0, 0): Tile("obelisk", {}), (0, 1): Tile("up", {}), (0, 2): Tile("player", {})}
                                tick = 0
                            elif menu_placement == "save_selection":
                                menu_placement = "main_game"
                                with open(f"src/saves/{save_file_name}.txt", "r", encoding="utf-8") as file:
                                    file_content = file.read().split(";")
                                chunks = deserialize_chunks(file_content[0])
                                location["tile"] = literal_eval(file_content[1])
                                tick = int(file_content[2])
                                location["room"] = literal_eval(file_content[3])
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
            render_menu(menu_placement, save_file_name, control_adjusted, controls)
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
                    chunks, location, machine_ui, machine_inventory, tick, recipe_number, inventory_number = button_press(event.button, position, zoom, chunks, location, machine_ui, inventory, health, max_health, machine_inventory, tick, inventory_number, recipe_number)
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
            render_tiles(chunks[location["room"]], location, zoom, inventory, inventory_number, tick)
            render_ui(inventory_number, inventory, machine_ui, recipe_number, health, max_health, machine_inventory)
            tick += 1
        pg.display.update()
        clock.tick(FPS)
    pg.quit()