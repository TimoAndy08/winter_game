import json
from .tile_class import Tile

def serialize_chunks(chunks):
    result = {}
    for room_pos, chunk_dict in chunks.items():
        room_key = str(tuple(int(x) for x in room_pos))
        result[room_key] = {}
        for chunk_pos, tile_dict in chunk_dict.items():
            chunk_key = str(chunk_pos)
            result[room_key][chunk_key] = {}
            for tile_pos, tile in tile_dict.items():
                tile_key = str(tile_pos)
                result[room_key][chunk_key][tile_key] = tile.to_dict()
    return result

def deserialize_chunks(serialized_chunks):
    raw = json.loads(serialized_chunks)
    chunks = {}
    for room_key, chunk_dict in raw.items():
        if room_key.strip(" ()") == "":
            room_pos = ()
        else:
            room_pos = tuple(
                int(float(x)) for x in room_key.strip(" ()").split(",") if x
            )
        chunks[room_pos] = {}
        for chunk_key, tile_dict in chunk_dict.items():
            chunk_pos = tuple(
                int(float(x)) for x in chunk_key.strip(" ()").split(",") if x
            )
            chunks[room_pos][chunk_pos] = {}
            for tile_key, tile_data in tile_dict.items():
                tile_pos = tuple(
                    int(float(x)) for x in tile_key.strip(" ()").split(",") if x
                )
                chunks[room_pos][chunk_pos][tile_pos] = Tile.from_dict(tile_data)
    return chunks
