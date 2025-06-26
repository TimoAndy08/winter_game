from noise import pnoise2
from random import uniform, random

from .tile_class import Tile
from ..info import MULTI_TILES, ROOMS, NOISE_TILES, NOISE_STRUCTURES, ATTRIBUTE_CARE, BIOMES
from .room_generation import generate_room


def generate_chunk(
    chunk_x: int,
    chunk_y: int,
    chunks: dict[tuple[int, int], dict[tuple[int, int], Tile]],
    noise_offset: tuple[float, float] = None
):
    if noise_offset == None:
        noise_offset = (uniform(-10000, 10000), uniform(-10000, 10000))
    if (chunk_x, chunk_y) not in chunks:
        chunks[chunk_x, chunk_y] = {}
        tile = chunks[chunk_x, chunk_y]
        for tile_x in range(0, 16):
            for tile_y in range(0, 16):
                tile_pos = (tile_x, tile_y)
                if tile_pos not in tile:
                    world_x = chunk_x * 16 + tile_x + noise_offset[0]
                    world_y = chunk_y * 16 + tile_y + noise_offset[1]
                    biome_value = pnoise2(world_x / 120 + noise_offset[0], world_y / 120 + noise_offset[1], 3, 0.5, 2)
                    biome = "plains"
                    for noise_chunk in BIOMES:
                        if noise_chunk[0] < biome_value < noise_chunk[1]:
                            biome = noise_chunk[2]
                            break
                    elevation_value = pnoise2(world_x / 10 + noise_offset[0], world_y / 10 + noise_offset[1], 3, 0.5, 2)
                    moisture_value = pnoise2(world_x / 30 + noise_offset[0], world_y / 30 + noise_offset[1], 3, 0.5, 2)
                    for noise_tile in NOISE_TILES[biome]:
                        if noise_tile[0][0] < elevation_value < noise_tile[0][1] and noise_tile[1][0] < moisture_value < noise_tile[1][1]:
                            tile[tile_pos] = Tile(noise_tile[2], noise_tile[3], noise_tile[4])
                            break
                    if tile_pos in tile:
                        tile_size = MULTI_TILES.get(tile[tile_pos].kind, (1, 1))
                        new_tile_x = tile_x - tile_size[0] + 1
                        new_tile_y = tile_y - tile_size[1] + 1
                        can_place = True
                        if tile_x - tile_size[0] + 1 < 0 or tile_y - tile_size[1] + 1 < 0:
                            can_place = False
                        for x in range(0, tile_size[0]):
                            for y in range(0, tile_size[1]):
                                test_tile = (new_tile_x + x, new_tile_y + y)
                                if test_tile in tile:
                                    for attribute in ATTRIBUTE_CARE:
                                        if attribute in tile[test_tile].attributes:
                                            can_place = False
                        if can_place:
                            tile[new_tile_x, new_tile_y] = tile[tile_pos]
                            for x in range(0, tile_size[0]):
                                if x != 0:
                                    tile[new_tile_x + x, new_tile_y] = Tile("left")
                                for y in range(1, tile_size[1]):
                                    tile[new_tile_x + x, new_tile_y + y] = Tile("up")
                        else:
                            del tile[tile_pos]
        structure_value = random()
        structure = False
        for noise_structure in NOISE_STRUCTURES.get(biome, ()):
            if noise_structure[0][0] < structure_value < noise_structure[0][1]:
                tile[0, 0] = Tile(noise_structure[1])
                structure = True
                break
        if structure:
            can_place = True
            tile_size = MULTI_TILES.get(tile[0, 0].kind, (1, 1))
            for x in range(0, tile_size[0]):
                for y in range(0, tile_size[1]):
                    test_tile = (x, y)
                    if test_tile in tile:
                        for attribute in ATTRIBUTE_CARE:
                            if attribute in tile[test_tile].attributes:
                                can_place = False
            if can_place:
                room_generating = ROOMS[tile[0, 0].kind]
                for room_info in room_generating:
                    room = generate_room(room_info[0], room_info[1], room_info[2], room_info[3])
                    for room_tile in room:
                        tile[room_tile] = room[room_tile]
            else:
                del tile[0, 0]
    return noise_offset