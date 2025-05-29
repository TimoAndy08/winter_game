from ast import literal_eval
from json import dumps
from os import listdir, path, remove

import pygame as pg

from .menu_rendering import SAVES_FOLDER
from .serialize import serialize_chunks, deserialize_chunks
from .world_generation import generate_chunk
from .tile_class import Tile

def update_menu(position, location, controls, menu_placement, chunks, tick, save_file_name, run = True, noise_offset = (0, 0)):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if menu_placement == "load_save":
                if position[1] <= 50:
                    menu_placement = "main_menu"
                elif position[1] <= 100:
                    menu_placement = "save_creation"
                else:
                    saves = [f[:-len(".txt")] for f in listdir(SAVES_FOLDER)]
                    if (position[1] // 50) - 2 < len(saves):
                        save_file_name = saves[(position[1] // 50) - 2]
                        if position[0] >= 120:
                            menu_placement = "main_game"
                            with open(f"{SAVES_FOLDER}{save_file_name}.txt", "r", encoding="utf-8") as file:
                                file_content = file.read().split(";")
                            chunks = deserialize_chunks(file_content[0])
                            location["tile"] = literal_eval(file_content[1])
                            tick = int(file_content[2])
                            location["room"] = literal_eval(file_content[3])
                            location["real"] = [*location["tile"],]
                            noise_offset = literal_eval(file_content[4])
                        elif position[0] <= 90:
                            file_path = path.join(SAVES_FOLDER, save_file_name + ".txt")
                            if path.exists(file_path):
                                remove(file_path)
            elif menu_placement == "save_creation" and len(save_file_name) > 0:
                if 200 <= position[1] <= 250:
                    menu_placement = "main_game"
                    chunks = {(0, 0, 0, 0): {}}
                    location["tile"] = [0, 0, 0, 2]
                    location["real"] = [0, 0, 0, 2]
                    location["room"] = (0, 0, 0, 0)
                    noise_offset = generate_chunk(0, 0, chunks[location["room"]])
                    for x in range(-4, 5):
                        for y in range(-4, 5):
                            generate_chunk(location["tile"][0] + x, location["tile"][1] + y, chunks[location["room"]], noise_offset)
                    chunks[location["room"]][0, 0][0, 0] = Tile("obelisk")
                    chunks[location["room"]][0, 0][0, 1] = Tile("up")
                    chunks[location["room"]][0, 0][0, 2] = Tile("player", floor = "void")
                    tick = 0
            elif menu_placement.split("_")[0] == "options":
                if menu_placement == "options_game":
                    if 0 <= position[1] <= 50:
                        menu_placement = "main_game"
                    elif 100 <= position[1] <= 150:
                        menu_placement = "main_menu"
                        with open(f"{SAVES_FOLDER}{save_file_name}.txt", "w", encoding="utf-8") as file:
                            chunks_json = dumps(serialize_chunks(chunks))
                            file.write(f"{chunks_json};{location["tile"]};{tick};{location["room"]};{noise_offset}")
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
            if menu_placement == "save_creation":
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
    return location, controls, menu_placement, run, noise_offset, chunks, tick, save_file_name