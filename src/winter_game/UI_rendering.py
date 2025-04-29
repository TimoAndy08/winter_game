import pygame as pg

from .tile_rendering import window, IMAGES, SCREEN_SIZE
from .tile_info import TILE_ATTRIBUTES, RECIPES, STORAGE

pg.font.init()

UI_SCALE = 2
UI_FONT = pg.font.SysFont("Lucida Console", 10 * UI_SCALE)
BIG_UI_FONT = pg.font.SysFont("Lucida Console", 20 * UI_SCALE)
SLOT_SIZE = (32 * UI_SCALE, 32 * UI_SCALE)
TILE_SIZE = (16 * UI_SCALE, 24 * UI_SCALE)
HALF_SIZE = SCREEN_SIZE[0] // 2
INVENTORY_SIZE = 12

def render_ui(inventory_number, inventory, machine_ui, recipe_number, health, max_health, machine_inventory):

    window.blit(
        pg.transform.scale(IMAGES["health_bar"], (128 * UI_SCALE, 32 * UI_SCALE)),
        (SCREEN_SIZE[0] - 128 * UI_SCALE, 0),
    )
    window.blit(
        pg.transform.scale(IMAGES["health_end"], (16 * UI_SCALE, 16 * UI_SCALE)),
        (SCREEN_SIZE[0] + (health * 64 / max_health - 96) * UI_SCALE, 8 * UI_SCALE),
    )
    pg.draw.rect(
        window,
        (181, 102, 60),
        pg.Rect(
            SCREEN_SIZE[0] - 96 * UI_SCALE,
            8 * UI_SCALE,
            health * 64 * UI_SCALE / max_health,
            16 * UI_SCALE,
        ),
    )
    window.blit(
        UI_FONT.render(f"{health} / {max_health}", False, (206, 229, 242)),
        (SCREEN_SIZE[0] - 80 * UI_SCALE, 12 * UI_SCALE),
    )

    for i in range(0, INVENTORY_SIZE):
        if i == inventory_number:
            window.blit(
                pg.transform.scale(
                    IMAGES["inventory_slot_2"], SLOT_SIZE
                ),
                (
                    SCREEN_SIZE[0] // 2 + (32 * i - 16 * INVENTORY_SIZE) * UI_SCALE,
                    SCREEN_SIZE[1] - 32 * UI_SCALE,
                ),
            )
        else:
            window.blit(
                pg.transform.scale(
                    IMAGES["inventory_slot"], SLOT_SIZE
                ),
                (
                    SCREEN_SIZE[0] // 2 + (32 * i - 16 * INVENTORY_SIZE) * UI_SCALE,
                    SCREEN_SIZE[1] - 32 * UI_SCALE,
                ),
            )
    t = 0
    for item in inventory:
        window.blit(
            pg.transform.scale(IMAGES[item], TILE_SIZE),
            (
                SCREEN_SIZE[0] // 2 + (32 * t - 16 * INVENTORY_SIZE + 8) * UI_SCALE,
                SCREEN_SIZE[1] - 28 * UI_SCALE,
            ),
        )
        window.blit(
            UI_FONT.render(str(inventory[item]), False, (19, 17, 18)),
            (
                SCREEN_SIZE[0] // 2 + (32 * t - 16 * INVENTORY_SIZE + 4) * UI_SCALE,
                SCREEN_SIZE[1] - 24 * UI_SCALE,
            ),
        )
        t += 1
    if "open" in TILE_ATTRIBUTES.get(machine_ui, ()):
        window.blit(
            pg.transform.scale(
                IMAGES["big_inventory_slot"], (320 * UI_SCALE, 128 * UI_SCALE)
            ),
            (SCREEN_SIZE[0] // 2 - 160 * UI_SCALE, SCREEN_SIZE[1] - 160 * UI_SCALE),
        )
        window.blit(
            pg.transform.scale(
                IMAGES["inventory_slot_3"], SLOT_SIZE
            ),
            (SCREEN_SIZE[0] // 2 + 88 * UI_SCALE, SCREEN_SIZE[1] - 80 * UI_SCALE),
        )
        window.blit(
            pg.transform.scale(IMAGES[machine_ui], TILE_SIZE),
            (SCREEN_SIZE[0] // 2 + 96 * UI_SCALE, SCREEN_SIZE[1] - 76 * UI_SCALE),
        )
        if "craft" in TILE_ATTRIBUTES.get(machine_ui, ()):
            current_recipes = RECIPES[machine_ui]
            window.blit(
                pg.transform.scale(
                    IMAGES["big_inventory_slot_2"], (96 * UI_SCALE, 96 * UI_SCALE)
                ),
                (SCREEN_SIZE[0] // 2 - 128 * UI_SCALE, SCREEN_SIZE[1] - 144 * UI_SCALE),
            )
            window.blit(
                pg.transform.scale(
                    IMAGES[current_recipes[recipe_number][0][0]],
                    (48 * UI_SCALE, 72 * UI_SCALE),
                ),
                (SCREEN_SIZE[0] // 2 - 104 * UI_SCALE, SCREEN_SIZE[1] - 132 * UI_SCALE),
            )
            window.blit(
                BIG_UI_FONT.render(
                    str(current_recipes[recipe_number][0][1]), False, (19, 17, 18)
                ),
                (SCREEN_SIZE[0] // 2 - 112 * UI_SCALE, SCREEN_SIZE[1] - 80 * UI_SCALE),
            )
            for inputs in range(0, len(current_recipes[recipe_number][1])):
                position = (SCREEN_SIZE[0] // 2 + ((40 * (inputs % 4) - 32)) * UI_SCALE, SCREEN_SIZE[1] + (32 * (inputs // 4) - 144) * UI_SCALE)
                window.blit(pg.transform.scale(IMAGES["inventory_slot"], SLOT_SIZE), position)
                window.blit(pg.transform.scale(IMAGES[current_recipes[recipe_number][1][inputs][0]], TILE_SIZE), (position[0] + 8 * UI_SCALE, position[1] + 4 * UI_SCALE),)
                window.blit(UI_FONT.render(str(current_recipes[recipe_number][1][inputs][1]), False, (19, 17, 18)), (position[0] + 8 * UI_SCALE, position[1] + 32 * UI_SCALE))
        elif "store" in TILE_ATTRIBUTES.get(machine_ui, ()):
            for item in range(0, STORAGE[machine_ui][0]):
                window.blit(pg.transform.scale(IMAGES["inventory_slot"], SLOT_SIZE), (SCREEN_SIZE[0] // 2 + (32 * (item % 7) - 112) * UI_SCALE, SCREEN_SIZE[1] + (32 * (item // 7) - 144) * UI_SCALE))
            t = 0
            for item in machine_inventory:
                position = (SCREEN_SIZE[0] // 2 + (32 * (t % 7) - 104) * UI_SCALE, SCREEN_SIZE[1] + (32 * (t // 7) - 140) * UI_SCALE)
                window.blit(pg.transform.scale(IMAGES[item], TILE_SIZE), position)
                window.blit(UI_FONT.render(str(machine_inventory[item]), False, (19, 17, 18)), position)
                t += 1
