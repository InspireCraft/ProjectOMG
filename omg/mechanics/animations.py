import os
import arcade

ASSET_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "assets", "images"
)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 3
# Frame update time in seconds
ANIMATION_SPEED = 0.08

# Character states
IDLE = "Idle"
WALK = "Walk"
SLASH = "Slash"
SPELLCAST = "SpellCast"
THRUST = "Thrust"
SHOOT = "Shoot"
DIE = "Die"

# Constants used to track if the player is facing left or right
DOWN_FACING = 0
UP_FACING = 1
RIGHT_FACING = 2
LEFT_FACING = 3


class Animations():
    
    def __init__(self, slash_key, cast_key, thrust_key, shoot_key):
        
        self.slash_key = slash_key
        self.cast_key = cast_key
        self.thrust_key = thrust_key
        self.shoot_key = shoot_key
        
        self.player_state = IDLE
        self.character_face_direction = DOWN_FACING
        self.player_texture = ""

        main_path = str(os.path.join(ASSET_DIR, "characters", "demo_archer", "sprites"))
        # main_path = "C:\Users\arda6\Desktop\Python\ProjectOMG\omg\assets\images\characters\demo_archer\sprites"

        # Load textures for different animations
        self.idle_textures = [arcade.load_texture(f"{main_path}/Walk_Down{i}.png") for i in range(1)]
        self.walk_textures = [arcade.load_texture(f"{main_path}/Walk_Down{i}.png") for i in range(9)]
        self.slash_textures = [arcade.load_texture(f"{main_path}/Slash_Down{i}.png") for i in range(6)]
        self.spellcast_textures = [arcade.load_texture(f"{main_path}/Cast_Down{i}.png") for i in range(7)]
        self.thrust_textures = [arcade.load_texture(f"{main_path}/Thrust_Down{i}.png") for i in range(8)]
        self.shoot_textures = [arcade.load_texture(f"{main_path}/Shoot_Down{i}.png") for i in range(12)]
        self.die_textures = [arcade.load_texture(f"{main_path}/Die{i}.png") for i in range(6)]

        self.idle_textures_up = [arcade.load_texture(f"{main_path}/Walk_Up{i}.png") for i in range(1)]
        self.idle_textures_down = [arcade.load_texture(f"{main_path}/Walk_Down{i}.png") for i in range(1)]
        self.idle_textures_left = [arcade.load_texture(f"{main_path}/Walk_Left{i}.png") for i in range(1)]
        self.idle_textures_right = [arcade.load_texture(f"{main_path}/Walk_Right{i}.png") for i in range(1)]
        self.walk_textures_up = [arcade.load_texture(f"{main_path}/Walk_Up{i}.png") for i in range(9)]
        self.walk_textures_down = [arcade.load_texture(f"{main_path}/Walk_Down{i}.png") for i in range(9)]
        self.walk_textures_left = [arcade.load_texture(f"{main_path}/Walk_Left{i}.png") for i in range(9)]
        self.walk_textures_right = [arcade.load_texture(f"{main_path}/Walk_Right{i}.png") for i in range(9)]
        self.slash_textures_up = [arcade.load_texture(f"{main_path}/Slash_Up{i}.png") for i in range(6)]
        self.slash_textures_down = [arcade.load_texture(f"{main_path}/Slash_Down{i}.png") for i in range(6)]
        self.slash_textures_left = [arcade.load_texture(f"{main_path}/Slash_Left{i}.png") for i in range(6)]
        self.slash_textures_right = [arcade.load_texture(f"{main_path}/Slash_Right{i}.png") for i in range(6)]
        self.spellcast_textures_up = [arcade.load_texture(f"{main_path}/Cast_Up{i}.png") for i in range(7)]
        self.spellcast_textures_down = [arcade.load_texture(f"{main_path}/Cast_Down{i}.png") for i in range(7)]
        self.spellcast_textures_left = [arcade.load_texture(f"{main_path}/Cast_Left{i}.png") for i in range(7)]
        self.spellcast_textures_right = [arcade.load_texture(f"{main_path}/Cast_Right{i}.png") for i in range(7)]
        self.thrust_textures_up = [arcade.load_texture(f"{main_path}/Thrust_Up{i}.png") for i in range(8)]
        self.thrust_textures_down = [arcade.load_texture(f"{main_path}/Thrust_Down{i}.png") for i in range(8)]
        self.thrust_textures_left = [arcade.load_texture(f"{main_path}/Thrust_Left{i}.png") for i in range(8)]
        self.thrust_textures_right = [arcade.load_texture(f"{main_path}/Thrust_Right{i}.png") for i in range(8)]
        self.shoot_textures_up = [arcade.load_texture(f"{main_path}/Shoot_Up{i}.png") for i in range(12)]
        self.shoot_textures_down = [arcade.load_texture(f"{main_path}/Shoot_Down{i}.png") for i in range(12)]
        self.shoot_textures_left = [arcade.load_texture(f"{main_path}/Shoot_Left{i}.png") for i in range(12)]
        self.shoot_textures_right = [arcade.load_texture(f"{main_path}/Shoot_Right{i}.png") for i in range(12)]
        self.die_textures = [arcade.load_texture(f"{main_path}/Die{i}.png") for i in range(6)]

        # Animation indices and timers
        self.idle_texture_index = 0
        self.walk_texture_index = 0
        self.slash_texture_index = 0
        self.spellcast_texture_index = 0
        self.thrust_texture_index = 0
        self.shoot_texture_index = 0
        self.die_texture_index = 0

        self.animation_timer = 0

        # Key states
        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False

        # Movement direction
        self.move_direction = (0, 0)

        # Action finish checker
        self.action_finished = 0

        self.player_change_x = 0
        self.player_change_y = 0

    def update(self, delta_time, player_change_x, player_change_y):
        # Movement and game logic
        self.player_change_x = player_change_x
        self.player_change_y = player_change_y
        self.update_animation(delta_time)

        if self.player_state == WALK:
            self.update_movement()

        return self.player_texture
    
    def update_animation(self, delta_time):

        # Figure out if we need to flip face left or right
        if self.player_change_y < 0 and self.character_face_direction != DOWN_FACING:
            self.character_face_direction = DOWN_FACING
            self.idle_textures = self.idle_textures_down
            self.walk_textures = self.walk_textures_down
            self.slash_textures = self.slash_textures_down
            self.spellcast_textures = self.spellcast_textures_down
            self.thrust_textures = self.thrust_textures_down
            self.shoot_textures = self.shoot_textures_down
        if self.player_change_y > 0 and self.character_face_direction != UP_FACING:
            self.character_face_direction = UP_FACING
            self.idle_textures = self.idle_textures_up
            self.walk_textures = self.walk_textures_up
            self.slash_textures = self.slash_textures_up
            self.spellcast_textures = self.spellcast_textures_up
            self.thrust_textures = self.thrust_textures_up
            self.shoot_textures = self.shoot_textures_up
        if self.player_change_x < 0 and self.character_face_direction != LEFT_FACING:
            self.character_face_direction = LEFT_FACING
            self.idle_textures = self.idle_textures_left
            self.walk_textures = self.walk_textures_left
            self.slash_textures = self.slash_textures_left
            self.spellcast_textures = self.spellcast_textures_left
            self.thrust_textures = self.thrust_textures_left
            self.shoot_textures = self.shoot_textures_left
        if self.player_change_x > 0 and self.character_face_direction != RIGHT_FACING:
            self.character_face_direction = RIGHT_FACING
            self.idle_textures = self.idle_textures_right
            self.walk_textures = self.walk_textures_right
            self.slash_textures = self.slash_textures_right
            self.spellcast_textures = self.spellcast_textures_right
            self.thrust_textures = self.thrust_textures_right
            self.shoot_textures = self.shoot_textures_right

        """ Update the animation state of the player """
        self.animation_timer += delta_time
            
        if self.animation_timer > ANIMATION_SPEED:
            if self.player_state == IDLE:
                self.player_texture = self.idle_textures[self.idle_texture_index]
                self.idle_texture_index = (self.idle_texture_index + 1) % len(self.idle_textures)
            elif self.player_state == WALK:
                self.player_texture = self.walk_textures[self.walk_texture_index]
                self.walk_texture_index = (self.walk_texture_index + 1) % len(self.walk_textures)
            elif self.player_state == SLASH:
                self.player_texture = self.slash_textures[self.slash_texture_index]
                self.slash_texture_index += 1
                if self.slash_texture_index >= len(self.slash_textures):
                    self.finish_action()
                    self.slash_texture_index = 0
            elif self.player_state == SPELLCAST:
                self.player_texture = self.spellcast_textures[self.spellcast_texture_index]
                self.spellcast_texture_index += 1
                if self.spellcast_texture_index >= len(self.spellcast_textures):
                    self.finish_action()
                    self.spellcast_texture_index = 0
            elif self.player_state == THRUST:
                self.player_texture = self.thrust_textures[self.thrust_texture_index]
                self.thrust_texture_index += 1
                if self.thrust_texture_index >= len(self.thrust_textures):
                    self.finish_action()
                    self.thrust_texture_index = 0
            elif self.player_state == SHOOT:
                self.player_texture = self.shoot_textures[self.shoot_texture_index]
                self.shoot_texture_index += 1
                if self.shoot_texture_index >= len(self.shoot_textures):
                    self.finish_action()
                    self.shoot_texture_index = 0
            elif self.player_state == DIE:
                self.player_texture = self.die_textures[self.die_texture_index]
                self.die_texture_index += 1
                if self.die_texture_index >= len(self.die_textures):
                    self.game_over = True
                    self.die_texture_index = 0

            self.animation_timer = 0

    def finish_action(self):
        """ Handle finishing an action and transition to the appropriate state """
        if self.move_direction != (0, 0):
            self.player_state = WALK
            self.update_movement()
        else:
            self.player_state = IDLE

    def update_movement(self):
        """ Update the player's movement based on the keys pressed """
        # Player.change_x = self.move_direction[0] * 1
        # Player.change_y = self.move_direction[1] * 1
        # self.player_change_x = self.move_direction[0] * 1
        # self.player_change_y = self.move_direction[1] * 1
        self.action_finished = 1

        if self.move_direction[0] == 0 and self.move_direction[1] == 0:
            self.player_state = IDLE

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        if key == arcade.key.W:
            self.w_pressed = True
            self.move_direction = (self.move_direction[0], PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.S:
            self.s_pressed = True
            self.move_direction = (self.move_direction[0], -PLAYER_MOVEMENT_SPEED)
        elif key == arcade.key.A:
            self.a_pressed = True
            self.move_direction = (-PLAYER_MOVEMENT_SPEED, self.move_direction[1])
        elif key == arcade.key.D:
            self.d_pressed = True
            self.move_direction = (PLAYER_MOVEMENT_SPEED, self.move_direction[1])

        if self.player_state not in [SLASH, SPELLCAST, THRUST, SHOOT, DIE]:
            self.player_state = WALK

        if key == self.slash_key and self.player_state not in [SLASH, SPELLCAST, THRUST, SHOOT, DIE]:
            self.player_state = SLASH
            self.slash_texture_index = 0
            self.action_finished = 0
        elif key == self.cast_key and self.player_state not in [SLASH, SPELLCAST, THRUST, SHOOT, DIE]:
            self.player_state = SPELLCAST
            self.spellcast_texture_index = 0
            self.action_finished = 0
        elif key == self.thrust_key and self.player_state not in [SLASH, SPELLCAST, THRUST, SHOOT, DIE]:
            self.player_state = THRUST
            self.thrust_texture_index = 0
            self.action_finished = 0
        elif key == self.shoot_key and self.player_state not in [SLASH, SPELLCAST, THRUST, SHOOT, DIE]:
            self.player_state = SHOOT
            self.shoot_texture_index = 0
            self.action_finished = 0

    def on_key_release(self, key, modifiers):
        """ Called whenever a key is released. """
        if key == arcade.key.W:
            self.w_pressed = False
            if not self.s_pressed:
                self.move_direction = (self.move_direction[0], 0)
        elif key == arcade.key.S:
            self.s_pressed = False
            if not self.w_pressed:
                self.move_direction = (self.move_direction[0], 0)
        elif key == arcade.key.A:
            self.a_pressed = False
            if not self.d_pressed:
                self.move_direction = (0, self.move_direction[1])
        elif key == arcade.key.D:
            self.d_pressed = False
            if not self.a_pressed:
                self.move_direction = (0, self.move_direction[1])

        self.check_movement_keys()

    def check_movement_keys(self):
        """ Check if any movement keys are pressed and update the state """
        if self.move_direction != (0, 0):
            if self.player_state == IDLE:
                self.player_state = WALK