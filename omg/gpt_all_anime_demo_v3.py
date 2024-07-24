import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Character Animation Example"

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
# Frame update time in seconds
ANIMATION_SPEED = 0.1

# Character states
IDLE = "Idle"
WALK = "Walk"
SLASH = "Slash"
SPELLCAST = "SpellCast"
THRUST = "Thrust"
SHOOT = "Shoot"
DIE = "Die"

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """ Initializer """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Sprite lists
        self.all_sprites_list = None

        # Player sprite
        self.player_sprite = None

        # Player state
        self.player_state = IDLE

        # Health
        self.health = 100

        main_path = "C:/Users/Admin/Desktop/2D_Sprite_Animations/demo_archer/sprites"

        # Load textures for different animations
        self.idle_textures = [arcade.load_texture(f"{main_path}/Walk_Down{i}.png") for i in range(1)]
        self.walk_textures = [arcade.load_texture(f"{main_path}/Walk_Down{i}.png") for i in range(9)]
        self.slash_textures = [arcade.load_texture(f"{main_path}/Slash_Down{i}.png") for i in range(6)]
        self.spellcast_textures = [arcade.load_texture(f"{main_path}/Cast_Down{i}.png") for i in range(7)]
        self.thrust_textures = [arcade.load_texture(f"{main_path}/Thrust_Down{i}.png") for i in range(8)]
        self.shoot_textures = [arcade.load_texture(f"{main_path}/Shoot_Down{i}.png") for i in range(12)]
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

        # Game state
        self.game_over = False

        # Key states
        self.w_pressed = False
        self.a_pressed = False
        self.s_pressed = False
        self.d_pressed = False

        # Movement direction
        self.move_direction = (0, 0)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.all_sprites_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite()
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_sprite.scale = 2
        self.all_sprites_list.append(self.player_sprite)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        # Draw all the sprites
        self.all_sprites_list.draw()

        # Draw health bar
        arcade.draw_text(f"Health: {self.health}", 10, 570, arcade.color.WHITE, 14)

        if self.game_over:
            arcade.draw_text("Game Over", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.WHITE, 54, anchor_x="center")

    def update(self, delta_time):
        """ Movement and game logic """
        if self.game_over:
            self.animation_timer += delta_time
            if self.animation_timer > 3:  # Wait for 3 seconds
                self.setup()
                self.game_over = False
                self.health = 100
                self.player_state = IDLE
                self.animation_timer = 0
            return

        self.update_animation(delta_time)

        if self.player_state == WALK:
            self.update_movement()

        # Call update on all sprites (The sprites don't do much in this example though.)
        self.all_sprites_list.update()

    def update_animation(self, delta_time):
        """ Update the animation state of the player """
        self.animation_timer += delta_time

        if self.animation_timer > ANIMATION_SPEED:
            if self.player_state == IDLE:
                self.player_sprite.texture = self.idle_textures[self.idle_texture_index]
                self.idle_texture_index = (self.idle_texture_index + 1) % len(self.idle_textures)
            elif self.player_state == WALK:
                self.player_sprite.texture = self.walk_textures[self.walk_texture_index]
                self.walk_texture_index = (self.walk_texture_index + 1) % len(self.walk_textures)
            elif self.player_state == SLASH:
                self.player_sprite.texture = self.slash_textures[self.slash_texture_index]
                self.slash_texture_index += 1
                if self.slash_texture_index >= len(self.slash_textures):
                    self.finish_action()
                    self.slash_texture_index = 0
            elif self.player_state == SPELLCAST:
                self.player_sprite.texture = self.spellcast_textures[self.spellcast_texture_index]
                self.spellcast_texture_index += 1
                if self.spellcast_texture_index >= len(self.spellcast_textures):
                    self.finish_action()
                    self.spellcast_texture_index = 0
            elif self.player_state == THRUST:
                self.player_sprite.texture = self.thrust_textures[self.thrust_texture_index]
                self.thrust_texture_index += 1
                if self.thrust_texture_index >= len(self.thrust_textures):
                    self.finish_action()
                    self.thrust_texture_index = 0
            elif self.player_state == SHOOT:
                self.player_sprite.texture = self.shoot_textures[self.shoot_texture_index]
                self.shoot_texture_index += 1
                if self.shoot_texture_index >= len(self.shoot_textures):
                    self.finish_action()
                    self.shoot_texture_index = 0
            elif self.player_state == DIE:
                self.player_sprite.texture = self.die_textures[self.die_texture_index]
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
        self.player_sprite.change_x = self.move_direction[0] * 1
        self.player_sprite.change_y = self.move_direction[1] * 1

        if self.player_sprite.change_x == 0 and self.player_sprite.change_y == 0:
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

        if key == arcade.key.KEY_1 and self.player_state not in [SLASH, SPELLCAST, THRUST, SHOOT, DIE]:
            self.player_state = SLASH
            self.slash_texture_index = 0
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
        elif key == arcade.key.KEY_2 and self.player_state not in [SLASH, SPELLCAST, THRUST, SHOOT, DIE]:
            self.player_state = SPELLCAST
            self.spellcast_texture_index = 0
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
        elif key == arcade.key.KEY_3 and self.player_state not in [SLASH, SPELLCAST, THRUST, SHOOT, DIE]:
            self.player_state = THRUST
            self.thrust_texture_index = 0
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
        elif key == arcade.key.KEY_4 and self.player_state not in [SLASH, SPELLCAST, THRUST, SHOOT, DIE]:
            self.player_state = SHOOT
            self.shoot_texture_index = 0
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0

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

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
