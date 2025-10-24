from ...info import LIGHTS


def lights(lighting, chunks, chunk, tile):
    light_strength = LIGHTS[chunks[chunk][tile]["kind"]]
    for dx in range(-light_strength, light_strength):
        for dy in range(-light_strength, light_strength):
            current_strength = light_strength - abs(dx) - abs(dy)
            if current_strength > 0:
                light_chunk = (chunk[0] + (tile[0] + dx) // 16, chunk[1] + (tile[1] + dy))
                light_tile = ((tile[0] + dx) % 16, (tile[1] + dy) % 16)
                if light_chunk not in lighting:
                    lighting[light_chunk] = {}
                if light_tile in lighting[light_chunk]:
                    lighting[light_chunk][light_tile] = max(lighting[light_chunk][light_tile], current_strength)
                else:
                    lighting[light_chunk][light_tile] = current_strength
    return lighting
