from ..game_state import Game_State
from .menu_updates import update_menu
from .input_updates import update_game
from .tile_updates import update_tiles

def update(state: Game_State, chunks):
    if state.menu_placement != "main_game":
        chunks = update_menu(state, chunks)
    else:
        chunks = update_game(state, chunks)
        chunks[state.location["room"]] = update_tiles(state, chunks[state.location["room"]])
    return chunks