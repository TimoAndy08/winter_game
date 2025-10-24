from math import cos, pi

import pygame as pg

from ...info import TILE_SIZE, HALF_SIZE, CHUNK_SIZE, SCREEN_SIZE, DAY_LENGTH, FLOOR_SIZE


def render_lights(tick, lighting, location, zoom, camera, window):
    dark_overlay = pg.Surface(SCREEN_SIZE)
    dark_overlay.fill((19, 17, 18))
    dark_overlay.set_alpha(int((1 - cos(((tick / DAY_LENGTH * 2) - 1 / 2) * pi)) * 95))
    window.blit(dark_overlay, (0, 0))

    for x in range(-2, 3):
        for y in range(-2, 3):
            chunk = (x + location["tile"][0], y + location["tile"][1])
            if chunk in lighting:
                for tile in lighting[chunk]:
                    current_tile = lighting[chunk][tile]
                    placement_x = (camera[0] + (tile[0] * TILE_SIZE + chunk[0] * CHUNK_SIZE + HALF_SIZE) * zoom)
                    placement_y = (camera[1] + (tile[1] * TILE_SIZE + chunk[1] * CHUNK_SIZE + HALF_SIZE) * zoom)
                    night_factor = 1 - cos(((tick / DAY_LENGTH * 2) - 1 / 2) * pi)
                    glow = pg.Surface((FLOOR_SIZE[0] * zoom, FLOOR_SIZE[1] * zoom), pg.SRCALPHA)
                    glow = pg.draw.rect(glow, (228, 148, 106, int(6 * night_factor * current_tile)), glow.get_rect())
                    window.blit(glow, (placement_x, placement_y))
    return window