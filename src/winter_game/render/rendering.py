import pygame as pg

from .menu_rendering import render_menu
from .tile_rendering import render_tiles, window, IMAGES
from .ui_rendering import render_ui
from ..game_state import Game_State

def render(state: Game_State, chunks) -> tuple:
    if state.menu_placement != "main_game":
        render_menu(state.menu_placement, state.save_file_name, state.control_adjusted, state.controls)
        window.blit(pg.transform.scale(IMAGES["cursor"], (32, 32)), (state.position[0] - 16, state.position[1] - 16))
    else:
        state.camera = render_tiles(
            chunks[state.location["room"]],
            state.location,
            state.zoom,
            state.target_zoom,
            state.inventory,
            state.inventory_number,
            state.tick,
            state.camera,
            state.position
        )
        render_ui(
            state.inventory_number,
            state.inventory,
            state.machine_ui,
            state.recipe_number,
            state.health,
            state.max_health,
            state.machine_inventory
        )
        cursor_size = (int(32 * state.zoom), int(32 * state.zoom))
        cursor_place = (state.position[0] - 16 * state.zoom, state.position[1] - 16 * state.zoom)
        window.blit(pg.transform.scale(IMAGES["cursor"], cursor_size), cursor_place)
    pg.display.update()
    return state.camera