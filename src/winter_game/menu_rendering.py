import pygame as pg

from .tile_rendering import window

pg.font.init()

MENU_FONT = pg.font.SysFont("Lucida Console", 50)
CONTROL_NAMES = ["Move up ", "Move left ", "Move down ", "Move right", "Inventory ", "Zoom in", "Zoom out"]

def render_menu(
    menu_placement: str,
    save_file_name: str,
    control_adjusted: int,
    controls: list,
):
    window.fill((206, 229, 242))
    if menu_placement == "load_save":
        window.blit(MENU_FONT.render("Load save?", False, (19, 17, 18)), (0, 0))
        window.blit(MENU_FONT.render("Yes", False, (19, 17, 18)), (0, 100))
        window.blit(MENU_FONT.render("No", False, (19, 17, 18)), (0, 200))
    elif menu_placement.split("_")[0] == "save":
        if menu_placement == "save_creation":
            window.blit(
                MENU_FONT.render("Name your new save?", False, (19, 17, 18)), (0, 0)
            )
        if menu_placement == "save_selection":
            window.blit(
                MENU_FONT.render("Which save to load?", False, (19, 17, 18)), (0, 0)
            )
        window.blit(MENU_FONT.render(save_file_name, False, (19, 17, 18)), (0, 100))
        window.blit(MENU_FONT.render("Proceed", False, (19, 17, 18)), (0, 200))
    elif menu_placement.split("_")[0] == "options":
        if menu_placement == "options_game":
            window.blit(MENU_FONT.render("Return to game", False, (19, 17, 18)), (0, 0))
            window.blit(
                MENU_FONT.render("Save and Quit", False, (19, 17, 18)), (0, 100)
            )
        elif menu_placement == "options_main":
            window.blit(MENU_FONT.render("Back to menu", False, (19, 17, 18)), (0, 0))
        window.blit(MENU_FONT.render("Controls options", False, (19, 17, 18)), (0, 200))
    elif menu_placement == "main_menu":
        window.blit(MENU_FONT.render("Play", False, (19, 17, 18)), (0, 0))
        window.blit(MENU_FONT.render("Options", False, (19, 17, 18)), (0, 100))
        window.blit(MENU_FONT.render("Quit Game", False, (19, 17, 18)), (0, 200))
    elif menu_placement == "controls_options":
        window.blit(MENU_FONT.render("Proceed", False, (19, 17, 18)), (0, 0))
        window.blit(
            MENU_FONT.render(
                f"{CONTROL_NAMES[control_adjusted]}: {chr(controls[control_adjusted])}",
                False,
                (19, 17, 18),
            ),
            (0, 100),
        )
