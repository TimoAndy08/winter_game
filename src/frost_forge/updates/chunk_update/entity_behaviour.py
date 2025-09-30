from random import randint

from .find_empty_place import find_empty_place

def wander(chunks, chunk, tile, current_tile, create_tiles, delete_tiles):
    if randint(0, 100) == 0:
        empty = find_empty_place(tile, chunk, chunks)
        if empty:
            x, y = empty
            create_tiles.append((
                (chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16),
                ((tile[0] + x) % 16, (tile[1] + y) % 16),
                {"kind": current_tile["kind"], "inventory": current_tile["inventory"]}
            ))
            delete_tiles.append((chunk, tile))
    return create_tiles, delete_tiles