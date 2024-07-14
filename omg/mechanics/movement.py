import arcade

def setup_movement_keys(player):
    key_state = {
        player.key_forward: False,
        player.key_backward: False,
        player.key_left: False,
        player.key_right: False
    }

    def on_key_press(key, modifiers):
        if key in key_state:
            key_state[key] = True
        update_player_velocity(player, key_state)

    def on_key_release(key, modifiers):
        if key in key_state:
            key_state[key] = False
        update_player_velocity(player, key_state)

    return on_key_press, on_key_release

def update_player_velocity(player, key_state):
    forward = 1 if key_state[player.key_forward] else 0
    backward = -1 if key_state[player.key_backward] else 0
    left = -1 if key_state[player.key_left] else 0
    right = 1 if key_state[player.key_right] else 0

    player.change_x = forward + backward
    player.change_y = left + right
