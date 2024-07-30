import arcade
import os
from entities.player import Player
from entities.obstacle import Obstacle
from mechanics.collision import handle_projectile_collisions
from mechanics.physics import PhysicsEngineBoundary
from structural.observer import Observer

from entities.projectile import FireballFactory, IceShardFactory, Projectile


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "2D Shooter RPG"

ASSET_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."),
    "assets",
    "images"
)


class GameWindowMeta(type(arcade.Window), type(Observer)):
    '''Define new metaclass for GameWindow and Observer multiple inheritence.'''
    pass


class GameWindow(arcade.Window, Observer, metaclass=GameWindowMeta):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.player: Player = None
        self.obstacles: arcade.SpriteList = None
        self.projectiles = None
        self.physics_engine = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.skill_icons = []
        self.icon_scale = 0.1
        self.icon_margin = 10
        self.icon_size = 64

    def setup(self):
        self.player = Player(
            name="Hero",
            char_class="Wizard",
            image_file=os.path.join(ASSET_DIR, "characters", "wizard_td2.PNG"),
            scale=0.2,
            initial_angle=0
        )
        self.player.add_observer(self)

        # Create obstacles
        self.obstacles = arcade.SpriteList()
        self.projectiles = arcade.SpriteList()
        obstacle_image = os.path.join(ASSET_DIR, "obstacles", "obstacle.png")
        obstacle = Obstacle(obstacle_image, 0.2, health=50)
        obstacle.center_x = 400
        obstacle.center_y = 300
        self.obstacles.append(obstacle)

        self.physics_engine = PhysicsEngineBoundary(
            player_sprite=self.player, walls=self.obstacles,
            screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT
        )
        # Add projectile types
        self.player.add_projectile(FireballFactory)
        self.player.add_projectile(IceShardFactory)

        # Load skill icons
        self.load_skill_icons()

    def on_event(self, event_type: str, *args, **kwargs):
        """Handle the event notifications."""
        if event_type == 'projectile_shot':
            projectile: Projectile = args[0]
            self.projectiles.append(projectile)

    def load_skill_icons(self):
        for projectile_type in self.player.projectile_types:
            icon_texture = arcade.load_texture(projectile_type.image_file)
            self.skill_icons.append(icon_texture)

    def on_draw(self):
        arcade.start_render()
        self.player.draw()
        self.obstacles.draw()
        self.projectiles.draw()
        self.draw_ui()

    def update(self, delta_time):
        self.player.update(
            self.mouse_x, self.mouse_y, delta_time)
        self.obstacles.update()
        self.physics_engine.update()
        self.projectiles.update()
        handle_projectile_collisions(self.projectiles, self.obstacles)

    def on_key_press(self, key, modifiers):
        # Delegate the input
        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        # Delegate the input
        self.player.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def draw_ui(self):
        for i, icon in enumerate(self.skill_icons):
            x = self.icon_margin + i * (self.icon_size + self.icon_margin)
            y = self.icon_margin
            if i == self.player.current_projectile_index:
                arcade.draw_rectangle_outline(
                    x + self.icon_size // 2,
                    y + self.icon_size // 2,
                    self.icon_size,
                    self.icon_size,
                    arcade.color.RED,
                    border_width=3
                )
            arcade.draw_texture_rectangle(
                x + self.icon_size // 2,
                y + self.icon_size // 2,
                self.icon_size,
                self.icon_size,
                icon
            )



def main():
    window = GameWindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
