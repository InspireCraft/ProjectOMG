import arcade
import os

from omg.entities.items import Pickupable
from omg.entities.player import Player
from omg.entities.obstacle import Obstacle
from omg.entities.projectile import (
    FireballFactory,
    IceShardFactory,
)
from omg.mechanics.collision import handle_projectile_collisions
from omg.mechanics.physics import PhysicsEngineBoundary
from omg.structural.observer import Observer
from omg.entities.events import PickupRequestEvent, ProjectileShotEvent


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "2D Shooter RPG"

ASSET_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "assets", "images"
)

COIN_IMAGE_PATH = ":resources:images/items/coinGold.png"


class GameWindow(arcade.Window):
    """Main game window."""

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.observer: Observer = None
        self.player: Player = None
        self.obstacles: arcade.SpriteList = None
        self.pickupables: arcade.SpriteList = (
            None  # items that can be pickedup from the ground
        )
        self.projectiles = None
        self.physics_engine = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.icon_scale = 0.1
        self.icon_margin = 10
        self.icon_size = 64

    def setup(self):
        """Reset the game state."""
        self.observer = Observer()
        self.observer.register_handler("projectile_shot", self._on_projectile_shot)
        self.observer.register_handler("pickup_request", self._on_pickup_request)
        self.player = Player(
            name="Hero",
            char_class="Wizard",
            image_file=os.path.join(ASSET_DIR, "characters", "wizard_td2.PNG"),
            scale=0.2,
            initial_angle=0,
        )
        self.player.add_observer(self.observer)

        # Create obstacles
        self.obstacles = arcade.SpriteList()
        self.pickupables = arcade.SpriteList(use_spatial_hash=True)
        self.projectiles = arcade.SpriteList()
        obstacle_image = os.path.join(ASSET_DIR, "obstacles", "obstacle.png")
        obstacle = Obstacle(obstacle_image, 0.2, health=50)
        obstacle.center_x = 400
        obstacle.center_y = 300
        self.obstacles.append(obstacle)

        self.physics_engine = PhysicsEngineBoundary(
            player_sprite=self.player,
            walls=self.obstacles,
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
        )
        # Add projectile types
        self.pickupables.append(
            Pickupable(COIN_IMAGE_PATH, 0.5, FireballFactory, 150, 10)
        )
        self.pickupables.append(
            Pickupable(COIN_IMAGE_PATH, 0.5, IceShardFactory, 250, 20)
        )
        self.pickupables.append(
            Pickupable(COIN_IMAGE_PATH, 0.5, FireballFactory, 250, 120)
        )

    @property
    def skill_icons(self):
        """Define self.skill_icons."""
        # TODO: refactor skill_icons logic if causes a performance bottleneck
        # For example "skill_acquired event" can trigger an update when necessary
        if self.player:
            return [
                arcade.load_texture(projectile_type.image_file)
                for projectile_type in self.player.skills
            ]
        else:
            return None

    def _load_skill_icons(self):
        for projectile_type in self.player.skills:
            icon_texture = arcade.load_texture(projectile_type.image_file)
            self.skill_icons.append(icon_texture)

    def on_draw(self):
        """Drawing code."""
        arcade.start_render()
        self.player.draw()
        self.obstacles.draw()
        self.projectiles.draw()
        self.pickupables.draw()
        self._draw_ui()

    def update(self, delta_time):
        """Main update window."""
        self.player.update(self.mouse_x, self.mouse_y, delta_time)
        self.obstacles.update()
        self.physics_engine.update()
        self.projectiles.update()
        handle_projectile_collisions(self.projectiles, self.obstacles)

    def _on_projectile_shot(self, event: ProjectileShotEvent):
        self.projectiles.append(event.projectile)

    def _on_pickup_request(self, event: PickupRequestEvent):
        """Handles pickup request of an entity.

        Handling logic:
        1) Checks pickupables in the environment with the current posiiton of the entity
           requesting a pickup.
        2) Pickup area is indicated with the hitbox of the event.entity_pickup_sprite
           so collision check can be used.
        3) Out of all the collisions, let the entity pick up the closest object.
        4) Remove the picked up item from the ground.
        """
        collided_sprites: list[Pickupable] = arcade.check_for_collision_with_list(
            event.entity_pickup_sprite, self.pickupables
        )
        if len(collided_sprites) >= 1:
            # Item is at pick up range
            closes_pickupable: Pickupable = arcade.get_closest_sprite(
                event.entity_pickup_sprite, collided_sprites
            )[0]
            item_to_add = collided_sprites[0]
            item_manager = event.entity
            item_manager.add_item(closes_pickupable.item)
            # remove reference to the pickupables list
            item_to_add.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """Key press logic."""
        # Delegate the input
        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """Key release logic."""
        # Delegate the input
        self.player.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """Adds mouse functionality to the game."""
        self.mouse_x = x
        self.mouse_y = y

    def _draw_ui(self):
        for i, icon in enumerate(self.skill_icons):
            x = self.icon_margin + i * (self.icon_size + self.icon_margin)
            y = self.icon_margin
            if i == self.player.skills.get_current_index():
                arcade.draw_rectangle_outline(
                    x + self.icon_size // 2,
                    y + self.icon_size // 2,
                    self.icon_size,
                    self.icon_size,
                    arcade.color.RED,
                    border_width=3,
                )
            arcade.draw_texture_rectangle(
                x + self.icon_size // 2,
                y + self.icon_size // 2,
                self.icon_size,
                self.icon_size,
                icon,
            )


def main():
    """Main application code."""
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
