# fmt off
import pygame as pg
import random
import os
import math
import ast
import json

from .crafting_system import recipe
from .world_generation import generate_chunk
from .tile_class import Tile
from .tile_class import tile_attributes
from .room_generation import generate_room
from .light import lights
from .serialize import serialize_chunks
from .serialize import deserialize_chunks
from .options import options

pg.init()
SCREEN_SIZE = (pg.display.Info().current_w + 64, pg.display.Info().current_h + 40)
DAY_LENGTH = 86400  # 24 minutes
UI_SCALE = 2
INVENTORY_SIZE = 12

def font(size):
    return pg.font.SysFont("Lucida Console", size)

def main() -> int:
    window = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()
    run = True
    zoom = 1
    recipes = {
        "player": [
            (("workbench", 1), [("wood", 4), ("flint", 2)]),
            (("stick", 4), [("wood", 2)]),
        ],
        "workbench": [
            (("flint axe", 1), [("stick", 3), ("flint", 4)]),
            (("flint pickaxe", 1), [("stick", 3), ("flint", 4), ("pebble", 1)]),
            (("flint shovel", 1), [("stick", 2), ("flint", 3)]),
            (("flint sword", 1), [("stick", 2), ("flint", 4), ("ice", 1)]),
            (("campfire", 1), [("wood", 5), ("flint", 2), ("stick", 6), ("pebble", 1)]),
            (("bowl", 4), [("wood", 3), ("stick", 2)]),
            (("wood pulp", 2), [("wood", 3), ("water", 2)]),
            (("flint hammer", 1), [("stick", 4), ("rock", 2), ("flint", 3)]),
            (("manual press", 1), [("workbench", 1), ("flint hammer", 1)]),
            (("sawbench", 1), [("workbench", 1), ("flint axe", 2)]),
        ],
        "campfire": [
            (("roasted mushroom", 1), [("mushroom", 1), ("stick", 1)]),
            (("water", 2), [("ice", 1), ("bowl", 2)]),
            (("mushroom stew", 2), [("mushroom", 3), ("carrot", 1), ("water", 2)]),
            (("stone", 1), [("rock", 1)]),
            (("brick", 1), [("clay", 1)]),
            (("roasted rabbit meat", 1), [("rabbit meat", 1)])
        ],
        "manual press": [
            (("blue dye", 2), [("bluebell", 2), ("water", 1), ("bowl", 1)]),
            (("paper", 2), [("wood pulp", 3)]),
            (("blueprint", 1), [("paper", 3), ("blue dye", 2)]),
        ],
        "sawbench": [
            (("stick", 7), [("wood", 3)]),
            (("small crate", 1), [("wood", 6), ("stick", 4)]),
            (("small barrel", 1), [("wood", 6), ("stick", 4)]),
            (("stone brick", 2), [("stone", 3)]),
            (("wooden cabin", 1), [("wood", 16), ("brick", 6)]),
            (("wooden bed", 1), [("wood", 10), ("blue dye", 3), ("rabbit fur", 2)]),
        ],
    }
    tool_required = {
        "player": "sword",
        "sapling": "shovel",
        "treeling": "axe",
        "tree": "axe",
        "wood": "axe",
        "spore": "shovel",
        "mushroom": "axe",
        "pebble": "pickaxe",
        "flint": "pickaxe",
        "ice": "pickaxe",
        "stick": "axe",
        "campfire": "axe",
        "carroot": "shovel",
        "carrot": "shovel",
        "rock": "pickaxe",
        "clay": "shovel",
        "stone": "pickaxe",
        "stone brick": "pickaxe",
        "brick": "pickaxe",
        "rabbit adult": "sword",
        "sawbench": "axe",
        "wood pulp": "shovel",
        "manual press": "pickaxe",
        "bluebell": "shovel",
        "small crate": "axe",
        "wooden cabin": "axe"
    }
    tool_efficiency = {"flint": 1}
    multi_tiles = {"sawbench": (2, 1), "manual press": (2, 1), "wooden cabin": (4, 3), "wooden bed": (1, 2)}
    storage = {"small crate": (9, 48), "small barrel": (1, 512)}
    food = {"mushroom": 1, "carrot": 2, "roasted mushroom": 3, "mushroom stew": 6, "rabbit meat": 1, "roasted rabbit meat": 4}
    inventory_number = 0
    recipe_number = 0
    save_file = ""
    option_placement = "main_menu"
    last_mined_location = [0, 0, 0, 0]
    images = {}
    sprites_folder = "src/sprites"
    controls = [119, 97, 115, 100, 101, 122, 120]
    control_names = ["Move up ", "Move left ", "Move down ", "Move right", "Inventory ", "Zoom in", "Zoom out"]
    velocity = [0, 0]
    machine_ui = "game"
    for filename in os.listdir(sprites_folder):
        images[filename.split(".")[0]] = pg.image.load(os.path.join(sprites_folder, filename)).convert_alpha()

    while run:
        window.fill((206, 229, 242))
        if option_placement != "main_game":
            for event in pg.event.get():
                position = pg.mouse.get_pos()[1]
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    option = options(position, option_placement, save_file, event)
                    if isinstance(option[1], str):
                        option_placement = option[1]
                    else:
                        control_adjusted = (control_adjusted + option[1]) % len(controls)
                    if option[0] == "create":
                        option_placement = "main_game"
                        chunks = {(): {}}
                        tile_location = [0, 0, 0, 0]
                        real_location = [0, 0, 0, 0]
                        room_location = ()
                        generate_chunk(0, 0, chunks[room_location])
                        chunks[room_location][(0, 0)] = {(0, 0): Tile("player", 20, 0, {})}
                        tick = 0
                    elif option[0] == "load":
                        option_placement = "main_game"
                        with open(f"src/saves/{save_file}.txt", "r", encoding="utf-8") as file:
                            file_content = file.read().split(";")
                        chunks = deserialize_chunks(file_content[0])
                        tile_location = ast.literal_eval(file_content[1])
                        tick = int(file_content[2])
                        room_location = ast.literal_eval(file_content[3])
                        real_location = [*tile_location,]
                    elif option[0] == "save":
                        option_placement = "main_menu"
                        with open(f"src/saves/{save_file}.txt", "w", encoding="utf-8") as file:
                            chunks_json = json.dumps(serialize_chunks(chunks))
                            file.write(f"{chunks_json};{tile_location};{tick};{room_location}")
                        save_file = ""
                    elif option[0] == "control":
                        control_adjusted = 0
                    elif option[0] == "exit":
                        run = False
                elif event.type == pg.KEYDOWN:
                    key = pg.key.get_pressed()
                    if option_placement.split("_")[0] == "save":
                        for letters in range(48, 123):
                            if key[letters]:
                                save_file += chr(letters)
                        if key[pg.K_SPACE]:
                            save_file += " "
                        elif key[pg.K_BACKSPACE]:
                            save_file = save_file[:-1]
                    elif option_placement == "controls_options":
                        for keys in range(0, len(key)):
                            if key[keys]:
                                controls[control_adjusted] = keys

            if option_placement == "load_save":
                window.blit(font(50).render("Load save?", False, (19, 17, 18)), (0, 0))
                window.blit(font(50).render("Yes", False, (19, 17, 18)), (0, 100))
                window.blit(font(50).render("No", False, (19, 17, 18)), (0, 200))
            elif option_placement.split("_")[0] == "save":
                if option_placement == "save_creation":
                    window.blit(font(50).render("Name your new save?", False, (19, 17, 18)), (0, 0))
                if option_placement == "save_selection":
                    window.blit(font(50).render("Which save to load?", False, (19, 17, 18)), (0, 0))
                window.blit(font(50).render(save_file, False, (19, 17, 18)), (0, 100))
                window.blit(font(50).render("Proceed", False, (19, 17, 18)), (0, 200))
            elif option_placement.split("_")[0] == "options":
                if option_placement == "options_game":
                    window.blit(font(50).render("Return to game", False, (19, 17, 18)), (0, 0))
                    window.blit(font(50).render("Save and Quit", False, (19, 17, 18)), (0, 100))
                elif option_placement == "options_main":
                    window.blit(font(50).render("Back to menu", False, (19, 17, 18)), (0, 0))
                window.blit(font(50).render("Controls options", False, (19, 17, 18)), (0, 200))
            elif option_placement == "main_menu":
                window.blit(font(50).render("Play", False, (19, 17, 18)), (0, 0))
                window.blit(font(50).render("Options", False, (19, 17, 18)), (0, 100))
                window.blit(font(50).render("Quit Game", False, (19, 17, 18)), (0, 200))
            elif option_placement == "controls_options":
                window.blit(font(50).render("Proceed", False, (19, 17, 18)), (0, 0))
                window.blit(font(50).render(f"{control_names[control_adjusted]}: {chr(controls[control_adjusted])}", False, (19, 17, 18)), (0, 100))
        else:
            old_location = [*tile_location,]
            inventory = chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory
            key = pg.key.get_pressed()
            if key[controls[0]]:
                velocity[1] -= 0.3 / (1 + abs(velocity[1]))
            if key[controls[1]]:
                velocity[0] -= 0.3 / (1 + abs(velocity[1]))
            if key[controls[2]]:
                velocity[1] += 0.3 / (1 + abs(velocity[1]))
            if key[controls[3]]:
                velocity[0] += 0.3 / (1 + abs(velocity[1]))
            real_location[2] += velocity[0] / 2
            real_location[3] += velocity[1] / 2
            velocity[0] *= 0.65
            velocity[1] *= 0.65
            real_location = [real_location[0] + real_location[2] // 16, real_location[1] + real_location[3] // 16, real_location[2] % 16, real_location[3] % 16,]
            tile_location = [int(real_location[0]), int(real_location[1]), int(real_location[2]), int(real_location[3]),]

            if room_location == ():
                for x in range(-4, 5):
                    for y in range(-4, 5):
                        generate_chunk(tile_location[0] + x, tile_location[1] + y, chunks[room_location])
            if not (tile_location[2], tile_location[3]) in chunks[room_location][(tile_location[0], tile_location[1])]:
                chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])] = chunks[room_location][(old_location[0], old_location[1])][(old_location[2], old_location[3])]
                del chunks[room_location][old_location[0], old_location[1]][old_location[2], old_location[3]]
            else:
                if chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].kind != "player":
                    real_location = [*old_location,]
                tile_location = [*old_location,]
                velocity = [0, 0]

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    position = [*pg.mouse.get_pos(),]
                    if abs(position[0] - SCREEN_SIZE[0] / 2 + 32) // (64 * zoom) <= 4 and abs(position[1] - SCREEN_SIZE[1] / 2 + 32) // (64 * zoom) <= 4 or "store" in tile_attributes.get(machine_ui, ()):
                        world_x = tile_location[0] * 16 + tile_location[2] + (position[0] - SCREEN_SIZE[0] / 2 + 32) // (64 * zoom)
                        world_y = tile_location[1] * 16 + tile_location[3] + (position[1] - SCREEN_SIZE[1] / 2 + 32) // (64 * zoom)
                        grid_position = [(world_x // 16, world_y // 16), (world_x % 16, world_y % 16)]
                        if grid_position[1] in chunks[room_location][grid_position[0]]:
                            while "point" in chunks[room_location][grid_position[0]][grid_position[1]].attributes:
                                if chunks[room_location][grid_position[0]][grid_position[1]].kind == "left":
                                    grid_position = [(grid_position[0][0] - (grid_position[1][0] == 0), grid_position[0][1]), ((grid_position[1][0] - 1) % 16, grid_position[1][1])]
                                elif chunks[room_location][grid_position[0]][grid_position[1]].kind == "up":
                                    grid_position = [(grid_position[0][0], grid_position[0][1] - (grid_position[1][1] == 0)), (grid_position[1][0], (grid_position[1][1] - 1) % 16)]
                        if event.button == 1:
                            if machine_ui == "game":
                                if grid_position[1] not in chunks[room_location][grid_position[0]]:
                                    if len(inventory) > inventory_number:
                                        can_place = True
                                        inventory_key = list(inventory.keys())[inventory_number]
                                        if "eat" in tile_attributes.get(inventory_key, ()):
                                            if health < max_health:
                                                chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].health = min(health + food[inventory_key], max_health)
                                                can_place = False
                                                inventory[inventory_key] -= 1
                                                if inventory[inventory_key] == 0:
                                                    del inventory[inventory_key]
                                        if "multi" in tile_attributes.get(inventory_key, ()):
                                            for x in range(0, multi_tiles[inventory_key][0]):
                                                for y in range(0, multi_tiles[inventory_key][1]):
                                                    if ((grid_position[1][0] + x) % 16, (grid_position[1][1] + y) % 16) in chunks[room_location][(grid_position[0][0] + (grid_position[1][0] + x) // 16, grid_position[0][1] + (grid_position[1][1] + y) // 16)]:
                                                        can_place = False
                                        if can_place:
                                            inventory[inventory_key] -= 1
                                            if "multi" in tile_attributes.get(inventory_key, ()):
                                                for x in range(0, multi_tiles[inventory_key][0]):
                                                    chunks[room_location][(grid_position[0][0] + (grid_position[1][0] + x) // 16, grid_position[0][1])][((grid_position[1][0] + x) % 16, grid_position[1][1])] = Tile("left", 1, 1, {})
                                                    for y in range(1, multi_tiles[inventory_key][1]):
                                                        chunks[room_location][(grid_position[0][0] + (grid_position[1][0] + x) // 16, grid_position[0][1] + (grid_position[1][1] + y) // 16)][((grid_position[1][0] + x) % 16, (grid_position[1][1] + y) % 16)] = Tile("up", 1, 1, {})
                                            chunks[room_location][grid_position[0]][grid_position[1]] = Tile(inventory_key, 4, 0, {})
                                            if inventory[inventory_key] == 0:
                                                del inventory[inventory_key]
                                elif "open" in chunks[room_location][grid_position[0]][grid_position[1]].attributes:
                                    machine_ui = chunks[room_location][grid_position[0]][grid_position[1]].kind
                                    last_opened_location = (grid_position[0], grid_position[1])
                                elif "enter" in chunks[room_location][grid_position[0]][grid_position[1]].attributes and room_location == ():
                                    room_location = (*grid_position[0], *grid_position[1],)
                                    real_location = [0, 0, 0, 0]
                                    last_mined_location = [0, 0, 0, 0]
                                    if room_location in chunks:
                                        chunks[room_location][(0, 0)][(0, 0)] = chunks[()][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                                        del chunks[()][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                                        tile_location = [0, 0, 0, 0]
                                    else:
                                        if chunks[()][grid_position[0]][grid_position[1]].kind == "wooden cabin":
                                            chunks[room_location] = generate_room("wood", (-5, -4), (8, 6))
                                            chunks[room_location][(0, 0)][(0, 1)] = Tile("wooden door", 1, 1, {})
                                            chunks[room_location][(0, 0)][(0, 0)] = chunks[()][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                                            del chunks[()][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                                            tile_location = [0, 0, 0, 0]
                                elif "exit" in chunks[room_location][grid_position[0]][grid_position[1]].attributes:
                                    chunks[()][(room_location[0] + (room_location[2] - 1) // 16, room_location[1])][((room_location[2] - 1) % 16, room_location[3])] = chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                                    del chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])]
                                    i = -1
                                    real_location = [room_location[0] + (room_location[2] + i) // 16, room_location[1], (room_location[2] + i) % 16, room_location[3]]
                                    tile_location = [*real_location,]
                                    last_mined_location = [*real_location,]
                                    room_location = ()
                                    machine_ui = "game"
                                elif "sleep" in chunks[room_location][grid_position[0]][grid_position[1]].attributes:
                                    if 48600 <= tick % 86400 < 81000:
                                        tick = 80999 + (tick // 86400) * 86400
                            elif "store" in tile_attributes.get(machine_ui, ()):
                                position[0] -= SCREEN_SIZE[0] // 2
                                if position[1] >= SCREEN_SIZE[1] - 32 * UI_SCALE and abs(position[0]) <= 16 * INVENTORY_SIZE * UI_SCALE:
                                    slot_number = (position[0] - 16 * UI_SCALE * (INVENTORY_SIZE % 2)) // (32 * UI_SCALE) + INVENTORY_SIZE // 2 + INVENTORY_SIZE % 2
                                    if slot_number < len(inventory):
                                        item = list(inventory.items())[slot_number]
                                        machine_item = machine_inventory.get(item[0], 0)
                                        if not (machine_item == 0 and len(machine_inventory) == storage[machine_ui][0]):
                                            if machine_item + item[1] <= storage[machine_ui][1]:
                                                chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory[item[0]] = machine_item + item[1]
                                                del chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item[0]]
                                            else:
                                                chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory[item[0]] = storage[machine_ui][1]
                                                chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item[0]] = machine_item + item[1] - storage[machine_ui][1]
                                elif SCREEN_SIZE[1] - 144 * UI_SCALE <= position[1] <= SCREEN_SIZE[1] - 80 * UI_SCALE and abs(position[0]) <= 112 * UI_SCALE:
                                    slot_number = (position[0] + 112 * UI_SCALE) // (32 * UI_SCALE) + (position[1] - SCREEN_SIZE[1] + 144 * UI_SCALE) // (32 * UI_SCALE) * 7
                                    if slot_number < len(machine_inventory):
                                        item = list(machine_inventory.items())[slot_number]
                                        inventory_item = inventory.get(item[0], 0)
                                        if not (inventory_item == 0 and len(inventory) == INVENTORY_SIZE):
                                            if inventory_item + item[1] <= 64:
                                                chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item[0]] = inventory_item + item[1]
                                                del chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory[item[0]]
                                            else:
                                                chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item[0]] = 64
                                                chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory[item[0]] = inventory_item + item[1] - 64
                            elif "craft" in tile_attributes.get(machine_ui, ()):
                                inventory = recipe(recipes[machine_ui][recipe_number][0], recipes[machine_ui][recipe_number][1], inventory, (INVENTORY_SIZE, 64))
                        elif event.button == 3:
                            if grid_position[1] in chunks[room_location][grid_position[0]]:
                                damage = 1 - chunks[room_location][grid_position[0]][grid_position[1]].resistance
                                if len(inventory) > inventory_number:
                                    inventory_key = list(inventory.keys())[inventory_number]
                                    inventory_words = inventory_key.split()
                                    if len(inventory_words) == 2 and chunks[room_location][grid_position[0]][grid_position[1]].kind in tool_required:
                                        if tool_required[chunks[room_location][grid_position[0]][grid_position[1]].kind] == inventory_words[1]:
                                            damage += tool_efficiency[inventory_words[0]]
                                chunks[room_location][grid_position[0]][grid_position[1]].health -= max(damage, 0)
                                last_mined_location = [grid_position[0][0], grid_position[0][1], grid_position[1][0], grid_position[1][1]]
                                if chunks[room_location][grid_position[0]][grid_position[1]].health <= 0:
                                    if chunks[room_location][grid_position[0]][grid_position[1]].kind != "player":
                                        junk_inventory = {}
                                        if not "no_pickup" in chunks[room_location][grid_position[0]][grid_position[1]].attributes:
                                            chunks[room_location][grid_position[0]][grid_position[1]].inventory[chunks[room_location][grid_position[0]][grid_position[1]].kind] = chunks[room_location][grid_position[0]][grid_position[1]].inventory.get(chunks[room_location][grid_position[0]][grid_position[1]].kind, 0) + 1
                                        for item, amount in chunks[room_location][grid_position[0]][grid_position[1]].inventory.items():
                                            if item in chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory:
                                                chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item] += amount
                                                if inventory[item] > 64:
                                                    junk_inventory[item] = chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item] - 64
                                                    chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item] = 64
                                            else:
                                                if len(inventory) < INVENTORY_SIZE:
                                                    chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].inventory[item] = amount
                                                else:
                                                    junk_inventory[item] = amount
                                        if "enter" in chunks[room_location][grid_position[0]][grid_position[1]].attributes and (*grid_position[0], *grid_position[1]) in chunks:
                                            del chunks[(*grid_position[0], *grid_position[1])]
                                        del chunks[room_location][grid_position[0]][grid_position[1]]
                                        if len(junk_inventory) > 0:
                                            chunks[room_location][grid_position[0]][grid_position[1]] = Tile("junk", 1, 0, junk_inventory)
                                        machine_ui = "game"
                                    else:
                                        chunks[room_location][grid_position[0]][grid_position[1]] = Tile("corpse", 1, 0, inventory)
                                        i = 0
                                        while (i % 16, i // 16) in chunks[()][(0, 0)]:
                                            i += 1
                                            if x == 256:
                                                i = 0
                                                break
                                        chunks[()][(0, 0)][(i % 16, i // 16)] = Tile("player", max_health, 0, {})
                                        tile_location = [0, 0, i % 16, i // 16]
                                        real_location = [0, 0, i % 16, i // 16]
                                        room_location = ()
                    if event.button >= 6:
                        if "craft" in tile_attributes.get(machine_ui, ()):
                            recipe_number = (recipe_number + (event.button == 6) - (event.button == 7)) % len(recipes[machine_ui])
                        else:
                            inventory_number = (inventory_number + (event.button == 6) - (event.button == 7)) % INVENTORY_SIZE
                elif event.type == pg.KEYDOWN:
                    key = pg.key.get_pressed()
                    if key[controls[4]]:
                        if machine_ui == "game": 
                            machine_ui = "player"
                        else: 
                            machine_ui = "game"
                            recipe_number = 0
                    elif key[controls[5]] or key[controls[6]]:
                        zoom += (key[controls[5]] - key[controls[6]]) / 4
                        zoom = min(max(zoom, 0.5), 2)
                    elif key[pg.K_TAB]:
                        option_placement = "options_game"

            delete_tiles = []
            create_tiles = []
            for chunk_x in range(-3, 4):
                for chunk_y in range(-3, 4):
                    chunk = (chunk_x + tile_location[0], chunk_y + tile_location[1])
                    if chunk in chunks[room_location]:
                        for tile in chunks[room_location][chunk]:
                            current_tile = chunks[room_location][chunk][tile]
                            if "grow" in current_tile.attributes:
                                chunks[room_location][chunk][tile] = current_tile.grow()
                            elif current_tile.kind == "left":
                                if ((tile[0] - 1) % 16, tile[1]) not in chunks[room_location][(chunk[0] + (tile[0] - 1) // 16, chunk[1])]:
                                    delete_tiles.append((chunk, tile))
                            elif current_tile.kind == "up":
                                if ((tile[0], (tile[1] - 1) % 16)) not in chunks[room_location][(chunk[0], chunk[1] + (tile[1] - 1) // 16)]:
                                    delete_tiles.append((chunk, tile))
                            elif current_tile.kind == "rabbit hole":
                                if random.randint(0, 10000) == 0:
                                    animal = random.choice((Tile("rabbit adult", 10, 1, {"rabbit meat": 2, "rabbit fur": 1}), Tile("rabbit child", 6, 1, {})))
                                    if animal.kind in current_tile.inventory:
                                        x = 0
                                        y = 0
                                        while ((tile[0] + x) % 16, (tile[1] + y) % 16) in chunks[room_location][(chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16)]:
                                            x = random.randint(-1, 1)
                                            y = random.randint(-1, 1)
                                        current_tile.inventory[animal.kind] -= 1
                                        if current_tile.inventory[animal.kind] <= 0:
                                            del current_tile.inventory[animal.kind]
                                        create_tiles.append(((chunk[0] + (tile[0] + x) // 16, chunk[1] + (tile[1] + y) // 16), ((tile[0] + x) % 16, (tile[1] + y) % 16), animal))
            for index in range(0, len(create_tiles)):
                chunks[room_location][create_tiles[index][0]][create_tiles[index][1]] = create_tiles[index][2]
            for index in range(0, len(delete_tiles)):
                del chunks[room_location][delete_tiles[index][0]][delete_tiles[index][1]]

            camera = [SCREEN_SIZE[0] / 2 - ((tile_location[2] * 64 + tile_location[0] * 1024 + 32) * zoom), SCREEN_SIZE[1] / 2 - ((tile_location[3] * 64 + tile_location[1] * 1024 + 32) * zoom)]
            for chunk_x in range(-3, 4):
                for chunk_y in range(-3, 4):
                    chunk = (chunk_x + tile_location[0], chunk_y + tile_location[1])
                    if chunk in chunks[room_location]:
                        for y in range(0, 16):
                            for x in range(0, 16):
                                tile = (x, y)
                                if tile in chunks[room_location][chunk] and "point" not in chunks[room_location][chunk][tile].attributes:
                                    placement = camera[0] + (x * 64 + chunk[0] * 1024) * zoom, camera[1] + (y * 64 + chunk[1] * 1024 - 32) * zoom
                                    size = multi_tiles.get(chunks[room_location][chunk][tile].kind, (1, 1))
                                    if -64 * zoom * size[0] <= placement[0] <= SCREEN_SIZE[0] and -64 * zoom * size[1] <= placement[1] <= SCREEN_SIZE[1]:
                                        window.blit(pg.transform.scale(images[chunks[room_location][chunk][tile].kind], (64 * zoom * size[0], (32 + 64 * size[1]) * zoom)), placement)

            if len(inventory) > inventory_number and machine_ui == "game":
                placement = (camera[0] + (tile_location[2] * 64 + tile_location[0] * 1024 - 4) * zoom, camera[1] + (tile_location[3] * 64 + tile_location[1] * 1024 - 8) * zoom)
                window.blit(pg.transform.scale(images[list(inventory.keys())[inventory_number]], (32 * zoom, 48 * zoom)), placement)

            dark_overlay = pg.Surface(SCREEN_SIZE)
            dark_overlay.fill((19, 17, 18))
            dark_overlay.set_alpha(int((1 - math.cos((tick - 21600) / DAY_LENGTH * 2 * math.pi)) * 95))
            window.blit(dark_overlay, (0, 0))

            for x in range(-3, 4):
                for y in range(-3, 4):
                    if chunk in chunks[room_location]:
                        chunk = (x + tile_location[0], y + tile_location[1])
                        for tile in chunks[room_location][chunk]:
                            current_tile = chunks[room_location][chunk][tile]
                            if "light" in current_tile.attributes:
                                scaled_glow = pg.transform.scale(lights[current_tile.kind][0], (int(lights[current_tile.kind][1] * zoom), int(lights[current_tile.kind][1] * zoom)))
                                night_factor = 1 - math.cos((tick - 21600) / DAY_LENGTH * 2 * math.pi)
                                scaled_glow.set_alpha(int(night_factor * 180))
                                window.blit(scaled_glow, (camera[0] + (tile[0] * 64 + chunk[0] * 1024 + 32) * zoom - int(lights[current_tile.kind][1] * zoom / 2), camera[1] + (tile[1] * 64 + chunk[1] * 1024 + 32) * zoom - int(lights[current_tile.kind][1] * zoom / 2)))

            if (last_mined_location[2], last_mined_location[3]) in chunks[room_location][(last_mined_location[0], last_mined_location[1])]:
                placement = (camera[0] + (last_mined_location[2] * 64 + last_mined_location[0] * 1024) * zoom, camera[1] + (last_mined_location[3] * 64 + last_mined_location[1] * 1024 + 60) * zoom)
                last_mined_tile = chunks[room_location][(last_mined_location[0], last_mined_location[1])][(last_mined_location[2], last_mined_location[3])]
                window.blit(pg.transform.scale(images["tiny_bar"], (64 * zoom, 16 * zoom)), placement)
                pg.draw.rect(window, (181, 102, 60), pg.Rect(placement[0] + 4 * zoom, placement[1] + 4 * zoom, last_mined_tile.health * 44 * zoom / last_mined_tile.max_health, 8 * zoom))

            health = chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].health
            max_health = chunks[room_location][(tile_location[0], tile_location[1])][(tile_location[2], tile_location[3])].max_health
            window.blit(pg.transform.scale(images["health_bar"], (128 * UI_SCALE, 32 * UI_SCALE)), (SCREEN_SIZE[0] - 128 * UI_SCALE, 0))
            window.blit(pg.transform.scale(images["health_end"], (16 * UI_SCALE, 16 * UI_SCALE)), (SCREEN_SIZE[0] + (health * 64 / max_health - 96) * UI_SCALE, 8 * UI_SCALE))
            pg.draw.rect(window, (181, 102, 60), pg.Rect(SCREEN_SIZE[0] - 96 * UI_SCALE, 8 * UI_SCALE, health * 64 * UI_SCALE / max_health, 16 * UI_SCALE))
            window.blit(font(10 * UI_SCALE).render(f"{health} / {max_health}", False, (206, 229, 242)), (SCREEN_SIZE[0] - 80 * UI_SCALE, 12 * UI_SCALE))

            for i in range(0, INVENTORY_SIZE):
                if i == inventory_number:
                    window.blit(pg.transform.scale(images["inventory_slot_2"], (32 * UI_SCALE, 32 * UI_SCALE)), (SCREEN_SIZE[0] // 2 + (32 * i - 16 * INVENTORY_SIZE) * UI_SCALE, SCREEN_SIZE[1] - 32 * UI_SCALE))
                else:
                    window.blit(pg.transform.scale(images["inventory_slot"], (32 * UI_SCALE, 32 * UI_SCALE)), (SCREEN_SIZE[0] // 2 + (32 * i - 16 * INVENTORY_SIZE) * UI_SCALE, SCREEN_SIZE[1] - 32 * UI_SCALE))
            t = 0
            for item in inventory:
                window.blit(pg.transform.scale(images[item], (16 * UI_SCALE, 24 * UI_SCALE)), (SCREEN_SIZE[0] // 2 + (32 * t - 16 * INVENTORY_SIZE + 8) * UI_SCALE, SCREEN_SIZE[1] - 28 * UI_SCALE))
                window.blit(font(10 * UI_SCALE).render(str(inventory[item]), False, (19, 17, 18)), (SCREEN_SIZE[0] // 2 + (32 * t - 16 * INVENTORY_SIZE + 4) * UI_SCALE, SCREEN_SIZE[1] - 24 * UI_SCALE))
                t += 1
            if "open" in tile_attributes.get(machine_ui, ()):
                window.blit(pg.transform.scale(images["big_inventory_slot"], (320 * UI_SCALE, 128 * UI_SCALE)), (SCREEN_SIZE[0] // 2 - 160 * UI_SCALE, SCREEN_SIZE[1] - 160 * UI_SCALE))
                window.blit(pg.transform.scale(images["inventory_slot_3"], (32 * UI_SCALE, 32 * UI_SCALE)), (SCREEN_SIZE[0] // 2 + 88 * UI_SCALE, SCREEN_SIZE[1] - 80 * UI_SCALE))
                window.blit(pg.transform.scale(images[machine_ui], (16 * UI_SCALE, 24 * UI_SCALE)), (SCREEN_SIZE[0] // 2 + 96 * UI_SCALE, SCREEN_SIZE[1] - 76 * UI_SCALE))
                if "craft" in tile_attributes.get(machine_ui, ()):
                    current_recipes = recipes[machine_ui]
                    window.blit(pg.transform.scale(images["big_inventory_slot_2"], (96 * UI_SCALE, 96 * UI_SCALE)), (SCREEN_SIZE[0] // 2 - 128 * UI_SCALE, SCREEN_SIZE[1] - 144 * UI_SCALE))
                    window.blit(pg.transform.scale(images[current_recipes[recipe_number][0][0]], (48 * UI_SCALE, 72 * UI_SCALE)), (SCREEN_SIZE[0] // 2 - 104 * UI_SCALE, SCREEN_SIZE[1] - 132 * UI_SCALE))
                    window.blit(font(20 * UI_SCALE).render(str(current_recipes[recipe_number][0][1]), False, (19, 17, 18)), (SCREEN_SIZE[0] // 2 - 112 * UI_SCALE, SCREEN_SIZE[1] - 80 * UI_SCALE))
                    for inputs in range(0, len(current_recipes[recipe_number][1])):
                        window.blit(pg.transform.scale(images["inventory_slot"], (32 * UI_SCALE, 32 * UI_SCALE)), (SCREEN_SIZE[0] // 2 + (40 * (inputs % 4) - 32) * UI_SCALE, SCREEN_SIZE[1] + (32 * (inputs // 4) - 144) * UI_SCALE))
                        window.blit(pg.transform.scale(images[current_recipes[recipe_number][1][inputs][0]], (16 * UI_SCALE, 24 * UI_SCALE)), (SCREEN_SIZE[0] // 2 + (40 * (inputs % 4) - 24) * UI_SCALE, SCREEN_SIZE[1] + (32 * (inputs // 4) - 140) * UI_SCALE))
                        window.blit(font(10 * UI_SCALE).render(str(current_recipes[recipe_number][1][inputs][1]), False, (19, 17, 18)), (SCREEN_SIZE[0] // 2 + (40 * (inputs % 4) - 24) * UI_SCALE, SCREEN_SIZE[1] + (32 * (inputs // 4) - 112) * UI_SCALE))
                elif "store" in tile_attributes.get(machine_ui, ()):
                    for item in range(0, storage[machine_ui][0]):
                        window.blit(pg.transform.scale(images["inventory_slot"], (32 * UI_SCALE, 32 * UI_SCALE)), (SCREEN_SIZE[0] // 2 + (32 * (item % 7) - 112) * UI_SCALE, SCREEN_SIZE[1] + (32 * (item // 7) - 144) * UI_SCALE))
                    machine_inventory = chunks[room_location][last_opened_location[0]][last_opened_location[1]].inventory
                    t = 0
                    for item in machine_inventory:
                        window.blit(pg.transform.scale(images[item], (16 * UI_SCALE, 24 * UI_SCALE)), (SCREEN_SIZE[0] // 2 + (32 * (t % 7) - 104) * UI_SCALE, SCREEN_SIZE[1] + (32 * (t // 7) - 140) * UI_SCALE))
                        window.blit(font(10 * UI_SCALE).render(str(machine_inventory[item]), False, (19, 17, 18)), (SCREEN_SIZE[0] // 2 + (32 * (t % 7) - 104) * UI_SCALE, SCREEN_SIZE[1] + (32 * (t // 7) - 140) * UI_SCALE))
                        t += 1
            tick += 1
        pg.display.update()
        clock.tick(60)
    pg.quit()