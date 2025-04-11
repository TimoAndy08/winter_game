import random

tile_attributes = {
    "player": ("open", "craft"),
    "sapling": ("grow"),
    "treeling": ("grow", "no_pickup"),
    "tree": ("no_pickup"),
    "spore": ("grow"),
    "mushroom": ("eat"),
    "carrot": ("grow", "eat"),
    "carroot": ("no_pickup"),
    "rabbit child": ("grow", "move", "no_pickup"),
    "rabbit adult": ("move", "no_pickup"),
    "roasted mushroom": ("eat",),
    "mushroom stew": ("eat",),
    "workbench": ("open", "craft"),
    "campfire": ("open", "craft", "light"),
    "sawbench": ("open", "craft", "multi"),
    "manual press": ("open", "craft", "multi"),
    "small crate": ("open", "store"),
    "small barrel": ("open", "store"),
    "wooden cabin": ("enter", "multi"),
    "wooden door": ("exit",),
    "wooden bed": ("sleep", "multi"),
    "rabbit meat": ("eat",),
    "roasted rabbit meat": ("eat",),
    "left": ("point",),
    "up": ("point",),
    "junk": ("no_pickup"),
    "corpse": ("no_pickup"),
}

class Tile:
    def __init__(
        self, kind: str, health: int, resistance: int, inventory: dict[str, int]
    ):
        self.kind = kind
        self.attributes = tile_attributes.get(kind, ())
        self.health = health
        self.max_health = health
        self.resistance = resistance
        self.inventory = inventory

    def grow(self):
        if random.randint(0, grow_chance[self.kind]) == 0:
            return grow_tiles[self.kind]
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


grow_tiles = {
    "sapling": Tile("treeling", 9, 0, {"wood": 2, "sapling": 1}),
    "treeling": Tile("tree", 15, 1, {"wood": 4, "sapling": 2}),
    "spore": Tile("mushroom", 10, 0, {"spore": 2, "mushroom": 1}),
    "carrot": Tile("carroot", 8, 0, {"carrot": 2}),
    "rabbit child": Tile("rabbit adult", 8, 1, {"rabbit fur": 1, "rabbit meat": 2}),
}
grow_chance = {
    "sapling": 5000,
    "treeling": 10000,
    "spore": 7500,
    "carrot": 10000,
    "rabbit child": 12500,
}
