NOISE_STRUCTURES = {
    "forest": (
        ((0, 0.05), "mushroom hut"),
    )
}
ROOM_COLORS = {
    (247, 247, 255): {"kind": "mushroom block"},
    (138, 138, 140): {"floor": "mushroom floor"},
    (53, 53, 54): {"floor": "mushroom door"},
    (106, 228, 138): {"kind": "mushroom shaper"},
}
STRUCTURE_ENTRANCE = {"copper dungeon": {"kind": "glass lock"}, "mushroom hut": {"floor": "mushroom door"}}
STRUCTURE_ROOM_SIZES = {"copper dungeon": ((1, 1), (2, 1), (2, 2)), "mushroom hut": ((1, 1),)}
STRUCTURE_SIZE = {"copper dungeon": 0.8, "mushroom hut": 0}
STRUCTURE_ROOMS = {
    "copper dungeon": {
        (1, 1): ("treasure room", "hallway"),
        (2, 1): ("library", "banquet"),
        (2, 2): ("forge",),
    },
    "mushroom hut": {
        (1, 1): ("mushroom hut",)
    },
}