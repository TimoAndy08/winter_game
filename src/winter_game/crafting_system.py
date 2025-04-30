def recipe(
    output: dict[str, int],
    input: dict[str, int],
    inventory: dict[str, int],
    max_items: tuple[int, int],
):
    output_item, output_amount = output
    if (len(inventory) >= max_items[0] and inventory.get(output_item, 0) + output_amount >= max_items[1]):
        return inventory
    for i in range(0, len(input)):
        if input[i][0] not in inventory or inventory[input[i][0]] < input[i][1]:
            return inventory
    for i in range(0, len(input)):
        inventory[input[i][0]] -= input[i][1]
        if inventory[input[i][0]] <= 0:
            del inventory[input[i][0]]
    inventory[output_item] = inventory.get(output_item, 0) + output_amount
    return inventory