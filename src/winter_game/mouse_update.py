from .tile_rendering import SCREEN_SIZE
from .tile_info import TILE_ATTRIBUTES, RECIPES
from .ui_rendering import INVENTORY_SIZE
from .right_click_updates import right_click
from .left_click_updates import left_click

def button_press(button, position, zoom, chunks, location, machine_ui, inventory, health, max_health, machine_inventory, tick, inventory_number, recipe_number):
    if abs(position[0] - SCREEN_SIZE[0] / 2 + 32) // (64 * zoom) <= 4 and abs(position[1] - SCREEN_SIZE[1] / 2 + 32) // (64 * zoom) <= 4 or "store" in TILE_ATTRIBUTES.get(machine_ui, ()):
        world_x = location["tile"][0] * 16 + location["tile"][2] + (position[0] - SCREEN_SIZE[0] / 2 + 32) // (64 * zoom)
        world_y = location["tile"][1] * 16 + location["tile"][3] + (position[1] - SCREEN_SIZE[1] / 2 + 32) // (64 * zoom)
        grid_position = [(world_x // 16, world_y // 16), (world_x % 16, world_y % 16)]

        if grid_position[1] in chunks[location["room"]][grid_position[0]]:
            while "point" in chunks[location["room"]][grid_position[0]][grid_position[1]].attributes:
                if chunks[location["room"]][grid_position[0]][grid_position[1]].kind == "left":
                    grid_position = [(grid_position[0][0] - (grid_position[1][0] == 0), grid_position[0][1]), ((grid_position[1][0] - 1) % 16, grid_position[1][1])]
                elif chunks[location["room"]][grid_position[0]][grid_position[1]].kind == "up":
                    grid_position = [(grid_position[0][0], grid_position[0][1] - (grid_position[1][1] == 0)), (grid_position[1][0], (grid_position[1][1] - 1) % 16)]
                    
        if button == 1:
            machine_ui, chunks, location, machine_inventory, tick = left_click(machine_ui, grid_position, chunks, inventory_number, health, max_health, position, recipe_number, location, inventory, machine_inventory, tick)
        elif button == 3:
            chunks, location, machine_ui = right_click(chunks, grid_position, inventory, inventory_number, location, machine_ui)
    
    if button == 4 or button == 5:
        if "craft" in TILE_ATTRIBUTES.get(machine_ui, ()):
            recipe_number = (recipe_number + (button == 5) - (button == 4)) % len(RECIPES[machine_ui])
        else:
            inventory_number = (inventory_number + (button == 5) - (button == 4)) % INVENTORY_SIZE

    return (chunks, location, machine_ui, machine_inventory, tick, recipe_number, inventory_number)