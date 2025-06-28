NOISE_TILES = {
    "plains": (((-0.5, -0.25), (0, 0.5), None, {}, "ice"),
        ((-0.5, -0.2), (-0.15, 0), "flint", {}, None),
        ((-0.1, 0.1), (-0.5, -0.4), "big rock", {"rock": 6}, None),
        ((-0.2, 0.1), (-0.5, -0.35), "rock", {}, None),
        ((-0.1, 0.1), (0.45, 0.5), "mushroom", {"spore": 2}, "dirt"),
        ((-0.15, 0.15), (0.4, 0.5), "spore", {}, "dirt"),
        ((0.3, 0.5), (0.2, 0.3), "tree", {"log": 2, "sapling": 2}, "dirt"),
        ((0.25, 0.5), (0.15, 0.35), "treeling", {"log": 1, "sapling": 1}, "dirt"),
        ((0.15, 0.5), (0.1, 0.4), "sapling", {}, "dirt"),
        ((-0.03, -0.02), (0.27, 0.28), "rabbit hole", {"rabbit adult": 2, "rabbit child": 2}, "dirt"),
        ((-0.05, 0), (0.25, 0.3), "carrot", {}, "dirt"),
        ((-0.25, -0.15), (0.2, 0.3), "clay", {}, None),
        ((0.05, 0.1), (0.35, 0.4), "bluebell", {}, "dirt"),
    ),
    "lake": (
        ((0, 0.1), (0.3, 0.5), "clay", {}, None),
        ((-0.5, 0), (-0.1, 0.5), None, {}, "ice"),
        ((-0.5, -0.1), (-0.25, -0.1), "flint", {}, None),
    ),
    "forest": (
        ((0, 0.1), (0.3, 0.35), "bluebell", {}, "dirt"),
        ((-0.1, 0.1), (0.45, 0.5), "mushroom", {"spore": 2}, "dirt"),
        ((-0.25, 0.25), (0.4, 0.5), "spore", {}, "dirt"),
        ((0.25, 0.5), (0, 0.3), "tree", {"log": 2, "sapling": 2}, "dirt"),
        ((0.2, 0.5), (-0.05, 0.35), "treeling", {"log": 1, "sapling": 1}, "dirt"),
        ((0.1, 0.5), (-0.1, 0.4), "sapling", {}, "dirt"),
        ((0, 0.5), (0, 0.5), None, {}, "dirt")
    ),
    "mountain": (
        ((0.3, 0.4), (0.1, 0.2), "coal ore", {"coal": 1}, "pebble"),
        ((0.1, 0.4), (-0.15, 0.15), "stone", {}, "pebble"),
        ((0, 0.5), (-0.2, 0.2), "rock", {}, "pebble"),
        ((-0.1, 0.3), (-0.25, 0.25), None, {}, "pebble")
    )
}
NOISE_STRUCTURES = {
    "forest": (
        ((0, 0.05), "mushroom hut"),
    )
}
ATTRIBUTE_CARE = ("unbreak", "point", "structure")
BIOMES = (
    (-0.05, 0.05, "lake"),
    (-0.25, -0.1, "forest"),
    (0.25, 0.5, "mountain"),
)
DUNGEON_ROOMS = {
    "copper dungeon": {
        (1, 1): ("treasure room",),
        (2, 1): ("library",),
        (2, 2): ("banquet",),
    }
}