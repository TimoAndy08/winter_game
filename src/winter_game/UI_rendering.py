import pygame as pg

from .tile_rendering import WINDOW, IMAGES
from .tile_info import TILE_ATTRIBUTES, RECIPES, STORAGE

pg.font.init()

UI_SCALE = 2
UI_FONT = pg.font.SysFont("Lucida Console", 10 * UI_SCALE)
BIG_UI_FONT = pg.font.SysFont("Lucida Console", 20 * UI_SCALE)

def render_ui(
    camera,
    chunks,
    zoom,
    location,
    SCREEN_SIZE,
    INVENTORY_SIZE,
    inventory_number,
    inventory,
    machine_ui,
    recipe_number,
    health,
    max_health,
    machine_inventory,
):
    if (location["mined"][2], location["mined"][3]) in chunks[(location["mined"][0], location["mined"][1])]:
        placement = (
            camera[0]
            + (location["mined"][2] * 64 + location["mined"][0] * 1024) * zoom,
            camera[1]
            + (location["mined"][3] * 64 + location["mined"][1] * 1024 + 60) * zoom,
        )
        last_mined_tile = chunks[(location["mined"][0], location["mined"][1])][(location["mined"][2], location["mined"][3])]
        WINDOW.blit(
            pg.transform.scale(IMAGES["tiny_bar"], (64 * zoom, 16 * zoom)), placement
        )
        pg.draw.rect(
            WINDOW,
            (181, 102, 60),
            pg.Rect(
                placement[0] + 4 * zoom,
                placement[1] + 4 * zoom,
                last_mined_tile.health * 44 * zoom / last_mined_tile.max_health,
                8 * zoom,
            ),
        )

    WINDOW.blit(
        pg.transform.scale(IMAGES["health_bar"], (128 * UI_SCALE, 32 * UI_SCALE)),
        (SCREEN_SIZE[0] - 128 * UI_SCALE, 0),
    )
    WINDOW.blit(
        pg.transform.scale(IMAGES["health_end"], (16 * UI_SCALE, 16 * UI_SCALE)),
        (SCREEN_SIZE[0] + (health * 64 / max_health - 96) * UI_SCALE, 8 * UI_SCALE),
    )
    pg.draw.rect(
        WINDOW,
        (181, 102, 60),
        pg.Rect(
            SCREEN_SIZE[0] - 96 * UI_SCALE,
            8 * UI_SCALE,
            health * 64 * UI_SCALE / max_health,
            16 * UI_SCALE,
        ),
    )
    WINDOW.blit(
        UI_FONT.render(f"{health} / {max_health}", False, (206, 229, 242)),
        (SCREEN_SIZE[0] - 80 * UI_SCALE, 12 * UI_SCALE),
    )

    for i in range(0, INVENTORY_SIZE):
        if i == inventory_number:
            WINDOW.blit(
                pg.transform.scale(
                    IMAGES["inventory_slot_2"], (32 * UI_SCALE, 32 * UI_SCALE)
                ),
                (
                    SCREEN_SIZE[0] // 2 + (32 * i - 16 * INVENTORY_SIZE) * UI_SCALE,
                    SCREEN_SIZE[1] - 32 * UI_SCALE,
                ),
            )
        else:
            WINDOW.blit(
                pg.transform.scale(
                    IMAGES["inventory_slot"], (32 * UI_SCALE, 32 * UI_SCALE)
                ),
                (
                    SCREEN_SIZE[0] // 2 + (32 * i - 16 * INVENTORY_SIZE) * UI_SCALE,
                    SCREEN_SIZE[1] - 32 * UI_SCALE,
                ),
            )
    t = 0
    for item in inventory:
        WINDOW.blit(
            pg.transform.scale(IMAGES[item], (16 * UI_SCALE, 24 * UI_SCALE)),
            (
                SCREEN_SIZE[0] // 2 + (32 * t - 16 * INVENTORY_SIZE + 8) * UI_SCALE,
                SCREEN_SIZE[1] - 28 * UI_SCALE,
            ),
        )
        WINDOW.blit(
            UI_FONT.render(str(inventory[item]), False, (19, 17, 18)),
            (
                SCREEN_SIZE[0] // 2 + (32 * t - 16 * INVENTORY_SIZE + 4) * UI_SCALE,
                SCREEN_SIZE[1] - 24 * UI_SCALE,
            ),
        )
        t += 1
    if "open" in TILE_ATTRIBUTES.get(machine_ui, ()):
        WINDOW.blit(
            pg.transform.scale(
                IMAGES["big_inventory_slot"], (320 * UI_SCALE, 128 * UI_SCALE)
            ),
            (SCREEN_SIZE[0] // 2 - 160 * UI_SCALE, SCREEN_SIZE[1] - 160 * UI_SCALE),
        )
        WINDOW.blit(
            pg.transform.scale(
                IMAGES["inventory_slot_3"], (32 * UI_SCALE, 32 * UI_SCALE)
            ),
            (SCREEN_SIZE[0] // 2 + 88 * UI_SCALE, SCREEN_SIZE[1] - 80 * UI_SCALE),
        )
        WINDOW.blit(
            pg.transform.scale(IMAGES[machine_ui], (16 * UI_SCALE, 24 * UI_SCALE)),
            (SCREEN_SIZE[0] // 2 + 96 * UI_SCALE, SCREEN_SIZE[1] - 76 * UI_SCALE),
        )
        if "craft" in TILE_ATTRIBUTES.get(machine_ui, ()):
            current_recipes = RECIPES[machine_ui]
            WINDOW.blit(
                pg.transform.scale(
                    IMAGES["big_inventory_slot_2"], (96 * UI_SCALE, 96 * UI_SCALE)
                ),
                (SCREEN_SIZE[0] // 2 - 128 * UI_SCALE, SCREEN_SIZE[1] - 144 * UI_SCALE),
            )
            WINDOW.blit(
                pg.transform.scale(
                    IMAGES[current_recipes[recipe_number][0][0]],
                    (48 * UI_SCALE, 72 * UI_SCALE),
                ),
                (SCREEN_SIZE[0] // 2 - 104 * UI_SCALE, SCREEN_SIZE[1] - 132 * UI_SCALE),
            )
            WINDOW.blit(
                BIG_UI_FONT.render(
                    str(current_recipes[recipe_number][0][1]), False, (19, 17, 18)
                ),
                (SCREEN_SIZE[0] // 2 - 112 * UI_SCALE, SCREEN_SIZE[1] - 80 * UI_SCALE),
            )
            for inputs in range(0, len(current_recipes[recipe_number][1])):
                WINDOW.blit(
                    pg.transform.scale(
                        IMAGES["inventory_slot"], (32 * UI_SCALE, 32 * UI_SCALE)
                    ),
                    (
                        SCREEN_SIZE[0] // 2 + (40 * (inputs % 4) - 32) * UI_SCALE,
                        SCREEN_SIZE[1] + (32 * (inputs // 4) - 144) * UI_SCALE,
                    ),
                )
                WINDOW.blit(
                    pg.transform.scale(
                        IMAGES[current_recipes[recipe_number][1][inputs][0]],
                        (16 * UI_SCALE, 24 * UI_SCALE),
                    ),
                    (
                        SCREEN_SIZE[0] // 2 + (40 * (inputs % 4) - 24) * UI_SCALE,
                        SCREEN_SIZE[1] + (32 * (inputs // 4) - 140) * UI_SCALE,
                    ),
                )
                WINDOW.blit(
                    UI_FONT.render(
                        str(current_recipes[recipe_number][1][inputs][1]),
                        False,
                        (19, 17, 18),
                    ),
                    (
                        SCREEN_SIZE[0] // 2 + (40 * (inputs % 4) - 24) * UI_SCALE,
                        SCREEN_SIZE[1] + (32 * (inputs // 4) - 112) * UI_SCALE,
                    ),
                )
        elif "store" in TILE_ATTRIBUTES.get(machine_ui, ()):
            for item in range(0, STORAGE[machine_ui][0]):
                WINDOW.blit(
                    pg.transform.scale(
                        IMAGES["inventory_slot"], (32 * UI_SCALE, 32 * UI_SCALE)
                    ),
                    (
                        SCREEN_SIZE[0] // 2 + (32 * (item % 7) - 112) * UI_SCALE,
                        SCREEN_SIZE[1] + (32 * (item // 7) - 144) * UI_SCALE,
                    ),
                )
            t = 0
            for item in machine_inventory:
                WINDOW.blit(
                    pg.transform.scale(IMAGES[item], (16 * UI_SCALE, 24 * UI_SCALE)),
                    (
                        SCREEN_SIZE[0] // 2 + (32 * (t % 7) - 104) * UI_SCALE,
                        SCREEN_SIZE[1] + (32 * (t // 7) - 140) * UI_SCALE,
                    ),
                )
                WINDOW.blit(
                    UI_FONT.render(str(machine_inventory[item]), False, (19, 17, 18)),
                    (
                        SCREEN_SIZE[0] // 2 + (32 * (t % 7) - 104) * UI_SCALE,
                        SCREEN_SIZE[1] + (32 * (t // 7) - 140) * UI_SCALE,
                    ),
                )
                t += 1