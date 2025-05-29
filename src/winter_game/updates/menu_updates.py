from ast import literal_eval
from json import dumps
from os import listdir, path, remove

import pygame as pg

from ..render.menu_rendering import SAVES_FOLDER
from ..tile_systems.serialize import serialize_chunks, deserialize_chunks
from ..tile_systems.world_generation import generate_chunk
from ..tile_systems.tile_class import Tile

def update_menu(state, chunks):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            state.run = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if state.menu_placement == "load_save":
                if state.position[1] <= 50:
                    state.menu_placement = "main_menu"
                elif state.position[1] <= 100:
                    state.menu_placement = "save_creation"
                else:
                    saves = [f[:-4] for f in listdir(SAVES_FOLDER) if f.endswith(".txt")]
                    index = (state.position[1] // 50) - 2
                    if index < len(saves):
                        state.save_file_name = saves[index]
                        if state.position[0] >= 120:
                            state.menu_placement = "main_game"
                            with open(path.join(SAVES_FOLDER, state.save_file_name + ".txt"), "r", encoding="utf-8") as file:
                                file_content = file.read().split(";")
                            chunks = deserialize_chunks(file_content[0])
                            state.location["tile"] = literal_eval(file_content[1])
                            state.tick = int(file_content[2])
                            state.location["room"] = literal_eval(file_content[3])
                            state.location["real"] = list(state.location["tile"])
                            state.noise_offset = literal_eval(file_content[4])
                        elif state.position[0] <= 90:
                            file_path = path.join(SAVES_FOLDER, state.save_file_name + ".txt")
                            if path.exists(file_path):
                                remove(file_path)

            elif state.menu_placement == "save_creation" and len(state.save_file_name) > 0:
                if 200 <= state.position[1] <= 250:
                    state.menu_placement = "main_game"
                    chunks = {(0, 0, 0, 0): {}}
                    state.location["tile"] = [0, 0, 0, 2]
                    state.location["real"] = [0, 0, 0, 2]
                    state.location["room"] = (0, 0, 0, 0)
                    state.noise_offset = generate_chunk(0, 0, chunks[state.location["room"]])
                    for x in range(-4, 5):
                        for y in range(-4, 5):
                            generate_chunk(state.location["tile"][0] + x, state.location["tile"][1] + y, chunks[state.location["room"]], state.noise_offset)
                    chunks[state.location["room"]][(0, 0)][(0, 0)] = Tile("obelisk")
                    chunks[state.location["room"]][(0, 0)][(0, 1)] = Tile("up")
                    chunks[state.location["room"]][(0, 0)][(0, 2)] = Tile("player", floor="void")
                    state.tick = 0

            elif state.menu_placement.startswith("options"):
                if state.menu_placement == "options_game":
                    if 0 <= state.position[1] <= 50:
                        state.menu_placement = "main_game"
                    elif 100 <= state.position[1] <= 150:
                        state.menu_placement = "main_menu"
                        with open(path.join(SAVES_FOLDER, state.save_file_name + ".txt"), "w", encoding="utf-8") as file:
                            chunks_json = dumps(serialize_chunks(chunks))
                            file.write(f"{chunks_json};{state.location['tile']};{state.tick};{state.location['room']};{state.noise_offset}")
                        state.save_file_name = ""
                elif state.menu_placement == "options_main":
                    if 0 <= state.position[1] <= 50:
                        state.menu_placement = "main_menu"
                if 200 <= state.position[1] <= 250:
                    state.menu_placement = "controls_options"

            elif state.menu_placement == "main_menu":
                if 0 <= state.position[1] <= 50:
                    state.menu_placement = "load_save"
                elif 100 <= state.position[1] <= 150:
                    state.menu_placement = "options_main"
                elif 200 <= state.position[1] <= 250:
                    state.run = False

            elif state.menu_placement == "controls_options":
                if 0 <= state.position[1] <= 50:
                    state.menu_placement = "options_game" if len(state.save_file_name) else "options_main"
                if event.button == 4:
                    state.control_adjusted = (state.control_adjusted - 1) % len(state.controls)
                elif event.button == 5:
                    state.control_adjusted = (state.control_adjusted + 1) % len(state.controls)

        elif event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if state.menu_placement == "save_creation":
                for letter in range(48, 123):
                    if keys[letter]:
                        state.save_file_name += chr(letter)
                if keys[pg.K_SPACE]:
                    state.save_file_name += " "
                elif keys[pg.K_BACKSPACE]:
                    state.save_file_name = state.save_file_name[:-1]

            elif state.menu_placement == "controls_options":
                for key_code in range(len(keys)):
                    if keys[key_code]:
                        state.controls[state.control_adjusted] = key_code
    return chunks