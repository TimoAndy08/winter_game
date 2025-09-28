from random import random

from ...info import GROW_CHANCE, GROW_TILES, FPS


def grow(tile, guarantee = False):
    old_kind = tile["kind"]
    if random() < 1 / (GROW_CHANCE[old_kind] * FPS) or guarantee:
        for info in GROW_TILES[old_kind]:
            tile[info] = GROW_TILES[old_kind][info]
    return tile