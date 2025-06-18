from json import dumps
from os import path

from ...render.menu_rendering import SAVES_FOLDER
from ...tile_systems.serialize import serialize_chunks
from .load_save import save_loading
from .create_save import save_creating
from .options import option

def update_mouse(state, event, chunks):
    if state.menu_placement == "load_save":
        if state.position[1] <= 50:
            state.menu_placement = "main_menu"
        elif state.position[1] <= 100:
            chunks = save_creating(state, chunks)
        else:
            chunks = save_loading(state, chunks)
    elif state.menu_placement.startswith("options"):
        option(state, chunks)

    elif state.menu_placement == "save_creation" and state.save_file_name != "" and state.save_file_name.split("_")[0] != "autosave":
        state.menu_placement = "main_menu"
        with open(path.join(SAVES_FOLDER, state.save_file_name + ".txt"), "w", encoding="utf-8") as file:
            chunks_json = dumps(serialize_chunks(chunks))
            file.write(f"{chunks_json};{state.location['tile']};{state.tick};{state.noise_offset}")
        state.save_file_name = ""

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
    return chunks