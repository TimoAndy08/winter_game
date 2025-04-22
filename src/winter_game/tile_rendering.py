import math
import os

import pygame as pg

from .tile_info import MULTI_TILES
from .light import lights

pg.init()
WINDOW = pg.display.set_mode((0, 0), pg.FULLSCREEN)
IMAGES = {}
SPRITES_FOLDER = "src/sprites"
for filename in os.listdir(SPRITES_FOLDER):
    IMAGES[filename.split(".")[0]] = pg.image.load(
        os.path.join(SPRITES_FOLDER, filename)
    ).convert_alpha()


def render_tiles(
    chunks,
    location,
    camera,
    zoom,
    SCREEN_SIZE,
    inventory,
    inventory_number,
    tick,
    DAY_LENGTH,
):
    for chunk_x in range(-3, 4):
        for chunk_y in range(-3, 4):
            chunk = (chunk_x + location["tile"][0], chunk_y + location["tile"][1])
            if chunk in chunks[location["room"]]:
                for y in range(0, 16):
                    for x in range(0, 16):
                        tile = (x, y)
                        if (
                            tile in chunks[location["room"]][chunk]
                            and "point"
                            not in chunks[location["room"]][chunk][tile].attributes
                        ):
                            placement = (
                                camera[0] + (x * 64 + chunk[0] * 1024) * zoom,
                                camera[1] + (y * 64 + chunk[1] * 1024 - 32) * zoom,
                            )
                            size = MULTI_TILES.get(
                                chunks[location["room"]][chunk][tile].kind, (1, 1)
                            )
                            if (
                                -64 * zoom * size[0] <= placement[0] <= SCREEN_SIZE[0]
                                and -64 * zoom * size[1]
                                <= placement[1]
                                <= SCREEN_SIZE[1]
                            ):
                                WINDOW.blit(
                                    pg.transform.scale(
                                        IMAGES[chunks[location["room"]][chunk][tile].kind],
                                        (
                                            64 * zoom * size[0],
                                            (32 + 64 * size[1]) * zoom,
                                        ),
                                    ),
                                    placement,
                                )

    if len(inventory) > inventory_number:
        placement = (
            camera[0] + (location["tile"][2] * 64 + location["tile"][0] * 1024 - 4) * zoom,
            camera[1] + (location["tile"][3] * 64 + location["tile"][1] * 1024 - 8) * zoom,
        )
        WINDOW.blit(
            pg.transform.scale(
                IMAGES[list(inventory.keys())[inventory_number]], (32 * zoom, 48 * zoom)
            ),
            placement,
        )

    dark_overlay = pg.Surface(SCREEN_SIZE)
    dark_overlay.fill((19, 17, 18))
    dark_overlay.set_alpha(
        int((1 - math.cos(((tick / DAY_LENGTH * 2) - 1 / 2) * math.pi)) * 95)
    )
    WINDOW.blit(dark_overlay, (0, 0))

    for x in range(-3, 4):
        for y in range(-3, 4):
            if chunk in chunks[location["room"]]:
                chunk = (x + location["tile"][0], y + location["tile"][1])
                for tile in chunks[location["room"]][chunk]:
                    current_tile = chunks[location["room"]][chunk][tile]
                    if "light" in current_tile.attributes:
                        scaled_glow = pg.transform.scale(
                            lights[current_tile.kind][0],
                            (
                                int(lights[current_tile.kind][1] * zoom),
                                int(lights[current_tile.kind][1] * zoom),
                            ),
                        )
                        night_factor = 1 - math.cos(
                            ((tick / DAY_LENGTH * 2) - 1 / 2) * math.pi
                        )
                        scaled_glow.set_alpha(int(night_factor * 180))
                        WINDOW.blit(
                            scaled_glow,
                            (
                                camera[0]
                                + (tile[0] * 64 + chunk[0] * 1024 + 32) * zoom
                                - int(lights[current_tile.kind][1] * zoom / 2),
                                camera[1]
                                + (tile[1] * 64 + chunk[1] * 1024 + 32) * zoom
                                - int(lights[current_tile.kind][1] * zoom / 2),
                            ),
                        )
