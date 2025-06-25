NOISE_TILES = {
    "lake": (
        (-0.18, -0.15, "clay", {}, None),
        (-0.15, 0.2, None, {}, "ice"),
        (0.25, 0.35, "flint", {}, None),
    ),
    "mushroom forest": (
        (0.2, 0.21, "mushroom hut", {}, None),
        (-0.05, 0.1, "mushroom", {"spore": 2}, "dirt"),
        (-0.2, 0.2, "spore", {}, "dirt"),
        (-0.5, 0.5, None, {}, "dirt")
    ),
    "forest": (
        (-0.25, 0.2, "treeling", {"wood": 2, "sapling": 1}, "dirt"),
        (0.35, 0.4, "bluebell", {}, "dirt"),
        (-0.3, 0.3, None, {}, "dirt"),
    ),
    "carrot plains": (
        (-0.2, 0, "carrot", {}, "dirt"),
        (0, 0.01, "rabbit hole", {"rabbit adult": 2, "rabbit child": 2}, "dirt"),
        (0.3, 0.35, "treeling", {"wood": 2, "sapling": 1}, "dirt"),
        (0.35, 0.4, "bluebell", {}, "dirt"),
    ),
    "mountain": (
        (-0.02, 0, "big rock", {"rock": 6}, None),
        (-0.1, 0.05, "rock", {}, "pebble"),
        (0.2, 0.35, "stone", {}, "pebble"),
        (0.15, 0.45, "rock", {}, "pebble"),
        (0.45, 0.5, "coal ore", {"coal": 1}, "pebble"),
        (-0.2, 0.15, None, {}, "pebble")
    ),
    "plains": (),
}
ATTRIBUTE_CARE = ("unbreak", "point", "structure")
BIOMES = (
    (-0.04, 0, "lake"),
    (-0.22, -0.2, "mushroom forest"),
    (-0.25, -0.1, "forest"),
    (0.1, 0.12, "carrot plains"),
    (0.25, 0.5, "mountain"),
    (-0.5, 0.5, "plains"),
)