import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Character Shooting and Walking Animation Example"

# Animation Constants
CHARACTER_SCALING = 2
FRAME_RATE = 0.1  # Time per frame
SHOOT_FRAME_COUNT = 12  # Number of frames in the shoot animation
WALK_FRAME_COUNT = 9  # Number of frames in the walk animation
MOVEMENT_SPEED = 2
UPDATES_PER_FRAME = 5
COIN_COUNT = 50

# Constants used to track if the player is facing left or right
DOWN_FACING = 0
UP_FACING = 1
RIGHT_FACING = 2
LEFT_FACING = 3

# Paths to your sprite images
CHARACTER_SPRITE = "character_idle.png"
SHOOT_SPRITES = ["shoot_frame_1.png", "shoot_frame_2.png", "shoot_frame_3.png", "shoot_frame_4.png"]
WALK_SPRITES = ["walk_frame_1.png", "walk_frame_2.png", "walk_frame_3.png", "walk_frame_4.png"]

class Character(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = DOWN_FACING

        # Used for flipping between image sequences
        self.current_shoot_frame = 0
        self.current_walk_frame = 0
        self.is_shooting = False
        self.is_walking = False
        self.shoot_timer = 0
        self.walk_timer = 0

        self.scale = CHARACTER_SCALING

        # --- Load Textures ---
        # main_path = "C:/Users/Admin/Desktop/2D_Sprite_Animations/Character_JohnnySins"
        main_path = "C:/Users/Admin/Desktop/2D_Sprite_Animations/demo_archer/sprites"
    
        # Load textures for idle standing
        self.idle_textures_down = arcade.load_texture(f"{main_path}/Walk_Down0.png")
        self.idle_textures_up = arcade.load_texture(f"{main_path}/Walk_Up0.png")
        self.idle_textures_right = arcade.load_texture(f"{main_path}/Walk_Right0.png")
        self.idle_textures_left = arcade.load_texture(f"{main_path}/Walk_Left0.png")

        # Load textures for walking
        self.walk_textures_down = []
        self.walk_textures_up = []
        self.walk_textures_right = []
        self.walk_textures_left = []
        for i in range(9):
            texture = arcade.load_texture(f"{main_path}/Walk_Down{i}.png")
            self.walk_textures_down.append(texture)
            texture = arcade.load_texture(f"{main_path}/Walk_Up{i}.png")
            self.walk_textures_up.append(texture)
            texture = arcade.load_texture(f"{main_path}/Walk_Right{i}.png")
            self.walk_textures_right.append(texture)
            texture = arcade.load_texture(f"{main_path}/Walk_Left{i}.png")
            self.walk_textures_left.append(texture)

        # Load textures for shooting
        self.shoot_textures_down = []
        self.shoot_textures_up = []
        self.shoot_textures_right = []
        self.shoot_textures_left = []
        for i in range(12):
            texture = arcade.load_texture(f"{main_path}/Shoot_Down{i}.png")
            self.shoot_textures_down.append(texture)
            texture = arcade.load_texture(f"{main_path}/Shoot_Up{i}.png")
            self.shoot_textures_up.append(texture)
            texture = arcade.load_texture(f"{main_path}/Shoot_Right{i}.png")
            self.shoot_textures_right.append(texture)
            texture = arcade.load_texture(f"{main_path}/Shoot_Left{i}.png")
            self.shoot_textures_left.append(texture)

        # super().__init__(CHARACTER_SPRITE, CHARACTER_SCALING)
        # self.shoot_textures = []
        # for texture in SHOOT_SPRITES:
        #     self.shoot_textures.append(arcade.load_texture(texture))
        # self.walk_textures = []
        # for texture in WALK_SPRITES:
        #     self.walk_textures.append(arcade.load_texture(texture))
        # self.current_shoot_frame = 0
        # self.current_walk_frame = 0
        # self.is_shooting = False
        # self.is_walking = False
        # self.shoot_timer = 0
        # self.walk_timer = 0

    def update_animation(self, delta_time):
        # Update direction character facing
        if self.change_y < 0 and self.character_face_direction != DOWN_FACING:
            self.character_face_direction = DOWN_FACING
        if self.change_y > 0 and self.character_face_direction != UP_FACING:
            self.character_face_direction = UP_FACING
        if self.change_x < 0 and self.character_face_direction != LEFT_FACING:
            self.character_face_direction = LEFT_FACING
        if self.change_x > 0 and self.character_face_direction != RIGHT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.is_shooting:
            self.shoot_timer += delta_time
            if self.shoot_timer > FRAME_RATE:
                self.shoot_timer -= FRAME_RATE
                self.current_shoot_frame += 1
                if self.current_shoot_frame >= SHOOT_FRAME_COUNT:
                    self.is_shooting = False
                    self.current_shoot_frame = 0
                    if self.character_face_direction == DOWN_FACING:
                        self.texture = self.idle_textures_down
                    elif self.character_face_direction == UP_FACING:
                        self.texture = self.idle_textures_up
                    elif self.character_face_direction == RIGHT_FACING:
                        self.texture = self.idle_textures_right
                    elif self.character_face_direction == LEFT_FACING:
                        self.texture = self.idle_textures_left
                else:
                    if self.character_face_direction == DOWN_FACING:
                        self.texture = self.shoot_textures_down[self.current_shoot_frame]
                    elif self.character_face_direction == UP_FACING:
                        self.texture = self.shoot_textures_up[self.current_shoot_frame]
                    elif self.character_face_direction == RIGHT_FACING:
                        self.texture = self.shoot_textures_right[self.current_shoot_frame]
                    elif self.character_face_direction == LEFT_FACING:
                        self.texture = self.shoot_textures_left[self.current_shoot_frame]

        elif self.is_walking:
            # Walking animation
            self.current_walk_frame += 1
            if self.current_walk_frame > 8 * UPDATES_PER_FRAME:
                self.current_walk_frame = 0
            frame = self.current_walk_frame // UPDATES_PER_FRAME
            direction = self.character_face_direction

            if direction == DOWN_FACING:
                self.texture = self.walk_textures_down[frame]
            if direction == UP_FACING:
                self.texture = self.walk_textures_up[frame]
            if direction == RIGHT_FACING:
                self.texture = self.walk_textures_right[frame]
            if direction == LEFT_FACING:
                self.texture = self.walk_textures_left[frame]

    def shoot(self):
        if not self.is_shooting:
            self.is_shooting = True
            self.current_shoot_frame = 0
            self.shoot_timer = 0
            if self.character_face_direction == DOWN_FACING:
                self.texture = self.shoot_textures_down[self.current_shoot_frame]
            elif self.character_face_direction == UP_FACING:
                self.texture = self.shoot_textures_up[self.current_shoot_frame]
            elif self.character_face_direction == RIGHT_FACING:
                self.texture = self.shoot_textures_right[self.current_shoot_frame]
            elif self.character_face_direction == LEFT_FACING:
                self.texture = self.shoot_textures_left[self.current_shoot_frame]

    def walk(self):
        if not self.is_shooting:  # Only walk if not shooting
            self.is_walking = True

    def stop_walking(self):
        self.is_walking = False
        if not self.is_shooting:
            if self.character_face_direction == DOWN_FACING:
                self.texture = self.idle_textures_down
            elif self.character_face_direction == UP_FACING:
                self.texture = self.idle_textures_up
            elif self.character_face_direction == RIGHT_FACING:
                self.texture = self.idle_textures_right
            elif self.character_face_direction == LEFT_FACING:
                self.texture = self.idle_textures_left

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.character = None
        self.set_update_rate(1/60)
        self.keys_pressed = set()

    def setup(self):
        self.character = Character()
        self.character.center_x = SCREEN_WIDTH // 2
        self.character.center_y = SCREEN_HEIGHT // 2
        self.current_speed = MOVEMENT_SPEED
        self.coin_list = arcade.SpriteList()

        for i in range(COIN_COUNT):
            coin = arcade.Sprite(":resources:images/items/gold_1.png",
                                 scale=0.5)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            self.coin_list.append(coin)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        self.character.draw()
        self.coin_list.draw()

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            self.keys_pressed.add(key)
            self.update_movement()
        if key == arcade.key.SPACE:
            self.character.shoot()

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            self.keys_pressed.discard(key)
            self.update_movement()
        if not self.keys_pressed:
            self.character.stop_walking()

    def on_update(self, delta_time):

        self.character.update()
        self.character.update_animation(delta_time)

        if not self.character.is_shooting and self.keys_pressed:
            self.character.walk()
        else:
            self.character.stop_walking()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.character, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()

    def update_movement(self):
        self.character.change_x = 0
        self.character.change_y = 0

        if arcade.key.W in self.keys_pressed:
            self.character.change_y = self.current_speed
        if arcade.key.S in self.keys_pressed:
            self.character.change_y = -self.current_speed
        if arcade.key.A in self.keys_pressed:
            self.character.change_x = -self.current_speed
        if arcade.key.D in self.keys_pressed:
            self.character.change_x = self.current_speed

def main():
    game = MyGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
