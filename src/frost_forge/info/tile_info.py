from .render_info import FPS


FERTILIZER_SPAWN = (
    (0.002, "bluebell"),
    (0.005, "potato"),
    (0.01, "carrot"),
    (0.02, "spore"),
    (0.035, "sapling"),
)
FERTILIZER_EFFICIENCY = {
    "fertilizer": 20,
    "compost": 1,
}
FOOD = {
    "carrot": 2,
    "mushroom": 1,
    "mushroom stew": 6,
    "potato": 3,
    "rabbit meat": 1,
    "roasted mushroom": 3,
    "roasted rabbit meat": 4,
}
FLOOR = {
    "brick floor",
    "dirt",
    "ice",
    "log floor",
    "mushroom door",
    "mushroom door open",
    "mushroom floor",
    "pebble",
    "stone brick floor",
    "stone floor",
    "void",
    "water",
    "wood door",
    "wood door open",
    "wood floor",
}
FLOOR_TYPE = {
    "dirt": "soil",
    "ice": "block",
    "mushroom door": "door",
    "mushroom door open": "open",
    "void": "block",
    "water": "fluid",
    "wood door": "door",
    "wood door open": "open",
}
GROW_CHANCE = {
    "carrot": 160,
    "potato": 240,
    "rabbit child": 200,
    "sapling": 80,
    "spore": 120,
    "treeling": 160,
}
GROW_TILES = {
    "carrot": {"kind": "carroot", "inventory": {"carrot": 2}},
    "potato": {"kind": "potatoo", "inventory": {"potato": 2}},
    "rabbit child": {"kind": "rabbit adult", "inventory": {"rabbit fur": 1, "rabbit meat": 2}},
    "sapling": {"kind": "treeling", "inventory": {"sapling": 1, "log": 1}},
    "spore": {"kind": "mushroom", "inventory": {"mushroom": 1, "spore": 2}},
    "treeling": {"kind": "tree", "inventory": {"sapling": 2, "log": 2}},
}
MULTI_TILES = {
    "big rock": (2, 2),
    "furnace": (2, 2),
    "manual press": (2, 1),
    "masonry bench": (2, 1),
    "obelisk": (1, 2),
    "sawbench": (2, 1),
    "wooden bed": (1, 2),
}
PROCESSING_TIME = {
    "bonsai pot": 40 * FPS,
    "composter": 2 * FPS,
    "furnace": 10 * FPS,
}
STORAGE = {
    "small barrel": (1, 512),
    "small crate": (9, 48),
}
UNBREAK = {
    "glass lock",
    "left",
    "obelisk",
    "player",
    "rabbit hole",
    "up",
    "void",
}
UNOBTAINABLE = {
    "big rock",
    "carroot",
    "coal ore",
    "corpse",
    "junk",
    "potatoo",
    "rabbit adult",
    "rabbit child",
    "tree",
    "treeling",
}