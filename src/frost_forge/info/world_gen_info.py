NOISE_TILES = (
    ((-0.5, -0.25), (0, 0.5), None, {}, "ice"),
    ((-0.5, -0.2), (-0.15, 0), "flint", {}, None),
    ((-0.1, 0.1), (-0.5, -0.4), "big rock", {"rock": 6}, None),
    ((-0.2, 0.1), (-0.5, -0.35), "rock", {}, None),
    ((0.1, 0.2), (-0.5, -0.4), "coal ore", {"coal": 1}, None),
    ((-0.03, 0.03), (0.47, 0.5), "mushroom hut", {}, None),
    ((-0.1, 0.1), (0.45, 0.5), "mushroom", {"spore": 2}, "dirt"),
    ((-0.15, 0.15), (0.4, 0.5), "spore", {}, "dirt"),
    ((0.3, 0.5), (0.2, 0.3), "tree", {"wood": 4, "sapling": 2}, "dirt"),
    ((0.25, 0.5), (0.15, 0.35), "treeling", {"wood": 2, "sapling": 1}, "dirt"),
    ((0.15, 0.5), (0.1, 0.4), "sapling", {}, "dirt"),
    ((-0.03, -0.02), (0.27, 0.28), "rabbit hole", {"rabbit adult": 2, "rabbit child": 2}, "dirt"),
    ((-0.05, 0), (0.25, 0.3), "carrot", {}, "dirt"),
    ((-0.25, -0.15), (0.2, 0.3), "clay", {}, None),
    ((0.05, 0.1), (0.35, 0.4), "bluebell", {}, "dirt"),
)
ATTRIBUTE_CARE = ("unbreak", "point", "structure")