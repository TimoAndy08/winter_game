from random import randint
from ast import literal_eval

from .tile_info import TILE_ATTRIBUTES, GROW_CHANCE, GROW_TILES, TILE_HEALTH, FLOOR_HEALTH, FLOOR_BREAK

class Tile:
    def __init__(self, kind: str = None, inventory: dict[str, int] = {}, floor: str = None, health: int = None, max_health: int = None, floor_health: int = None, floor_break: bool = None, attributes: tuple = None):
        self.kind = kind
        self.inventory = inventory
        self.floor = floor
        if attributes == None:
            self.attributes = TILE_ATTRIBUTES.get(kind, ())
        else:
            self.attributes = attributes
        if health == None:
            self.health = TILE_HEALTH.get(kind, 1)
        else:
            self.health = health
        if max_health == None:
            self.max_health = TILE_HEALTH.get(kind, 1)
        else:
            self.max_health = max_health
        if floor_health == None:
            self.floor_health = FLOOR_HEALTH.get(floor, 1)
        else:
            self.floor_health = floor_health
        self.max_floor_health = self.floor_health
        if floor_break == None:
            self.floor_break = FLOOR_BREAK.get(floor, True)
        else:
            self.floor_break = floor_break

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