import pygame as pg


MENU_FONT = pg.font.SysFont("Lucida Console", 50)


def render_text(window, text, position, images):
    window.blit(pg.transform.scale(images["left text"], (25, 50)), (0, position * 75))
    window.blit(MENU_FONT.render(text, False, (19, 17, 18)), (30, position * 75))
    window.blit(
        pg.transform.scale(images["right text"], (25, 50)),
        (30 + 30 * len(text), position * 75),
    )
    return window
