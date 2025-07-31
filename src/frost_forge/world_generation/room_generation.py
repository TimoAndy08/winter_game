import os
from PIL import Image, ImageOps
from random import randint, random

from ..info import ROOM_COLORS, LOOT_TABLES
from .loot_calculation import calculate_loot


def generate_room(structure, room, offset, rotate = True, vary = True):
    room_image = Image.open(os.path.normpath(os.path.join(__file__, "../../..", f"structures/{structure}/{room}.png"))).convert("RGB")
    chunk = {}
    if vary:
        variation = randint(0, 15)
        if variation % 2:
            room_image = ImageOps.mirror(room_image)
        if (variation // 2) % 2:
            room_image = ImageOps.flip(room_image)
        if rotate:
            room_image = room_image.rotate((variation // 4) * 90)
    for x in range(0, room_image.size[0]):
        for y in range(0, room_image.size[1]):
            if room_image.getpixel((x, y)) in ROOM_COLORS:
                placement = x + offset[0], y + offset[1]
                tile = ROOM_COLORS[room_image.getpixel((x, y))]
                chunk[placement] = {}
                for index in tile:
                    chunk[placement][index] = tile[index]
                if "loot" in chunk[placement]:
                    chunk[placement] = calculate_loot(chunk[placement])
    return chunk