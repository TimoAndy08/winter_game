import pygame as pg

from .render.tile_rendering import FPS
from .updates.update import update
from .settings_saving import settings_save
from .render.rendering import render
from .game_state import Game_State

pg.init()
pg.mouse.set_visible(False)

def main() -> None:
    state = Game_State()
    chunks = {(0, 0, 0, 0): {}}
    while state.run:
        state.position = pg.mouse.get_pos()
        chunks = update(state, chunks)
        state.camera = render(state, chunks)
        state.clock.tick(FPS)
    pg.quit()
    settings_save(state.controls)