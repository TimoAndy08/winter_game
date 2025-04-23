import random
from .tile_info import TILE_ATTRIBUTES, GROW_CHANCE, GROW_TILES, TILE_HEALTH


class Tile:
    def __init__(self, kind: str, inventory: dict[str, int]):
        self.kind = kind
        self.attributes = TILE_ATTRIBUTES.get(kind, ())
        self.health = TILE_HEALTH[kind]
        self.max_health = TILE_HEALTH[kind]
        self.inventory = inventory

    def grow(self):
        if random.randint(0, GROW_CHANCE[self.kind]) == 0:
            grow_tile = GROW_TILES[self.kind]
            return Tile(grow_tile[0], grow_tile[1])
        return self

    def to_dict(self):
        if len(self.inventory) == 0:
            return [self.kind]
        return [self.kind, self.inventory]

    @staticmethod
    def from_dict(data):
        if len(data) > 1:
            return Tile(data[0], data[1])
        return Tile(data[0], {})
