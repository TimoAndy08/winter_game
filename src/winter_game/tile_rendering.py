from math import pi, cos
import os

import pygame as pg

from .tile_info import MULTI_TILES, FLOOR
from .light import LIGHTS

pg.init()
window = pg.display.set_mode((0, 0), pg.FULLSCREEN)

SCREEN_SIZE = (pg.display.Info().current_w, pg.display.Info().current_h)
TILE_SIZE = 64
CHUNK_SIZE = 16 * TILE_SIZE
IMAGES = {}
FPS = 60
DAY_LENGTH = 60 * 24 * FPS
SPRITES_FOLDER = "src/sprites"
for filename in os.listdir(SPRITES_FOLDER):
    IMAGES[filename.split(".")[0]] = pg.image.load(
        os.path.join(SPRITES_FOLDER, filename)).convert_alpha()

def render_tiles(
    chunks,
    location,
    zoom,
    inventory,
    inventory_number,
    tick,
):
    if location["room"] == (0, 0, 0, 0):
        window.fill((206, 229, 242))
    else:
        window.fill((19, 17, 18))
    camera = [SCREEN_SIZE[0] / 2 - ((location["tile"][2] * TILE_SIZE + location["tile"][0] * CHUNK_SIZE + 32) * zoom), SCREEN_SIZE[1] / 2 - ((location["tile"][3] * TILE_SIZE + location["tile"][1] * CHUNK_SIZE + 32) * zoom)]
    scaled_image = {}
    for image in IMAGES:
        if image in FLOOR:
            scaled_image[image] = pg.transform.scale(IMAGES[image], (64 * zoom, 64 * zoom))
        else:
            size = MULTI_TILES.get(image, (1, 1))
            scaled_image[image] = pg.transform.scale(IMAGES[image], (64 * size[0] * zoom, (size[1] * 64 + 32) * zoom))
    for chunk_x in range(-3, 4):
        for chunk_y in range(-3, 4):
            chunk = (chunk_x + location["tile"][0], chunk_y + location["tile"][1])
            if chunk in chunks:
                for y in range(0, 16):
                    for x in range(0, 16):
                        tile = (x, y)
                        if tile in chunks[chunk] and "point" not in chunks[chunk][tile].attributes:
                            current_tile = chunks[chunk][tile]
                            placement = (camera[0] + (x * 64 + chunk[0] * 1024) * zoom, camera[1] + (y * 64 + chunk[1] * 1024 - 32) * zoom,)
                            if -64 * zoom * size[0] <= placement[0] <= SCREEN_SIZE[0] and -64 * zoom * size[1] <= placement[1] <= SCREEN_SIZE[1]:
                                if isinstance(chunks[chunk][tile].floor, str):
                                    window.blit(scaled_image[current_tile.floor], (placement[0], placement[1] + 32 * zoom))
                                if isinstance(chunks[chunk][tile].kind, str):
                                    window.blit(scaled_image[current_tile.kind], placement)
    if len(inventory) > inventory_number:
        placement = (
            camera[0]
            + (location["tile"][2] * 64 + location["tile"][0] * 1024 - 4) * zoom,
            camera[1]
            + (location["tile"][3] * 64 + location["tile"][1] * 1024 - 8) * zoom,
        )
        window.blit(
            pg.transform.scale(
                IMAGES[list(inventory.keys())[inventory_number]], (32 * zoom, 48 * zoom)
            ),
            placement,
        )

    dark_overlay = pg.Surface(SCREEN_SIZE)
    dark_overlay.fill((19, 17, 18))
    dark_overlay.set_alpha(
        int((1 - cos(((tick / DAY_LENGTH * 2) - 1 / 2) * pi)) * 95)
    )
    window.blit(dark_overlay, (0, 0))

    for x in range(-3, 4):
        for y in range(-3, 4):
            if chunk in chunks:
                chunk = (x + location["tile"][0], y + location["tile"][1])
                for tile in chunks[chunk]:
                    current_tile = chunks[chunk][tile]
                    if "light" in current_tile.attributes:
                        scaled_glow = pg.transform.scale(
                            LIGHTS[current_tile.kind][0],
                            (
                                int(LIGHTS[current_tile.kind][1] * zoom),
                                int(LIGHTS[current_tile.kind][1] * zoom),
                            ),
                        )
                        night_factor = 1 - cos(
                            ((tick / DAY_LENGTH * 2) - 1 / 2) * pi
                        )
                        scaled_glow.set_alpha(int(night_factor * 180))
                        window.blit(
                            scaled_glow,
                            (
                                camera[0]
                                + (tile[0] * 64 + chunk[0] * 1024 + 32) * zoom
                                - int(LIGHTS[current_tile.kind][1] * zoom / 2),
                                camera[1]
                                + (tile[1] * 64 + chunk[1] * 1024 + 32) * zoom
                                - int(LIGHTS[current_tile.kind][1] * zoom / 2),
                            ),
                        )
    
    if location["mined"][1] in chunks[location["mined"][0]]:
        placement = (
            camera[0]
            + (location["mined"][1][0] * 64 + location["mined"][0][0] * 1024) * zoom,
            camera[1]
            + (location["mined"][1][1] * 64 + location["mined"][0][1] * 1024 + 60) * zoom,
        )
        last_mined_tile = chunks[location["mined"][0]][location["mined"][1]]
        window.blit(pg.transform.scale(IMAGES["tiny_bar"], (64 * zoom, 16 * zoom)), placement)
        if isinstance(chunks[location["mined"][0]][location["mined"][1]].kind, str):
            pg.draw.rect(
                window,
                (181, 102, 60),
                pg.Rect(
                    placement[0] + 4 * zoom,
                    placement[1] + 4 * zoom,
                    last_mined_tile.health * 44 * zoom / last_mined_tile.max_health,
                    8 * zoom,
                ),
            )
        elif isinstance(chunks[location["mined"][0]][location["mined"][1]].floor, str):
            pg.draw.rect(
                window,
                (181, 102, 60),
                pg.Rect(
                    placement[0] + 4 * zoom,
                    placement[1] + 4 * zoom,
                    last_mined_tile.floor_health * 44 * zoom / last_mined_tile.max_floor_health,
                    8 * zoom,
                ),
            )
