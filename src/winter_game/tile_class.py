import random
from .tile_info import TILE_ATTRIBUTES, GROW_CHANCE, GROW_TILES

class Tile:
    def __init__(self, kind: str, health: int, inventory: dict[str, int]):
        self.kind = kind
        self.attributes = TILE_ATTRIBUTES.get(kind, ())
        self.health = health
        self.max_health = health
        self.inventory = inventory

    def grow(self):
        if random.randint(0, GROW_CHANCE[self.kind]) == 0:
            grow_tile = GROW_TILES[self.kind]
            return Tile(grow_tile[0], grow_tile[1], grow_tile[2])
        return self

    def to_dict(self):
        if len(self.inventory) == 0:
            return [self.kind, self.health]
        return [self.kind, self.health, self.inventory]

    @staticmethod
    def from_dict(data):
        if len(data) > 2:
            return Tile(data[0], data[1], data[2])
        return Tile(data[0], data[1], {})