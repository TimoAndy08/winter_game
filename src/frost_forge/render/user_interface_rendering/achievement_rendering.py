import pygame as pg

from ...info import ACHIEVEMENTS, SLOT_SIZE, HALF_SCREEN_SIZE, UI_SCALE, FLOOR, TILE_UI_SIZE, FLOOR_SIZE


def render_achievement(achievement, window, images):
    window.blit(
            pg.transform.scale(images["inventory_slot_2"], SLOT_SIZE),
            (HALF_SCREEN_SIZE - 32 * UI_SCALE, 0),
        )
    if achievement not in FLOOR:
        window.blit(
            pg.transform.scale(images[achievement], TILE_UI_SIZE),
            (HALF_SCREEN_SIZE - 24 * UI_SCALE, 4 * UI_SCALE),
        )
    else:
        window.blit(
            pg.transform.scale(images[achievement], FLOOR_SIZE),
            (HALF_SCREEN_SIZE - 24 * UI_SCALE, 8 * UI_SCALE),
        )
    return window
