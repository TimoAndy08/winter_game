from collections import deque
from ...info import FLOOR_TYPE


def bfs(start, goal, chunks):
    blocked = set()
    for chunk in chunks:
        for tile in chunks[chunk]:
            current_tile = chunks[chunk][tile]
            if ("kind" in current_tile and current_tile["kind"] != "player") or (
                "floor" in current_tile
                and (
                    FLOOR_TYPE.get(current_tile["floor"]) == "door"
                    or FLOOR_TYPE.get(current_tile["floor"]) == "fluid"
                )
            ):
                blocked.add((chunk[0] * 16 + tile[0], chunk[1] * 16 + tile[1]))

    queue = deque([start])
    visited = {start: None}
    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))

    while queue:
        current = queue.popleft()
        if current == goal:
            break
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if (
                start[0] - 8 <= neighbor[0] < start[0] + 8
                and start[1] - 8 <= neighbor[1] < start[1] + 8
                and neighbor not in blocked
                and neighbor not in visited
            ):
                queue.append(neighbor)
                visited[neighbor] = current

    path = []
    if goal in visited:
        cur = goal
        while cur != start:
            path.append(cur)
            cur = visited[cur]
        path.reverse()
    return path
