from random import randint

from .maze_solving import bfs
from ...info import FLOOR_TYPE

def wander(chunks, chunk, tile, current_tile, create_tiles, delete_tiles):
    while "goal" not in current_tile:
        goal = (randint(-8, 8), randint(-8, 8))
        current_tile["goal"] = (((current_tile[0] + goal[0]) // 16, (current_tile[1] + goal[1]) // 16), ((current_tile[0] + goal[0]) % 16, (current_tile[1] + goal[1]) % 16))
        goal_tile = chunks[current_tile["goal"][0]][current_tile["goal"][1]]
        current_tile["path"] = []
        for road in bfs((chunk[0] * 16 + tile[0], chunk[1] * 16 + tile[1]), (current_tile["goal"][0][0] * 16 + current_tile["goal"][1][0], current_tile["goal"][0][1] * 16 + current_tile["goal"][1][1]), chunks, goal_tile):
            current_tile["path"].append(((road[0] // 16, road[1] // 16), (road[0] % 16, road[1] % 16)))
        if "kind" in goal_tile or FLOOR_TYPE.get(goal_tile["floor"]) == "door" or FLOOR_TYPE.get(goal_tile["floor"]) == "fluid":
            del current_tile["goal"]
    if randint(0, 100) == 0:
        path_tile = chunks[current_tile["path"][0]][current_tile["path"][1]]
        if "kind" not in path_tile and "door" != FLOOR_TYPE.get(path_tile["floor"]) != "fluid":
            create_tiles.append((
                current_tile["path"][0][0],
                current_tile["path"][0][1],
                {"kind": current_tile["kind"], "inventory": current_tile["inventory"], "goal": current_tile["goal"], "path": current_tile["path"][1:]}
            ))
            delete_tiles.append((chunk, tile))
    return create_tiles, delete_tiles