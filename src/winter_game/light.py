import pygame as pg


def create_light_surface(intensity: int, color: tuple[int, int, int]):
    light_surface = pg.Surface((32, 32), pg.SRCALPHA)
    for i in range(16, 0, -1):
        alpha = intensity - int((i / 16) * intensity)
        pg.draw.circle(light_surface, (*color, alpha), (16, 16), i)
    return light_surface


lights = {"campfire": (create_light_surface(170, (181, 102, 60)), 832)}
