import os.path
from typing import Dict

import arcade

from omg.entities.events import PickupRequestEvent, ProjectileShotEvent
from omg.entities.items import Pickupable
from omg.entities.player import Player
from omg.entities.projectile import (
    FireballFactory,
    IceShardFactory,
)
from omg.entities.obstacle import Obstacle
from omg.mechanics.collision import handle_projectile_collisions
from omg.mechanics.physics import PhysicsEngineBoundary
from omg.structural.observer import Observer


ASSET_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "assets", "images"
)

COIN_IMAGE_PATH = ":resources:images/items/coinGold.png"

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "2D Shooter RPG"


class GameView(arcade.View):
    """Main game view."""

    def __init__(self, window: arcade.Window = None):
        super().__init__(window)
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
        self.active_keys: Dict[tuple, bool] = None

    def setup(self):
        """Reset the game state."""
        self.active_keys = {}
        self.flag = True

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
        self.active_keys[(key, modifiers)] = True  # mark the key as `active`
        # Delegate the input
        self.player.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        """Key release logic."""
        self.active_keys[(key, modifiers)] = False  # mark the key as `not active`
        # Delegate the input
        self.player.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """Adds mouse functionality to the game."""
        self.mouse_x = x
        self.mouse_y = y

    def on_hide_view(self):
        """Hide view callback function.

        Callback logic: 1 - Some of the pressed keys might not have their
        corresponding `key_release` logic called when the view has been changed.
        Those callbacks are called before the view is changed.
        """
        for (key_tuple, is_active) in self.active_keys.items():
            # NOTE: keys which are also modifiers are pressed and released
            # differently. CTRL is (65507, 18) when pressed, (65507, 16) when
            # released. A more detailed check for those keys might be necessary
            # in future if those are actively used.
            if is_active:
                self.on_key_release(*key_tuple)
        self.active_keys = {}  # reset the dictionary

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


class PauseView(arcade.View):
    """Pause screen of the game."""

    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self._view_to_draw: arcade.View = None

    def update_view_to_draw(self, new_view):
        """Update the View to be drawn in the pause state."""
        self._view_to_draw = new_view

    def on_draw(self):
        """Draw the game as is and the pause view extras."""
        self.clear()
        if self._view_to_draw:
            self._view_to_draw.on_draw()

        # Draw the Pause text on the given View as overlay
        arcade.draw_text("PAUSED", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Q to quit",
                         SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 30,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")

    def on_key_release(self, key, modifiers):
        """Key release logic."""
        if key == arcade.key.Q:
            arcade.exit()
