import os

from omg.mechanics.animation import Animation
# from omg.mechanics.movement import PlayerMovement

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

    def __init__(self, slash_key, cast_key, thrust_key, shoot_key):

        self.key_to_action_dict = {
            slash_key: SLASH,
            cast_key: SPELLCAST,
            thrust_key: THRUST,
            shoot_key: SHOOT,
         }

        self._player_state = IDLE
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
        self._is_moving: bool = False

        # Action finish checker
        self.action_finished = 0


    def update(self, delta_time, player_change_x, player_change_y, is_moving):

        self._is_moving = is_moving
        # Movement and game logic
        self.update_animation(delta_time, player_change_x, player_change_y)

        if self._player_state == WALK:
            self.update_movement()

        return self.player_texture

    def update_animation(self, delta_time, player_change_x=0, player_change_y=0):

        # Figure out if we need to flip face left or right
        if player_change_y < 0 and self.character_face_direction != DOWN_FACING:
            self.character_face_direction = DOWN_FACING
        if player_change_y > 0 and self.character_face_direction != UP_FACING:
            self.character_face_direction = UP_FACING
        if player_change_x < 0 and self.character_face_direction != LEFT_FACING:
            self.character_face_direction = LEFT_FACING
        if player_change_x > 0 and self.character_face_direction != RIGHT_FACING:
            self.character_face_direction = RIGHT_FACING

        """ Update the animation state of the player """
        self.animation_timer += delta_time

        if self.animation_timer > ANIMATION_SPEED:
            current_animation: Animation = self.all_animations[self._player_state]
            self.player_texture, is_animation_finished = current_animation.get_next_texture(self.character_face_direction)

            if is_animation_finished:
                self.finish_action()

            self.animation_timer = 0


    def finish_action(self):
        """ Handle finishing an action and transition to the appropriate state """
        if self._is_moving:
            self._player_state = WALK
            self.update_movement()
        else:
            self._player_state = IDLE

    def update_movement(self):
        """ Update the player's movement based on the keys pressed """
        self.action_finished = 1

        if not self._is_moving:
            self._player_state = IDLE

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        
        if self._player_state  not in self.key_to_action_dict.values():
            self._player_state = self.key_to_action_dict.get(key, WALK)
            if self._player_state != WALK:
                self.action_finished = 0

    def on_key_release(self, key, modifiers):
        """ Called whenever a key is released. """

        if self._is_moving and self._player_state == IDLE:
            self._player_state = WALK
