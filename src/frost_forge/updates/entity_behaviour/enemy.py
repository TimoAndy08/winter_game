from .entity_movement import move_entity


def enemy(
    chunks, chunk, tile, current_tile, location, health, player_distance
):
    if player_distance == 1:
        health -= 1
    elif player_distance < 73:
        chunks = move_entity(chunks, chunk, tile, current_tile, 1, location)
    else:
        chunks = move_entity(chunks, chunk, tile, current_tile, 0, location)
    return chunks, health
