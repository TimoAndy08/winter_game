from ...info import TILE_SIZE, CHUNK_SIZE, SCREEN_SIZE
from .border_rendering import render_border


def render_floor(x, y, camera, zoom, chunks, chunk, window, scaled_image):
    tile = (x, y)
    world_x = x * TILE_SIZE + chunk[0] * CHUNK_SIZE
    world_y = y * TILE_SIZE + chunk[1] * CHUNK_SIZE
    placement = (camera[0] + world_x * zoom, camera[1] + world_y * zoom,)
    boundary = - TILE_SIZE * zoom
    if boundary <= placement[0] <= SCREEN_SIZE[0] and boundary <= placement[1] <= SCREEN_SIZE[1]:
        if tile in chunks[chunk] and "floor" in chunks[chunk][tile]:
            floor_image = scaled_image[chunks[chunk][tile]["floor"]]
            window.blit(floor_image, placement)
            render_border(
                chunk,
                x,
                y,
                chunks,
                placement,
                zoom,
                window,
                chunks[chunk][tile],
            )
