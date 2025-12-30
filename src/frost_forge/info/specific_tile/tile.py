from ..render import FPS


MULTI_TILES = {
    "copper constructor": (2, 2),
    "destroyed obelisk": (1, 2),
    "dye bench": (2, 1),
    "manual press": (2, 1),
    "masonry bench": (2, 1),
    "obelisk": (1, 2),
    "packager bench": (2, 1),
    "sawbench": (2, 1),
    "sewbench": (2, 1),
    "steam furnace": (2, 2),
    "wooden bed": (1, 2),
}
PROCESSING_TIME = {
    "burner drill": 30 * FPS,
    "caelium sieve": 15 * FPS,
    "composter": 2 * FPS,
    "copper boiler": 10 * FPS,
    "copper press": 20 * FPS,
    "furnace": 30 * FPS,
    "mana constructor": 10 * FPS,
    "mana converter": 10 * FPS,
    "mana deconstructor": 10 * FPS,
    "steam furnace": 30 * FPS,
    "wood crucible": 60 * FPS,
    "wooden sieve": 15 * FPS,
}
STORAGE = {
    "destroyed void crate": (6, 64),
    "small barrel": (1, 512),
    "small crate": (8, 64),
    "void crate": (8, 64),
}
UNBREAK = {
    "amethyst mineable",
    "coal mineable",
    "copper mineable",
    "copper pit",
    "destroyed obelisk",
    "destroyed void crate",
    "glass lock",
    "left",
    "obelisk",
    "slime summon",
    "up",
    "void",
    "void converter",
    "void crate",
}
MODIFICATIONS = {
    "amethyst pipe": 2,
    "amethyst pump": 2,
    "copper pipe": 2, 
    "copper pump": 2,
    "rail": 6,
    "wood fence": 3,
}
SHEARABLE = {
    "caelium tree": ("caelium leaf", 2, {"kind": "log", "inventory": {"log": 1}}),
    "caelium treeling": ("caelium leaf", 1, {"kind": "log", "inventory": {}}),
    "coal tree": ("coal leaf", 2, {"kind": "log", "inventory": {"log": 1}}),
    "coal treeling": ("coal leaf", 1, {"kind": "log", "inventory": {}}),
    "copper tree": ("copper leaf", 2, {"kind": "log", "inventory": {"log": 1}}),
    "copper treeling": ("copper leaf", 1, {"kind": "log", "inventory": {}}),
    "obelisk": ("mana converter", 1, {"kind": "destroyed obelisk"}),
    "quartz adult": ("quartz", 1, {"kind": "quartz child"}),
    "rabbit adult": ("rabbit fur", 1, {"kind": "furless rabbit", "inventory": {"rabbit meat": 1}}),
    "tin tree": ("tin leaf", 2, {"kind": "log", "inventory": {"log": 1}}),
    "tin treeling": ("tin leaf", 1, {"kind": "log", "inventory": {}}),
    "tree": ("leaf", 2, {"kind": "log", "inventory": {"log": 1}}),
    "treeling": ("leaf", 1, {"kind": "log", "inventory": {}}),
    "void crate": ("mana converter", 1, {"kind": "destroyed void crate"}),
}
RUNES = {
    "amethyst rune": (0, 1),
    "citrine rune": (0, 2),
    "lava rune": (1, 0.8, 5),
    "sapphire rune": (1, 1.26, -3),
}
RUNES_USER = {
    "mana constructor": 2,
    "mana converter": 2,
    "mana deconstructor": 2,
}
CONNECTIONS = {
    "bronze harvester": "connector",
    "copper boiler": "connector",
    "furnace": "connector",
    "steam furnace": "connector",
}
CONTENTS = {
    "copper boiler": {"coal block", "copper tank"},
    "furnace": {"coal block", "furnace accelerator", "lavastone furnace accelerator"},
    "steam furnace": {"coal block", "furnace accelerator", "lavastone furnace accelerator"},
}
CONTENT_VALUES = {
    "coal block": (0, 1),
    "copper tank": (1, -2),
    "furnace accelerator": (1, -1),
    "lavastone furnace accelerator": (1, 0)
}
REQUIREMENTS = {
    "copper tank": ("coal block", 3),
    "furnace accelerator": (("coal block", 2),),
    "lavastone furnace accelerator": (("furnace accelerator", 4),),
}
ITEM_TICK = {
    "basic belt": 1,
}