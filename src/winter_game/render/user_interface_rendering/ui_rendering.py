import pygame as pg

from .health_rendering import render_health
from .inventory_rendering import render_inventory
from .machine_rendering import render_machine

def render_ui(inventory_number, inventory, machine_ui, recipe_number, health, max_health, machine_inventory, window, images):
    window = render_health(window, images, health, max_health)
    window = render_inventory(inventory_number, window, images, inventory)
    window = render_machine(machine_ui, window, images, recipe_number, machine_inventory)
    return window