from noise import pnoise2
import random

from .tile_class import Tile
from .tile_info import MULTI_TILES

noise_offset_x = random.uniform(-10000, 10000)
noise_offset_y = random.uniform(-10000, 10000)


def generate_chunk(
    chunk_x: int,
    chunk_y: int,
    chunks: dict[tuple[int, int], dict[tuple[int, int], Tile]],
):
    if (chunk_x, chunk_y) not in chunks:
        chunks[(chunk_x, chunk_y)] = {}
        for tile_x in range(0, 16):
            for tile_y in range(0, 16):
                tile = chunks[(chunk_x, chunk_y)]
                tile_position = (tile_x, tile_y)
                if tile_position not in tile:
                    world_x = chunk_x * 16 + tile_x
                    world_y = chunk_y * 16 + tile_y
                    elevation_value = pnoise2(
                        (world_x + noise_offset_x) * 0.1,
                        (world_y + noise_offset_y) * 0.1,
                        3,
                        0.5,
                        2,
                    )
                    moisture_value = pnoise2(
                        (world_x + noise_offset_x) * 0.03,
                        (world_y + noise_offset_y) * 0.03,
                        3,
                        0.5,
                        3,
                    )
                    if moisture_value > 0 and -0.25 > elevation_value:
                        tile[tile_position] = Tile("ice", {})
                    elif moisture_value > -0.15 and -0.2 > elevation_value:
                        tile[tile_position] = Tile("flint", {"flint": 1})
                    elif 0.1 > elevation_value > -0.1 and -0.40 > moisture_value:
                        tile[tile_position] = Tile("big rock", {"rock": 6})
                    elif 0.1 > elevation_value > -0.2 and -0.35 > moisture_value:
                        tile[tile_position] = Tile("rock", {})
                    elif 0.1 > elevation_value > -0.1 and moisture_value > 0.45:
                        tile[tile_position] = Tile(
                            "mushroom",
                            {"spore": 2},
                        )
                    elif 0.15 > elevation_value > -0.15 and moisture_value > 0.4:
                        tile[tile_position] = Tile("spore", {})
                    elif elevation_value > 0.3 and 0.3 > moisture_value > 0.2:
                        tile[tile_position] = Tile(
                            "tree",
                            {"wood": 4, "sapling": 2},
                        )
                    elif elevation_value > 0.25 and 0.35 > moisture_value > 0.15:
                        tile[tile_position] = Tile(
                            "treeling", {"wood": 2, "sapling": 1}
                        )
                    elif elevation_value > 0.15 and 0.4 > moisture_value > 0.1:
                        tile[tile_position] = Tile("sapling", {})
                    elif (
                        -0.02 > elevation_value > -0.03 and 0.28 > moisture_value > 0.27
                    ):
                        tile[tile_position] = Tile(
                            "rabbit hole",
                            {"rabbit adult": 2, "rabbit child": 2},
                        )
                    elif 0 > elevation_value > -0.05 and 0.3 > moisture_value > 0.25:
                        tile[tile_position] = Tile("carrot", {})
                    elif -0.15 > elevation_value and 0.3 > moisture_value > 0.2:
                        tile[tile_position] = Tile("clay", {})
                    elif 0.1 > elevation_value > 0.05 and 0.4 > moisture_value > 0.35:
                        tile[tile_position] = Tile("bluebell", {})
                    if tile_position in tile:
                        if "multi" in tile[tile_position].attributes:
                            tile_size = MULTI_TILES[tile[tile_position].kind]
                            for x in range(0, tile_size[0]):
                                if x != 0:
                                    tile[(tile_x + x, tile_y)] = Tile("left", {})
                                for y in range(1, tile_size[1]):
                                    tile[(tile_x + x, tile_y + y)] = Tile("up", {})
