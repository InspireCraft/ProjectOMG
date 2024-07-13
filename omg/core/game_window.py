import arcade
import os
from entities.player import Player
from entities.obstacle import Obstacle
from mechanics.movement import setup_movement_keys
from mechanics.collision import handle_projectile_collisions

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "2D Shooter RPG"

ROOT_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."),
    "assets",
    "images"
)

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player = None
        self.obstacles = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.on_key_press_handler = None
        self.on_key_release_handler = None

    def setup(self):
        self.player = Player(
            name="Hero",
            char_class="Wizard",
            image_file=os.path.join(ROOT_DIR, "characters", "wizard_td2.PNG"),
            scale=0.2,
            initial_angle=0
        )
        self.on_key_press_handler, self.on_key_release_handler = setup_movement_keys(self.player)
        
        # Create obstacles
        self.obstacles = arcade.SpriteList()
        obstacle_image = os.path.join(ROOT_DIR, "obstacles", "obstacle.png")
        obstacle = Obstacle(obstacle_image, 0.1, health=50)
        obstacle.center_x = 400
        obstacle.center_y = 300
        self.obstacles.append(obstacle)

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.obstacles.draw()

    def update(self, delta_time):
        self.player.update(self.mouse_x, self.mouse_y, self.obstacles, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.check_for_collisions()

    def on_key_press(self, key, modifiers):
        if self.on_key_press_handler:
            self.on_key_press_handler(key, modifiers)
        if key == arcade.key.SPACE:
            self.player.shoot(os.path.join(ROOT_DIR, "skills", "fireball.PNG"), scale=0.05, damage=10, speed=5)

    def on_key_release(self, key, modifiers):
        if self.on_key_release_handler:
            self.on_key_release_handler(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def check_for_collisions(self):
        handle_projectile_collisions(self.player.projectiles, self.obstacles)

def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
