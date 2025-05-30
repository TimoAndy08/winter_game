from ...info import SCREEN_SIZE, INVENTORY_SIZE, UI_SCALE, STORAGE

def storage(position, chunks, location, inventory, machine_ui):
    moved_x = position[0] - SCREEN_SIZE[0] // 2
    machine_inventory = chunks[location["room"]][location["opened"][0]][
        location["opened"][1]
    ].inventory
    if (
        position[1] >= SCREEN_SIZE[1] - 32 * UI_SCALE
        and abs(moved_x) <= 16 * INVENTORY_SIZE[0] * UI_SCALE
    ):
        slot_number = (
            (moved_x - 16 * UI_SCALE * (INVENTORY_SIZE[0] % 2)) // (32 * UI_SCALE)
            + INVENTORY_SIZE[0] // 2
            + INVENTORY_SIZE[0] % 2
        )
        if slot_number < len(inventory):
            item = list(inventory.items())[slot_number]
            machine_item = machine_inventory.get(item[0], 0)
            if not (
                machine_item == 0
                and len(machine_inventory) == STORAGE[machine_ui][0]
            ):
                if machine_item + item[1] <= STORAGE[machine_ui][1]:
                    chunks[location["room"]][location["opened"][0]][
                        location["opened"][1]
                    ].inventory[item[0]] = machine_item + item[1]
                    del chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                        (location["tile"][2], location["tile"][3])
                    ].inventory[item[0]]
                else:
                    chunks[location["room"]][location["opened"][0]][
                        location["opened"][1]
                    ].inventory[item[0]] = STORAGE[machine_ui][1]
                    chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                        (location["tile"][2], location["tile"][3])
                    ].inventory[item[0]] = (
                        machine_item + item[1] - STORAGE[machine_ui][1]
                    )
    elif (
        SCREEN_SIZE[1] - 144 * UI_SCALE
        <= position[1]
        <= SCREEN_SIZE[1] - 80 * UI_SCALE
        and abs(moved_x) <= 112 * UI_SCALE
    ):
        slot_number = (moved_x + 112 * UI_SCALE) // (32 * UI_SCALE) + (
            position[1] - SCREEN_SIZE[1] + 144 * UI_SCALE
        ) // (32 * UI_SCALE) * 7
        if slot_number < len(machine_inventory):
            item = list(machine_inventory.items())[slot_number]
            inventory_item = inventory.get(item[0], 0)
            if not (inventory_item == 0 and len(inventory) == INVENTORY_SIZE[0]):
                if inventory_item + item[1] <= INVENTORY_SIZE[1]:
                    chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                        (location["tile"][2], location["tile"][3])
                    ].inventory[item[0]] = inventory_item + item[1]
                    del chunks[location["room"]][location["opened"][0]][
                        location["opened"][1]
                    ].inventory[item[0]]
                else:
                    chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                        (location["tile"][2], location["tile"][3])
                    ].inventory[item[0]] = INVENTORY_SIZE[1]
                    chunks[location["room"]][location["opened"][0]][
                        location["opened"][1]
                    ].inventory[item[0]] = inventory_item + item[1] - INVENTORY_SIZE[1]
    return chunks