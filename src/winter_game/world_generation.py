from noise import pnoise2
import random

from .tile_class import Tile

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
                world_x = chunk_x * 16 + tile_x
                world_y = chunk_y * 16 + tile_y
                elevation_value = pnoise2(
                    (world_x + noise_offset_x) * 0.1,
                    (world_y + noise_offset_y) * 0.1,
                    octaves=3,
                    persistence=0.5,
                    lacunarity=2,
                )
                moisture_value = pnoise2(
                    (world_x + noise_offset_x) * 0.03,
                    (world_y + noise_offset_y) * 0.03,
                    octaves=3,
                    persistence=0.5,
                    lacunarity=3,
                )
                tile = chunks[(chunk_x, chunk_y)]
                if moisture_value > 0 and -0.25 > elevation_value:
                    tile[(tile_x, tile_y)] = Tile("ice", 12, 1, {})
                elif moisture_value > -0.15 and -0.2 > elevation_value:
                    tile[(tile_x, tile_y)] = Tile(
                        "flint", 16, 0, {"flint": 1, "pebble": 1}
                    )
                elif 0.1 > elevation_value > -0.1 and -0.4 > moisture_value:
                    tile[(tile_x, tile_y)] = Tile(
                        "rock",
                        20,
                        1,
                        {"rock": 1, "pebble": 1},
                    )
                elif 0.1 > elevation_value > -0.2 and -0.35 > moisture_value:
                    tile[(tile_x, tile_y)] = Tile("pebble", 8, 0, {"pebble": 1})
                elif 0.1 > elevation_value > -0.1 and moisture_value > 0.45:
                    tile[(tile_x, tile_y)] = Tile(
                        "mushroom",
                        10,
                        0,
                        {"spore": 2},
                    )
                elif 0.15 > elevation_value > -0.15 and moisture_value > 0.4:
                    tile[(tile_x, tile_y)] = Tile("spore", 4, 0, {})
                elif elevation_value > 0.3 and 0.3 > moisture_value > 0.2:
                    tile[(tile_x, tile_y)] = Tile(
                        "tree",
                        15,
                        1,
                        {"wood": 4, "sapling": 2},
                    )
                elif elevation_value > 0.25 and 0.35 > moisture_value > 0.15:
                    tile[(tile_x, tile_y)] = Tile(
                        "treeling", 9, 0, {"wood": 2, "sapling": 1}
                    )
                elif elevation_value > 0.15 and 0.4 > moisture_value > 0.1:
                    tile[(tile_x, tile_y)] = Tile("sapling", 4, 0, {})
                elif -0.02 > elevation_value > -0.03 and 0.28 > moisture_value > 0.27:
                    tile[(tile_x, tile_y)] = Tile(
                        "rabbit hole",
                        1,
                        1,
                        {"rabbit adult": 2, "rabbit child": 2},
                    )
                elif 0 > elevation_value > -0.05 and 0.3 > moisture_value > 0.25:
                    tile[(tile_x, tile_y)] = Tile("carrot", 4, 0, {})
                elif -0.15 > elevation_value and 0.3 > moisture_value > 0.2:
                    tile[(tile_x, tile_y)] = Tile("clay", 12, 1, {"clay": 1})
                elif 0.1 > elevation_value > 0.05 and 0.4 > moisture_value > 0.35:
                    tile[(tile_x, tile_y)] = Tile("bluebell", 6, 1, {})
