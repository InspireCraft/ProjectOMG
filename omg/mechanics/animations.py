import os
import arcade
from omg.mechanics.textures import Textures
from omg.mechanics.movement import PlayerMovement
from omg.mechanics.animation import Animation

ASSET_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "assets", "images"
)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 3
# Frame update time in seconds
ANIMATION_SPEED = 0.08

# Character states
IDLE = "idle"
WALK = "walk"
SLASH = "slash"
SPELLCAST = "spellcast"
THRUST = "thrust"
SHOOT = "shoot"
DIE = "die"

# Constants used to track if the player is facing left or right
DOWN_FACING = "down"
UP_FACING = "up"
RIGHT_FACING = "right"
LEFT_FACING = 'left'


class Animations():

    def __init__(self, slash_key, cast_key, thrust_key, shoot_key, move_logic):

        self.slash_key = slash_key
        self.cast_key = cast_key
        self.thrust_key = thrust_key
        self.shoot_key = shoot_key

        self.player_state = IDLE
        self.character_face_direction = DOWN_FACING
        self.player_texture = ""

        main_path = str(os.path.join(ASSET_DIR, "characters", "demo_archer_2", "sprites"))

        animation_types = ["idle", "walk", "slash", "spellcast", "thrust", "shoot", "die"]
        self.all_animations = {}
        for action in animation_types:
            self.all_animations[action] = Animation(main_path, action)

        self.active_direction = "down"

        self.animation_timer = 0

        # Key states
        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False

        # Movement logic
        self.move_logic: PlayerMovement = move_logic

        # Action finish checker
        self.action_finished = 0

        self.player_change_x = 0
        self.player_change_y = 0

    @property
    def move_direction(self):
        return self.move_logic.move_direction

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
        if self.player_change_y > 0 and self.character_face_direction != UP_FACING:
            self.character_face_direction = UP_FACING
        if self.player_change_x < 0 and self.character_face_direction != LEFT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.player_change_x > 0 and self.character_face_direction != RIGHT_FACING:
            self.character_face_direction = RIGHT_FACING

        """ Update the animation state of the player """
        self.animation_timer += delta_time

        if self.animation_timer > ANIMATION_SPEED:
            current_animation: Animation = self.all_animations[self.player_state]
            self.player_texture, is_animation_finished = current_animation.get_next_texture(self.character_face_direction)

            if is_animation_finished:
                self.finish_action()

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
        self.action_finished = 1

        if self.move_direction[0] == 0 and self.move_direction[1] == 0:
            self.player_state = IDLE

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """

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

        self.check_movement_keys()

    def check_movement_keys(self):
        """ Check if any movement keys are pressed and update the state """
        if self.move_direction != (0, 0):
            if self.player_state == IDLE:
                self.player_state = WALK
