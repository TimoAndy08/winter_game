from noise import pnoise2
from random import uniform

from .tile_class import Tile
from .tile_info import MULTI_TILES

def generate_chunk(
    chunk_x: int,
    chunk_y: int,
    chunks: dict[tuple[int, int], dict[tuple[int, int], Tile]],
    noise_offset: tuple[float, float] = None
):
    if noise_offset == None:
        noise_offset = (uniform(-10000, 10000), uniform(-10000, 10000))
    if (chunk_x, chunk_y) not in chunks:
        chunks[(chunk_x, chunk_y)] = {}
        for tile_x in range(0, 16):
            for tile_y in range(0, 16):
                tile = chunks[(chunk_x, chunk_y)]
                tile_pos = (tile_x, tile_y)
                if tile_pos not in tile:
                    world_x = chunk_x * 16 + tile_x
                    world_y = chunk_y * 16 + tile_y
                    elevation_value = pnoise2(
                        (world_x + noise_offset[0]) * 0.1,
                        (world_y + noise_offset[1]) * 0.1,
                        3,
                        0.5,
                        2,
                    )
                    moisture_value = pnoise2(
                        (world_x + noise_offset[0]) * 0.03,
                        (world_y + noise_offset[1]) * 0.03,
                        3,
                        0.5,
                        3,
                    )
                    if moisture_value > 0 and -0.25 > elevation_value:
                        tile[tile_pos] = Tile("ice")
                    elif moisture_value > -0.15 and -0.2 > elevation_value:
                        tile[tile_pos] = Tile("flint", {"flint": 1})
                    elif 0.1 > elevation_value > -0.1 and -0.40 > moisture_value and tile_x < 15 and tile_y < 15:
                        tile[tile_pos] = Tile("big rock", {"rock": 6})
                    elif 0.1 > elevation_value > -0.2 and -0.35 > moisture_value:
                        tile[tile_pos] = Tile("rock")
                    elif 0.03 > elevation_value > -0.03 and moisture_value > 0.47:
                        tile[tile_pos] = Tile("mushroom hut")
                    elif 0.1 > elevation_value > -0.1 and moisture_value > 0.45:
                        tile[tile_pos] = Tile("mushroom", {"spore": 2})
                    elif 0.15 > elevation_value > -0.15 and moisture_value > 0.4:
                        tile[tile_pos] = Tile("spore")
                    elif elevation_value > 0.3 and 0.3 > moisture_value > 0.2:
                        tile[tile_pos] = Tile("tree", {"wood": 4, "sapling": 2})
                    elif elevation_value > 0.25 and 0.35 > moisture_value > 0.15:
                        tile[tile_pos] = Tile("treeling", {"wood": 2, "sapling": 1})
                    elif elevation_value > 0.15 and 0.4 > moisture_value > 0.1:
                        tile[tile_pos] = Tile("sapling")
                    elif -0.02 > elevation_value > -0.03 and 0.28 > moisture_value > 0.27:
                        tile[tile_pos] = Tile("rabbit hole", {"rabbit adult": 2, "rabbit child": 2})
                    elif 0 > elevation_value > -0.05 and 0.3 > moisture_value > 0.25:
                        tile[tile_pos] = Tile("carrot")
                    elif -0.15 > elevation_value and 0.3 > moisture_value > 0.2:
                        tile[tile_pos] = Tile("clay")
                    elif 0.1 > elevation_value > 0.05 and 0.4 > moisture_value > 0.35:
                        tile[tile_pos] = Tile("bluebell")
                    if tile_pos in tile:
                        tile_size = MULTI_TILES.get(tile[tile_pos].kind, (1, 1))
                        tile_x -= tile_size[0] - 1
                        tile_y -= tile_size[1] - 1
                        can_place = True
                        for x in range(0, tile_size[0]):
                            for y in range(0, tile_size[1]):
                                if (tile_x + x, tile_y + y) in tile and "unbreak" in tile[(tile_x + x, tile_y + y)].attributes:
                                    can_place = False
                        if can_place:
                            tile[((tile_x, tile_y))] = tile[tile_pos]
                            for x in range(0, tile_size[0]):
                                if x != 0:
                                    tile[(tile_x + x, tile_y)] = Tile("left")
                                for y in range(1, tile_size[1]):
                                    tile[(tile_x + x, tile_y + y)] = Tile("up")
                        else:
                            del tile[tile_pos]
    return noise_offset