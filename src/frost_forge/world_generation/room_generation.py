import os
from PIL import Image, ImageOps
from random import randint

from ..info import ROOM_COLORS
from .loot_calculation import calculate_loot


def generate_room(structure, room, rotate=True, vary=True):
    room_image = Image.open(
        os.path.normpath(
            os.path.join(__file__, "../../..", f"structures/{structure}/{room}.png")
        )
    ).convert("RGB")
    room_chunks = {}
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
            if room_image.getpixel((x, y)) in ROOM_COLORS[structure]:
                tile = ROOM_COLORS[structure][room_image.getpixel((x, y))]
                room_chunks[x, y] = {}
                for index in tile:
                    room_chunks[x, y][index] = tile[index]
                if "loot" in room_chunks[x, y]:
                    room_chunks[x, y] = calculate_loot(room_chunks[x, y])
    return room_chunks
