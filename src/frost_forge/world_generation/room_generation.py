import os
from PIL import Image

from ..info import ROOM_COLORS

def generate_room(structure, room, offset):
    room_image = Image.open(os.path.normpath(os.path.join(__file__, "../../..", f"structures/{structure}/{room}.png"))).convert("RGB")
    chunk = {}
    for x in range(0, room_image.size[0]):
        for y in range(0, room_image.size[1]):
            if room_image.getpixel((x, y)) in ROOM_COLORS:
                chunk[x + offset[0], y + offset[1]] = ROOM_COLORS[room_image.getpixel((x, y))]
    return chunk