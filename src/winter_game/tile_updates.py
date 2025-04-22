import random

from .tile_class import Tile


def update_tiles(chunks, tile_location, room_location):
    delete_tiles = []
    create_tiles = []
    for chunk_x in range(-3, 4):
        for chunk_y in range(-3, 4):
            chunk = (chunk_x + tile_location[0], chunk_y + tile_location[1])
            if chunk in chunks[room_location]:
                for tile in chunks[room_location][chunk]:
                    current_tile = chunks[room_location][chunk][tile]
                    if "grow" in current_tile.attributes:
                        chunks[room_location][chunk][tile] = current_tile.grow()
                    elif current_tile.kind == "left":
                        if ((tile[0] - 1) % 16, tile[1]) not in chunks[room_location][
                            (chunk[0] + (tile[0] - 1) // 16, chunk[1])
                        ]:
                            delete_tiles.append((chunk, tile))
                    elif current_tile.kind == "up":
                        if ((tile[0], (tile[1] - 1) % 16)) not in chunks[room_location][
                            (chunk[0], chunk[1] + (tile[1] - 1) // 16)
                        ]:
                            delete_tiles.append((chunk, tile))
                    elif current_tile.kind == "rabbit hole":
                        if random.randint(0, 10000) == 0:
                            animal = random.choice(
                                (
                                    Tile(
                                        "rabbit adult",
                                        10,
                                        1,
                                        {"rabbit meat": 2, "rabbit fur": 1},
                                    ),
                                    Tile("rabbit child", 6, 1, {}),
                                )
                            )
                            if animal.kind in current_tile.inventory:
                                x = 0
                                y = 0
                                while (
                                    (tile[0] + x) % 16,
                                    (tile[1] + y) % 16,
                                ) in chunks[room_location][
                                    (
                                        chunk[0] + (tile[0] + x) // 16,
                                        chunk[1] + (tile[1] + y) // 16,
                                    )
                                ]:
                                    x = random.randint(-1, 1)
                                    y = random.randint(-1, 1)
                                current_tile.inventory[animal.kind] -= 1
                                if current_tile.inventory[animal.kind] <= 0:
                                    del current_tile.inventory[animal.kind]
                                create_tiles.append(
                                    (
                                        (
                                            chunk[0] + (tile[0] + x) // 16,
                                            chunk[1] + (tile[1] + y) // 16,
                                        ),
                                        ((tile[0] + x) % 16, (tile[1] + y) % 16),
                                        animal,
                                    )
                                )
    for index in range(0, len(create_tiles)):
        chunks[room_location][create_tiles[index][0]][create_tiles[index][1]] = (
            create_tiles[index][2]
        )
    for index in range(0, len(delete_tiles)):
        del chunks[room_location][delete_tiles[index][0]][delete_tiles[index][1]]
    return chunks
