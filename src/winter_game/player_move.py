def move_player(key, controls, velocity, real_location):
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
    return (real_location, tile_location, velocity)