import arcade
import random
import math
import arcade.key
import arcade.gui


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Johnny Geliyor"

COIN_SCALE = 0.5
COIN_COUNT = 50
CHARACTER_SCALING = 2
SWING_SCALING = 0.2
SWING_FADE_RATE = 8

# How fast to move, and how fast to run the animation
MOVEMENT_SPEED = 2
UPDATES_PER_FRAME = 5

# Constants used to track if the player is facing left or right
DOWN_FACING = 0
UP_FACING = 1
RIGHT_FACING = 2
LEFT_FACING = 3

def load_texture(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return arcade.load_texture(filename)

class QuitButton(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        arcade.exit()

class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        back_button = arcade.gui.UIFlatButton(text="Back", width=200)
        self.v_box.add(back_button.with_space_around(bottom=20))

        # Add a hook to run when we click on the button.
        back_button.on_click = self.on_click_start
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        self.manager.add(
           arcade.gui.UITextArea(x=SCREEN_WIDTH/2,
                                 y=SCREEN_HEIGHT/2,
                                 width=200,
                                 height=300,
                                 text="Work in progress...",
                                 text_color=(0, 0, 0, 255),
                                 font_size=24
                                )
        )

    def on_click_start(self, event):
        game_view = StartView()
        self.window.show_view(game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()

class StartView(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Set background color
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        self.v_box.add(start_button.with_space_around(bottom=20))

        settings_button = arcade.gui.UIFlatButton(text="Settings", width=200)
        self.v_box.add(settings_button.with_space_around(bottom=20))

        # Again, method 1. Use a child class to handle events.
        quit_button = QuitButton(text="Quit", width=200)
        self.v_box.add(quit_button)

        # --- Method 2 for handling click events,
        # assign self.on_click_start as callback
        start_button.on_click = self.on_click_start

        # --- Method 3 for handling click events,
        # use a decorator to handle on_click events
        @settings_button.event("on_click")
        def on_click_settings(event):
            game_view = SettingsView()
            self.window.show_view(game_view)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        game_view = MyGame()
        game_view.setup()
        self.window.show_view(game_view)

    def on_draw(self):
        self.clear()
        self.manager.draw()


class Sword(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        self.scale = SWING_SCALING

        self.cur_texture = 0

        # --- Load Textures ---
        main_path = "C:/Users/Admin/Desktop/2D_Sprite_Animations/Character_JohnnySins"

        self.swing_textures = []
        for i in range(7):
            texture = load_texture(f"{main_path}/SwordSwing/{i}.png")
            self.swing_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):
        self.cur_texture += 1
        if self.cur_texture > 6 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME
        self.texture = self.swing_textures[frame]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = DOWN_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.cur_texture_oneTime = 0

        # Check the action
        self.actionType = ""
        self.animationDone = False

        self.scale = CHARACTER_SCALING

        # --- Load Textures ---
        # main_path = "C:/Users/Admin/Desktop/2D_Sprite_Animations/Character_JohnnySins"
        main_path = "C:/Users/Admin/Desktop/2D_Sprite_Animations/demo_archer/sprites"
    
        # Load textures for idle standing
        self.idle_textures_down = load_texture(f"{main_path}/Walk_Down0.png")
        self.idle_textures_up = load_texture(f"{main_path}/Walk_Up0.png")
        self.idle_textures_right = load_texture(f"{main_path}/Walk_Right0.png")
        self.idle_textures_left = load_texture(f"{main_path}/Walk_Left0.png")

        # Load textures for walking
        self.walk_textures_down = []
        self.walk_textures_up = []
        self.walk_textures_right = []
        self.walk_textures_left = []
        for i in range(9):
            texture = load_texture(f"{main_path}/Walk_Down{i}.png")
            self.walk_textures_down.append(texture)
            texture = load_texture(f"{main_path}/Walk_Up{i}.png")
            self.walk_textures_up.append(texture)
            texture = load_texture(f"{main_path}/Walk_Right{i}.png")
            self.walk_textures_right.append(texture)
            texture = load_texture(f"{main_path}/Walk_Left{i}.png")
            self.walk_textures_left.append(texture)
        
        # Load textures for slashing
        self.slash_textures_down = []
        self.slash_textures_up = []
        self.slash_textures_right = []
        self.slash_textures_left = []
        for i in range(6):
            texture = load_texture(f"{main_path}/Slash_Down{i}.png")
            self.slash_textures_down.append(texture)
            texture = load_texture(f"{main_path}/Slash_Up{i}.png")
            self.slash_textures_up.append(texture)
            texture = load_texture(f"{main_path}/Slash_Right{i}.png")
            self.slash_textures_right.append(texture)
            texture = load_texture(f"{main_path}/Slash_Left{i}.png")
            self.slash_textures_left.append(texture)

        # Load textures for back slashing
        self.backslash_textures_down = []
        self.backslash_textures_up = []
        self.backslash_textures_right = []
        self.backslash_textures_left = []
        for i in range(6):
            texture = load_texture(f"{main_path}/BackSlash_Down{i}.png")
            self.backslash_textures_down.append(texture)
            texture = load_texture(f"{main_path}/BackSlash_Up{i}.png")
            self.backslash_textures_up.append(texture)
            texture = load_texture(f"{main_path}/BackSlash_Right{i}.png")
            self.backslash_textures_right.append(texture)
            texture = load_texture(f"{main_path}/BackSlash_Left{i}.png")
            self.backslash_textures_left.append(texture)

        # Load textures for spell casting
        self.cast_textures_down = []
        self.cast_textures_up = []
        self.cast_textures_right = []
        self.cast_textures_left = []
        for i in range(7):
            texture = load_texture(f"{main_path}/Cast_Down{i}.png")
            self.cast_textures_down.append(texture)
            texture = load_texture(f"{main_path}/Cast_Up{i}.png")
            self.cast_textures_up.append(texture)
            texture = load_texture(f"{main_path}/Cast_Right{i}.png")
            self.cast_textures_right.append(texture)
            texture = load_texture(f"{main_path}/Cast_Left{i}.png")
            self.cast_textures_left.append(texture)

        # Load textures for shooting
        self.shoot_textures_down = []
        self.shoot_textures_up = []
        self.shoot_textures_right = []
        self.shoot_textures_left = []
        for i in range(12):
            texture = load_texture(f"{main_path}/Shoot_Down{i}.png")
            self.shoot_textures_down.append(texture)
            texture = load_texture(f"{main_path}/Shoot_Up{i}.png")
            self.shoot_textures_up.append(texture)
            texture = load_texture(f"{main_path}/Shoot_Right{i}.png")
            self.shoot_textures_right.append(texture)
            texture = load_texture(f"{main_path}/Shoot_Left{i}.png")
            self.shoot_textures_left.append(texture)

        # Load textures for thrusting
        self.thrust_textures_down = []
        self.thrust_textures_up = []
        self.thrust_textures_right = []
        self.thrust_textures_left = []
        for i in range(8):
            texture = load_texture(f"{main_path}/Thrust_Down{i}.png")
            self.thrust_textures_down.append(texture)
            texture = load_texture(f"{main_path}/Thrust_Up{i}.png")
            self.thrust_textures_up.append(texture)
            texture = load_texture(f"{main_path}/Thrust_Right{i}.png")
            self.thrust_textures_right.append(texture)
            texture = load_texture(f"{main_path}/Thrust_Left{i}.png")
            self.thrust_textures_left.append(texture)

        # Load textures for dying
        self.die_textures = []
        for i in range(6):
            texture = load_texture(f"{main_path}/Die{i}.png")
            self.die_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_y < 0 and self.character_face_direction != DOWN_FACING:
            self.character_face_direction = DOWN_FACING
        if self.change_y > 0 and self.character_face_direction != UP_FACING:
            self.character_face_direction = UP_FACING
        if self.change_x < 0 and self.character_face_direction != LEFT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction != RIGHT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0 and self.actionType == "Idle":
            self.cur_texture_oneTime = 0
            self.animationDone = True
            if self.character_face_direction == DOWN_FACING:
                self.texture = self.idle_textures_down
            elif self.character_face_direction == UP_FACING:
                self.texture = self.idle_textures_up
            elif self.character_face_direction == RIGHT_FACING:
                self.texture = self.idle_textures_right
            elif self.character_face_direction == LEFT_FACING:
                self.texture = self.idle_textures_left
            return
        
        if self.actionType == "Walk":
            # Walking animation
            self.cur_texture_oneTime = 0
            self.animationDone = True
            self.cur_texture += 1
            if self.cur_texture > 8 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction

            if direction == DOWN_FACING:
                self.texture = self.walk_textures_down[frame]
            if direction == UP_FACING:
                self.texture = self.walk_textures_up[frame]
            if direction == RIGHT_FACING:
                self.texture = self.walk_textures_right[frame]
            if direction == LEFT_FACING:
                self.texture = self.walk_textures_left[frame]

        elif self.actionType == "Cast":
            # Casting animation
            self.cur_texture += 1
            if self.cur_texture > 6 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction

            if direction == DOWN_FACING:
                self.texture = self.cast_textures_down[frame]
            if direction == UP_FACING:
                self.texture = self.cast_textures_up[frame]
            if direction == RIGHT_FACING:
                self.texture = self.cast_textures_right[frame]
            if direction == LEFT_FACING:
                self.texture = self.cast_textures_left[frame]

        elif self.actionType == "Slash":
            # Casting animation
            self.animationDone = False
            self.cur_texture_oneTime += 1
            if self.cur_texture_oneTime > 5 * UPDATES_PER_FRAME:
                self.cur_texture_oneTime = 0
                self.animationDone = True
                self.actionType = "Idle"
            frame = self.cur_texture_oneTime // UPDATES_PER_FRAME
            direction = self.character_face_direction

            if direction == DOWN_FACING:
                self.texture = self.slash_textures_down[frame]
            if direction == UP_FACING:
                self.texture = self.slash_textures_up[frame]
            if direction == RIGHT_FACING:
                self.texture = self.slash_textures_right[frame]
            if direction == LEFT_FACING:
                self.texture = self.slash_textures_left[frame]

        elif self.actionType == "BackSlash":
            # Casting animation
            self.cur_texture += 1
            if self.cur_texture > 5 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction

            if direction == DOWN_FACING:
                self.texture = self.backslash_textures_down[frame]
            if direction == UP_FACING:
                self.texture = self.backslash_textures_up[frame]
            if direction == RIGHT_FACING:
                self.texture = self.backslash_textures_right[frame]
            if direction == LEFT_FACING:
                self.texture = self.backslash_textures_left[frame]

        elif self.actionType == "Shoot":
            # Casting animation
            self.cur_texture += 1
            if self.cur_texture > 11 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction

            if direction == DOWN_FACING:
                self.texture = self.shoot_textures_down[frame]
            if direction == UP_FACING:
                self.texture = self.shoot_textures_up[frame]
            if direction == RIGHT_FACING:
                self.texture = self.shoot_textures_right[frame]
            if direction == LEFT_FACING:
                self.texture = self.shoot_textures_left[frame]

        elif self.actionType == "Thrust":
            # Casting animation
            self.cur_texture += 1
            if self.cur_texture > 7 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            direction = self.character_face_direction

            if direction == DOWN_FACING:
                self.texture = self.thrust_textures_down[frame]
            if direction == UP_FACING:
                self.texture = self.thrust_textures_up[frame]
            if direction == RIGHT_FACING:
                self.texture = self.thrust_textures_right[frame]
            if direction == LEFT_FACING:
                self.texture = self.thrust_textures_left[frame]

        elif self.actionType == "Die":
            # Casting animation
            self.cur_texture += 1
            if self.cur_texture > 5 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            frame = self.cur_texture // UPDATES_PER_FRAME
            self.texture = self.die_textures[frame]

class MyGame(arcade.View):
    """ Main application class. """

    def __init__(self):
        """ Set up the game and initialize the variables. """
        super().__init__()

        # Sprite lists
        self.player_list = None
        self.coin_list = None
        self.swing_list = None

        # Set up the player
        self.score = 0
        self.player = None
        self.swing = None

        # Animation enabler
        self.animation_bool = False

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.swing_list = arcade.SpriteList()

        # Set up the player
        self.will_be_removed_keys = set()
        self.pressed_keys = set()
        self.current_speed = MOVEMENT_SPEED
        self.speed_multiplier = 1
        self.score = 0
        self.player = PlayerCharacter()

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        
        self.player_list.append(self.player)

        for i in range(COIN_COUNT):
            coin = arcade.Sprite(":resources:images/items/gold_1.png",
                                 scale=0.5)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.
        self.coin_list.draw()
        self.player_list.draw()
        self.swing_list.draw()

        # self.player.draw_hit_box()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.W:
            self.pressed_keys.add(key)
            self.player.actionType = "Walk"
        elif key == arcade.key.S:
            self.pressed_keys.add(key)
            self.player.actionType = "Walk"
        elif key == arcade.key.A:
            self.pressed_keys.add(key)
            self.player.actionType = "Walk"
        elif key == arcade.key.D:
            self.pressed_keys.add(key)
            self.player.actionType = "Walk"
        elif key == arcade.key.LSHIFT:
            self.speed_multiplier = 2
            self.current_speed = MOVEMENT_SPEED * self.speed_multiplier
        elif key == arcade.key.KEY_1:
            self.pressed_keys.add(key)
            self.player.actionType = "Slash"

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.W:
            self.pressed_keys.remove(key)
        elif key == arcade.key.S:
            self.pressed_keys.remove(key)
        elif key == arcade.key.A:
            self.pressed_keys.remove(key)
        elif key == arcade.key.D:
            self.pressed_keys.remove(key)
        elif key == arcade.key.LSHIFT:
            self.speed_multiplier = 1
            self.current_speed = MOVEMENT_SPEED * self.speed_multiplier
        elif key == arcade.key.KEY_1:
            self.will_be_removed_keys.add(key)

    def on_mouse_press(self, x, y, button, modifiers):
        # Create swing sprite
        self.swing = Sword()
        self.animation_bool = True

        self.swing.center_x = self.player.center_x + 10
        self.swing.center_y = self.player.center_y
        # Position the bullet at the player's current location
        start_x = self.swing.center_x
        start_y = self.swing.center_y

        # Get from the mouse the destination location for the bullet
        # IMPORTANT! If you have a scrolling screen, you will also need
        # to add in self.view_bottom and self.view_left.
        dest_x = x
        dest_y = y

        # Do math to calculate how to get the bullet to the destination.
        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite so it doesn't look like it is flying
        # sideways.
        self.swing.angle = math.degrees(angle) - 90
        self.swing_list.append(self.swing)

    def on_mouse_release(self, x, y, button, modifiers):
        self.animation_bool = False
        # for swing in self.swing_list:
        #     swing.remove_from_sprite_lists()
    
    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player.change_x = 0
        self.player.change_y = 0

        # Movement
        if len(self.pressed_keys) == 0:
            self.player.actionType = "Idle"
        if self.player.animationDone:
            if arcade.key.W in self.pressed_keys:
                self.player.change_y = self.current_speed
            if arcade.key.S in self.pressed_keys:
                self.player.change_y = -self.current_speed
            if arcade.key.A in self.pressed_keys:
                self.player.change_x = -self.current_speed
            if arcade.key.D in self.pressed_keys:
                self.player.change_x = self.current_speed

        # Move the player
        self.player_list.update()
        self.swing_list.update()
        # Update the players animation
        self.player_list.update_animation()
        self.swing_list.update_animation()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.score += 1 

        
def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    # start_view.setup()
    arcade.run()

    # window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    # window.setup()
    # arcade.run()


if __name__ == "__main__":
    main()
