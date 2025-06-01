from .tile_class import Tile


def generate_room(material: str, location: tuple[int, int], size: tuple[int, int], floor: str = None):
    room = {}
    for x in range(location[0], location[0] + size[0]):
        for y in range(location[1], location[1] + size[1]):
            if (x // 16, y // 16) not in room:
                room[x // 16, y // 16] = {}
            room[x // 16, y // 16][x % 16, y % 16] = Tile(material, floor = floor, floor_unbreak = True, unbreak = True)
            room[x // 16, y // 16][x % 16, y % 16].attributes = (*room[x // 16, y // 16][x % 16, y % 16].attributes, "unbreak")
    for x in range(location[0] + 1, location[0] + size[0] - 1):
        for y in range(location[1] + 1, location[1] + size[1] - 1):
            room[x // 16, y // 16][x % 16, y % 16] = Tile(floor = floor, floor_unbreak = True, unbreak = True)
    return room