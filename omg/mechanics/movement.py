import arcade

def setup_movement_keys(player, key_bindings=None):
    if key_bindings is None:
        key_bindings = {'up': arcade.key.W, 'left': arcade.key.A, 'down': arcade.key.S, 'right': arcade.key.D}
    
    def on_key_press(key, modifiers):
        if key == key_bindings['up']:
            player.change_y = 5
        elif key == key_bindings['left']:
            player.change_x = -5
        elif key == key_bindings['down']:
            player.change_y = -5
        elif key == key_bindings['right']:
            player.change_x = 5

    def on_key_release(key, modifiers):
        if key == key_bindings['up'] or key == key_bindings['down']:
            player.change_y = 0
        elif key == key_bindings['left'] or key == key_bindings['right']:
            player.change_x = 0

    return on_key_press, on_key_release
