def transport_item(output_kind, machine_inventory, output_inventory, item_tick):
    if output_kind in machine_inventory:
        output_number = min(machine_inventory[output_kind], min(item_tick, 2 * item_tick - output_inventory.get(output_kind, 0)))
        if output_kind not in output_inventory:
            output_inventory[output_kind] = output_number
        else:
            output_inventory[output_kind] += output_number
        machine_inventory[output_kind] -= output_number
        if machine_inventory[output_kind] == 0:
            del machine_inventory[output_kind]
    return machine_inventory, output_inventory