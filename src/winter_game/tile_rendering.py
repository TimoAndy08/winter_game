from math import pi, cos
from os import listdir, path

import pygame as pg

from .tile_info import MULTI_TILES, FLOOR
from .light import LIGHTS

pg.init()
window = pg.display.set_mode((0, 0), pg.FULLSCREEN)

SCREEN_SIZE = (pg.display.Info().current_w, pg.display.Info().current_h)
TILE_SIZE = 64
HALF_SIZE = TILE_SIZE // 2
CHUNK_SIZE = 16 * TILE_SIZE
IMAGES = {}
FPS = 60
DAY_LENGTH = 60 * 24 * FPS
SPRITES_FOLDER = "src/sprites"

for filename in listdir(SPRITES_FOLDER):
    IMAGES[filename.split(".")[0]] = pg.image.load(
        path.join(SPRITES_FOLDER, filename)).convert_alpha()

def render_tiles(
    chunks,
    location,
    zoom,
    target_zoom,
    inventory,
    inventory_number,
    tick,
    camera,
):
    if location["room"] == (0, 0, 0, 0):
        window.fill((206, 229, 242))
    else:
        window.fill((19, 17, 18))
    player_pixel_position = (location["real"][2] * TILE_SIZE + location["real"][0] * CHUNK_SIZE + HALF_SIZE, location["real"][3] * TILE_SIZE + location["real"][1] * CHUNK_SIZE + HALF_SIZE)
    interpolation = max(min(abs(1 - target_zoom / zoom) * 0.5 + 0.2, 1.0), 0.0)
    camera = ((SCREEN_SIZE[0] / 2 - player_pixel_position[0] * zoom) * interpolation + camera[0] * (1 - interpolation), (SCREEN_SIZE[1] / 2 - player_pixel_position[1] * zoom) * interpolation + camera[1] * (1 - interpolation))
    scaled_image = {}
    for image in IMAGES:
        if image in FLOOR:
            scaled_image[image] = pg.transform.scale(IMAGES[image], ((TILE_SIZE + 2) * zoom, (TILE_SIZE + 2) * zoom))
        else:
            size = MULTI_TILES.get(image, (1, 1))
            scaled_image[image] = pg.transform.scale(IMAGES[image], ((TILE_SIZE * size[0] + 2) * zoom, ((size[1] + 1 / 2) * TILE_SIZE + 2) * zoom))
    for chunk_y in range(-3, 4):
        for chunk_x in range(-3, 4):
            chunk = (chunk_x + location["tile"][0], chunk_y + location["tile"][1])
            if chunk in chunks:
                for y in range(0, 16):
                    for x in range(0, 16):
                        tile = (x, y)
                        if tile in chunks[chunk] and "point" not in chunks[chunk][tile].attributes:
                            current_tile = chunks[chunk][tile]
                            placement = (camera[0] + (x * TILE_SIZE + chunk[0] * CHUNK_SIZE) * zoom, camera[1] + (y * TILE_SIZE + chunk[1] * CHUNK_SIZE - HALF_SIZE) * zoom,)
                            if -TILE_SIZE * zoom * size[0] <= placement[0] <= SCREEN_SIZE[0] and -TILE_SIZE * zoom * size[1] * 3 / 2 <= placement[1] <= SCREEN_SIZE[1]:
                                if isinstance(chunks[chunk][tile].floor, str):
                                    window.blit(scaled_image[current_tile.floor], (placement[0], placement[1] + HALF_SIZE * zoom))
                                if isinstance(chunks[chunk][tile].kind, str):
                                    window.blit(scaled_image[current_tile.kind], placement)
    if len(inventory) > inventory_number:
        placement = (
            camera[0]
            + (location["tile"][2] * TILE_SIZE + location["tile"][0] * CHUNK_SIZE - 4) * zoom,
            camera[1]
            + (location["tile"][3] * TILE_SIZE + location["tile"][1] * CHUNK_SIZE - 8) * zoom,
        )
        window.blit(
            pg.transform.scale(
                IMAGES[list(inventory.keys())[inventory_number]], (HALF_SIZE * zoom, 3 * TILE_SIZE // 4 * zoom)
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
                                + (tile[0] * TILE_SIZE + chunk[0] * CHUNK_SIZE + HALF_SIZE) * zoom
                                - int(LIGHTS[current_tile.kind][1] * zoom / 2),
                                camera[1]
                                + (tile[1] * TILE_SIZE + chunk[1] * CHUNK_SIZE + HALF_SIZE) * zoom
                                - int(LIGHTS[current_tile.kind][1] * zoom / 2),
                            ),
                        )
    
    if location["mined"][1] in chunks[location["mined"][0]]:
        placement = (
            camera[0]
            + (location["mined"][1][0] * TILE_SIZE + location["mined"][0][0] * CHUNK_SIZE) * zoom,
            camera[1]
            + (location["mined"][1][1] * TILE_SIZE + location["mined"][0][1] * CHUNK_SIZE + 60) * zoom,
        )
        last_mined_tile = chunks[location["mined"][0]][location["mined"][1]]
        window.blit(pg.transform.scale(IMAGES["tiny_bar"], (TILE_SIZE * zoom, 16 * zoom)), placement)
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
    return camera