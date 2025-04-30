from .tile_class import Tile


def generate_room(material: str, location: tuple[int, int], size: tuple[int, int]):
    room = {}
    for x in range(location[0], location[0] + size[0]):
        for y in range(location[1], location[1] + size[1]):
            if (
                x == location[0]
                or y == location[1]
                or x == location[0] + size[0] - 1
                or y == location[1] + size[1] - 1
            ):
                if (x // 16, y // 16) not in room:
                    room[x // 16, y // 16] = {}
                room[(x // 16, y // 16)][(x % 16, y % 16)] = Tile(material)
                room[(x // 16, y // 16)][(x % 16, y % 16)].attributes = ("unbreak",)
    return room
