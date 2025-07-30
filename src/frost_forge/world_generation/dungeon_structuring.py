from random import random, choice
from ..info import DUNGEON_SIZE, DUNGEON_ROOM_SIZES


ADJACENT_ROOMS = ((0, -1), (0, 1), (-1, 0), (1, 0))

def structure_dungeon(dungeon_type, dungeon=None, tile=(0, 0), distanse=1):
    if dungeon == None:
        dungeon = set()
    dungeon.add(tile)
    for pos in ADJACENT_ROOMS:
        if random() < DUNGEON_SIZE[dungeon_type]**distanse and (tile[0] + pos[0], tile[1] + pos[1]) not in dungeon:
            structure_dungeon(dungeon_type, dungeon, (tile[0] + pos[0], tile[1] + pos[1]), distanse + 1)
    return dungeon

def add_hallways(hallways, room, adj_room):
    if isinstance(room, tuple) and isinstance(adj_room, tuple):
        hallways.setdefault(room, set()).add(adj_room)
        hallways.setdefault(adj_room, set()).add(room)
    return hallways

def structure_hallways(room, dungeon, hallways=None, visited=None):
    if hallways == None:
        hallways = {}
    if visited == None:
        visited = set()
    visited.add(room)
    for pos in ADJACENT_ROOMS:
        adj_room = (room[0] + pos[0], room[1] + pos[1])
        if adj_room in dungeon:
            if random() < 0.5:
                hallways = add_hallways(hallways, room, adj_room)
                if adj_room not in visited:
                    hallways = structure_hallways((room[0] + pos[0], room[1] + pos[1]), dungeon, hallways, visited=visited)
    return hallways

def ensure_hallways(dungeon, hallways, room, visited=None):
    if visited == None:
        visited = set()
    visited.add(room)
    adj_dungeon_rooms = []
    return_rooms = []
    for pos in ADJACENT_ROOMS:
        adj_room = (room[0] + pos[0], room[1] + pos[1])
        if adj_room not in visited:
            if adj_room in hallways:
                hallways = add_hallways(hallways, room, adj_room)
                return hallways
            elif adj_room in dungeon:
                adj_dungeon_rooms.append(adj_room)
        else:
            return_rooms.append(adj_room)
    if len(adj_dungeon_rooms):
        adj_room = choice(adj_dungeon_rooms)
    else:
        adj_room = choice(return_rooms)
    hallways = add_hallways(hallways, room, choice(adj_room))
    if adj_room != (0, 0):
        hallways = ensure_hallways(dungeon, hallways, adj_room, visited)
    return hallways

def dungeon_rooms(dungeon_type):
    structure = structure_dungeon(dungeon_type)
    dungeon = {}
    if len(structure) > 1:
        hallways = structure_hallways((0, 0), structure)
        for room in structure:
            if room not in hallways:
                hallways = ensure_hallways(structure, hallways, room)
    else:
        hallways = {}
    y = 0
    while (0, y) in structure:
        y -= 1
    entrance = (0, y + 1)
    dungeon[0, y + 1] = (1, 1)
    for room in structure:
        if room not in dungeon:
            avaliable_sizes = []
            for size in DUNGEON_ROOM_SIZES[dungeon_type]:
                can_place = True
                for x in range(0, size[0]):
                    for y in range(0, size[1]):
                        if (room[0] + x, room[1] + y) in dungeon:
                            can_place = False
                if can_place:
                    avaliable_sizes.append(size)
            size = choice(avaliable_sizes)
            for x in range(0, size[0]):
                for y in range(0, size[1]):
                    dungeon[room[0] + x, room[1] + y] = (-x, -y)
            dungeon[room] = size
    return (dungeon, hallways, entrance)