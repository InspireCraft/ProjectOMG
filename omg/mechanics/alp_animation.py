import os
import arcade
from omg.mechanics.textures import Textures
from omg.mechanics.movement import PlayerMovement

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
    
    def __init__(self, slash_key, cast_key, thrust_key, shoot_key, move_logic):
        
        self.slash_key = slash_key
        self.cast_key = cast_key
        self.thrust_key = thrust_key
        self.shoot_key = shoot_key
        
        self.player_state = IDLE
        self.character_face_direction = DOWN_FACING
        self.player_texture = ""

        main_path = str(os.path.join(ASSET_DIR, "characters", "demo_archer", "sprites"))
        self.textures = Textures(sprite_path=main_path)

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
            self.textures.set_texture(direction="down")
            direction = "down"
        if self.player_change_y > 0 and self.character_face_direction != UP_FACING:
            self.character_face_direction = UP_FACING
            self.textures.set_texture(direction="up")
            direction = "up"
        if self.player_change_x < 0 and self.character_face_direction != LEFT_FACING:
            self.character_face_direction = LEFT_FACING
            self.textures.set_texture(direction="left")
            direction = "left"
        if self.player_change_x > 0 and self.character_face_direction != RIGHT_FACING:
            self.character_face_direction = RIGHT_FACING
            self.textures.set_texture(direction="right") 
            direction = "right"

        """ Update the animation state of the player """
        self.animation_timer += delta_time
        self.textures_all = {'IDLE': Texture(path_to_idle), 'WALK': Texture(path_to_walk), "SLASH": Texture(path_to_slash)}
        for texture in self.textures_all:
            texture.set_direction(self, direction)


        if self.animation_timer > ANIMATION_SPEED:
            active_texture = self.textures_all[self.player_state]
            current_image, is_over = active_texture.get_current_frame()

            if is_over:
                self.finish_action()

            self.animation_timer = 0
            return current_image


        if self.animation_timer > ANIMATION_SPEED:
            if self.player_state == IDLE:
                self.player_texture = self.textures.idle[self.textures.idle_index]
                self.textures.increment_index(state="idle")

            elif self.player_state == WALK:
                self.player_texture = self.textures.walk[self.textures.walk_index]
                self.textures.increment_index(state="walk")

            elif self.player_state == SLASH:
                self.player_texture = self.textures.slash[self.textures.slash_index]
                self.textures.increment_index(state="slash")
                if self.textures.slash_index >= len(self.textures.slash):
                    self.finish_action()
                    self.textures.reset_index(state="slash")

            elif self.player_state == SPELLCAST:
                self.player_texture = self.textures.spellcast[self.textures.spellcast_index]
                self.textures.increment_index(state="spellcast")
                if self.textures.spellcast_index >= len(self.textures.spellcast):
                    self.finish_action()
                    self.textures.reset_index(state="spellcast")
            elif self.player_state == THRUST:
                self.player_texture = self.textures.thrust[self.textures.thrust_index]
                self.textures.increment_index(state="thrust")
                if self.textures.thrust_index >= len(self.textures.thrust):
                    self.finish_action()
                    self.textures.reset_index(state="thrust")
            elif self.player_state == SHOOT:
                self.player_texture = self.textures.shoot[self.textures.shoot_index]
                self.textures.increment_index(state="shoot")
                if self.textures.shoot_index >= len(self.textures.shoot):
                    self.finish_action()
                    self.textures.reset_index(state="shoot")
            elif self.player_state == DIE:
                self.player_texture = self.textures.die[self.textures.die_index]
                self.textures.increment_index(state="die")
                if self.textures.die_index >= len(self.textures.die):
                    self.game_over = True
                    self.textures.reset_index(state="die")

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
        # if key == arcade.key.W:
        #     self.w_pressed = True
        #     self.move_direction = (self.move_direction[0], PLAYER_MOVEMENT_SPEED)
        #     # self.move_direction = self.move_logic.move_direction
        # elif key == arcade.key.S:
        #     self.s_pressed = True
        #     self.move_direction = (self.move_direction[0], -PLAYER_MOVEMENT_SPEED)
        # elif key == arcade.key.A:
        #     self.a_pressed = True
        #     self.move_direction = (-PLAYER_MOVEMENT_SPEED, self.move_direction[1])
        # elif key == arcade.key.D:
        #     self.d_pressed = True
        #     self.move_direction = (PLAYER_MOVEMENT_SPEED, self.move_direction[1])

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
        # if key == arcade.key.W:
        #     self.w_pressed = False
        #     if not self.s_pressed:
        #         self.move_direction = (self.move_direction[0], 0)
        # elif key == arcade.key.S:
        #     self.s_pressed = False
        #     if not self.w_pressed:
        #         self.move_direction = (self.move_direction[0], 0)
        # elif key == arcade.key.A:
        #     self.a_pressed = False
        #     if not self.d_pressed:
        #         self.move_direction = (0, self.move_direction[1])
        # elif key == arcade.key.D:
        #     self.d_pressed = False
        #     if not self.a_pressed:
        #         self.move_direction = (0, self.move_direction[1])

        self.check_movement_keys()

    def check_movement_keys(self):
        """ Check if any movement keys are pressed and update the state """
        if self.move_direction != (0, 0):
            if self.player_state == IDLE:
                self.player_state = WALK


 class Texture():
            __init__(self, path, prefix):
                self.images_up:List[Images] = load_from_path(path, "up")
                self.images_down:List[Images] = load_from_path(path, "down")
                self.images_left:List[Images] = load_from_path(path, "left")
                self.images_right:List[Images] = load_from_path(path, "right")
                self.max_counter_up = len(self.images_up)
                self.max_counter_down = len(self.images_down)
                self.max_counter_left = len(self.images_left)
                self.max_counter_right = len(self.images_right)
                self.current_idx = 0
                self.current_direction = "Up"


            def set_direction(self, direction):
                if direction != self.current_direction:
                    self.current_idx = 0 
                    self.current_direction = direction

            def get_current_frame(self):
                if self.current_idx < getattr(self, f"max_counter_{self.current_direction}"):
                    self.current_idx +=1
                    current_image_list = getattr(self, f"images_{self.current_direction}")
                    current_frame = current_image_list[self.current_idx]
                    is_over = False
                elif self.current_idx == getattr(self, f"max_counter_{self.current_direction}"):
                    current_frame = None
                    is_over = True
                    
                else:
                    raise ValueError(f"This should not be possible, self.current_idx  = {self.current_idx }")
                
                return current_frame, is_over
                
