from random import randint

from .maze_solving import bfs
from ...info import FLOOR_TYPE


def move_entity(
    chunks, chunk, tile, current_tile, create_tiles, delete_tiles, type, location
):
    obscured_path = False
    if "goal" not in current_tile:
        if type == 0:
            goal = (randint(-8, 8), randint(-8, 8))
            current_tile["goal"] = (
                (
                    chunk[0] + int((tile[0] + goal[0]) / 16),
                    chunk[1] + int((tile[1] + goal[1]) / 16),
                ),
                ((tile[0] + goal[0]) % 16, (tile[1] + goal[1]) % 16),
            )
        elif type == 1:
            current_tile["goal"] = (
                (location["tile"][0], location["tile"][1]),
                (location["tile"][2], location["tile"][3]),
            )
        current_tile["path"] = []
        start = (chunk[0] * 16 + tile[0], chunk[1] * 16 + tile[1])
        goal = (
            current_tile["goal"][0][0] * 16 + current_tile["goal"][1][0],
            current_tile["goal"][0][1] * 16 + current_tile["goal"][1][1],
        )
        path = bfs(start, goal, chunks)
        for road in path:
            current_tile["path"].append(
                ((road[0] // 16, road[1] // 16), (road[0] % 16, road[1] % 16))
            )
    if len(current_tile["path"]) > 0:
        path_tile = chunks[current_tile["path"][0][0]].get(
            current_tile["path"][0][1], {}
        )
        if "kind" not in path_tile and (
            "floor" not in path_tile
            or "door" != FLOOR_TYPE.get(path_tile["floor"]) != "fluid"
        ):
            path_location = current_tile["path"][0]
            current_tile["path"].pop(0)
            create_tiles.append((path_location[0], path_location[1], current_tile))
            delete_tiles.append((chunk, tile))
        else:
            obscured_path = True
    if len(current_tile["path"]) == 0 or obscured_path:
        del current_tile["path"]
        del current_tile["goal"]
    return create_tiles, delete_tiles
