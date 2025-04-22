import random
from .tile_info import TILE_ATTRIBUTES, GROW_CHANCE, GROW_TILES


class Tile:
    def __init__(
        self, kind: str, health: int, resistance: int, inventory: dict[str, int]
    ):
        self.kind = kind
        self.attributes = TILE_ATTRIBUTES.get(kind, ())
        self.health = health
        self.max_health = health
        self.resistance = resistance
        self.inventory = inventory

    def grow(self):
        if random.randint(0, GROW_CHANCE[self.kind]) == 0:
            grow_tile = GROW_TILES[self.kind]
            return Tile(grow_tile[0], grow_tile[1], grow_tile[2], grow_tile[3])
        return self

    def to_dict(self):
        return {
            "kind": self.kind,
            "health": self.health,
            "resistance": self.resistance,
            "inventory": self.inventory,
        }

    @staticmethod
    def from_dict(data):
        return Tile(
            kind=data["kind"],
            health=data["health"],
            resistance=data["resistance"],
            inventory=data.get("inventory", {}),
        )
