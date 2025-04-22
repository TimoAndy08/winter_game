from .tile_info import TOOL_REQUIRED, TOOL_EFFICIENCY
from .tile_class import Tile


def right_click(
    chunks,
    grid_position,
    inventory,
    inventory_number,
    INVENTORY_SIZE,
    max_health,
    location,
    machine_ui,
):
    if grid_position[1] in chunks[location["room"]][grid_position[0]]:
        damage = (
            1 - chunks[location["room"]][grid_position[0]][grid_position[1]].resistance
        )
        if len(inventory) > inventory_number:
            inventory_key = list(inventory.keys())[inventory_number]
            inventory_words = inventory_key.split()
            if (
                len(inventory_words) == 2
                and chunks[location["room"]][grid_position[0]][grid_position[1]].kind
                in TOOL_REQUIRED
            ):
                if (
                    TOOL_REQUIRED[
                        chunks[location["room"]][grid_position[0]][grid_position[1]].kind
                    ]
                    == inventory_words[1]
                ):
                    damage += TOOL_EFFICIENCY[inventory_words[0]]
        chunks[location["room"]][grid_position[0]][grid_position[1]].health -= max(
            damage, 0
        )
        location["mined"] = [
            grid_position[0][0],
            grid_position[0][1],
            grid_position[1][0],
            grid_position[1][1],
        ]
        if chunks[location["room"]][grid_position[0]][grid_position[1]].health <= 0:
            if (
                chunks[location["room"]][grid_position[0]][grid_position[1]].kind
                != "player"
            ):
                junk_inventory = {}
                if (
                    not "no_pickup"
                    in chunks[location["room"]][grid_position[0]][
                        grid_position[1]
                    ].attributes
                ):
                    chunks[location["room"]][grid_position[0]][grid_position[1]].inventory[
                        chunks[location["room"]][grid_position[0]][grid_position[1]].kind
                    ] = (
                        chunks[location["room"]][grid_position[0]][
                            grid_position[1]
                        ].inventory.get(
                            chunks[location["room"]][grid_position[0]][
                                grid_position[1]
                            ].kind,
                            0,
                        )
                        + 1
                    )
                for item, amount in chunks[location["room"]][grid_position[0]][
                    grid_position[1]
                ].inventory.items():
                    if (
                        item
                        in chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                            (location["tile"][2], location["tile"][3])
                        ].inventory
                    ):
                        chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                            (location["tile"][2], location["tile"][3])
                        ].inventory[item] += amount
                        if inventory[item] > 64:
                            junk_inventory[item] = (
                                chunks[location["room"]][
                                    (location["tile"][0], location["tile"][1])
                                ][(location["tile"][2], location["tile"][3])].inventory[item]
                                - 64
                            )
                            chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                                (location["tile"][2], location["tile"][3])
                            ].inventory[item] = 64
                    else:
                        if len(inventory) < INVENTORY_SIZE:
                            chunks[location["room"]][(location["tile"][0], location["tile"][1])][
                                (location["tile"][2], location["tile"][3])
                            ].inventory[item] = amount
                        else:
                            junk_inventory[item] = amount
                if (
                    "enter"
                    in chunks[location["room"]][grid_position[0]][
                        grid_position[1]
                    ].attributes
                    and (*grid_position[0], *grid_position[1]) in chunks
                ):
                    del chunks[(*grid_position[0], *grid_position[1])]
                del chunks[location["room"]][grid_position[0]][grid_position[1]]
                if len(junk_inventory) > 0:
                    chunks[location["room"]][grid_position[0]][grid_position[1]] = Tile(
                        "junk", 1, 0, junk_inventory
                    )
                machine_ui = "game"
            else:
                chunks[location["room"]][grid_position[0]][grid_position[1]] = Tile(
                    "corpse", 1, 0, inventory
                )
                i = 0
                while (i % 16, i // 16) in chunks[(0, 0, 0, 0)][(0, 0)]:
                    i += 1
                    if i == 256:
                        i = 0
                        break
                chunks[(0, 0, 0, 0)][(0, 0)][(i % 16, i // 16)] = Tile(
                    "player", max_health, 0, {}
                )
                location["tile"] = [0, 0, i % 16, i // 16]
                location["real"] = [0, 0, i % 16, i // 16]
                location["room"] = (0, 0, 0, 0)
    return (chunks, location, machine_ui)
