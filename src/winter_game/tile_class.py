from random import randint
from ast import literal_eval

from .tile_info import TILE_ATTRIBUTES, GROW_CHANCE, GROW_TILES, TILE_HEALTH, FLOOR_HEALTH


class Tile:
    def __init__(self, kind: str = None, inventory: dict[str, int] = {}, floor: str = None, health: int = None, max_health: int = None):
        self.kind = kind
        self.floor = floor
        self.attributes = TILE_ATTRIBUTES.get(kind, ())
        if health == None:
            self.health = TILE_HEALTH.get(kind, 1)
        else:
            self.health = health
        if max_health == None:
            self.max_health = TILE_HEALTH.get(kind, 1)
        else:
            self.max_health = max_health
        self.floor_health = FLOOR_HEALTH.get(floor, 1)
        self.inventory = inventory

    def grow(self):
        if randint(0, GROW_CHANCE[self.kind]) == 0:
            grow_tile = GROW_TILES[self.kind]
            return Tile(grow_tile[0], grow_tile[1])
        return self

    def to_dict(self):
        if len(self.inventory) == 0:
            return f"{self.kind}"
        return f"{self.kind}_{self.inventory}"

    @staticmethod
    def from_dict(data):
        data_parts = data.split("_")
        if len(data_parts) > 1:
            return Tile(data_parts[0], literal_eval(data_parts[1]))
        return Tile(data_parts[0])
    
    def move(tile):
        return Tile(tile.kind, tile.inventory)