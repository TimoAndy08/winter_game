from ..info import UNBREAK, TILE_ATTRIBUTES, TILE_HEALTH

class Tile:
    def __init__(self, kind: str = None, inventory: dict[str, int] = None, floor: str = None, health: int = None, max_health: int = None, floor_health: int = None, attributes: tuple = None, unbreak: bool = None, spawn: tuple[int, int] = None, recipe: int = None):
        self.kind = kind
        self.floor = floor
        if inventory == None:
            self.inventory = {}
        else:
            self.inventory = inventory
        if unbreak == None:
            self.unbreak = (kind in UNBREAK)
        else:
            self.unbreak = unbreak
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
            self.floor_health = TILE_HEALTH.get(floor, 1)
        else:
            self.floor_health = floor_health
        if recipe == None:
            self.recipe = 0
        else:
            self.recipe = recipe
        self.max_floor_health = self.floor_health
        self.spawn = spawn

    def to_dict(self):
        saving = {}
        if isinstance(self.kind, str) and "point" not in self.attributes:
            saving[0] = self.kind
        if len(self.inventory) > 0:
            saving[1] = self.inventory
        if isinstance(self.floor, str):
            saving[2] = self.floor
        if self.unbreak and self.unbreak not in UNBREAK:
            saving[3] = 1
        if isinstance(self.spawn, tuple):
            saving[4] = self.spawn
        if self.recipe > 0:
            saving[5] = self.recipe
        return str(saving)

    @staticmethod
    def from_dict(data):
        loading = [None] * 7
        if 0 in data:
            loading[0] = data[0]
        if 1 in data:
            loading[1] = data[1]
        if 2 in data:
            loading[2] = data[2]
        if 3 in data:
            loading[4] = True
        if 4 in data:
            loading[4] = data[4]
        if 5 in data:
            loading[5] = data[5]
        return Tile(loading[0], loading[1], loading[2], unbreak = loading[3], spawn = loading[4], recipe = loading[5])