import os.path
from typing import Dict

import arcade
import arcade.key

from omg.entities.events import (
    PickupRequestEvent,
    ProjectileShotEvent,
    PickupButtonKeyChangeRequestEvent,
)
from omg.entities.items import Pickupable
from omg.entities.player import Player
from omg.entities.obstacle import Obstacle
from omg.mechanics.collision import handle_projectile_collisions
from omg.mechanics.physics import PhysicsEngineBoundary
from omg.structural.observer import Observer
from omg.entities.elements import ELEMENTS


ASSET_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "assets", "images"
)

COIN_IMAGE_PATH = ":resources:images/items/coinGold.png"

SCREEN_WIDTH = 800  # Also defines player's POV
SCREEN_HEIGHT = 600  # Also defines player's POV
# player's coordinates are limited to -GAME_MAX_BOUNDS, GAME_MAX_BOUNDS
GAME_MAX_BOUNDS = 10000
SCREEN_TITLE = "2D Shooter RPG"


class GameView(arcade.View):
    """Main game view."""

    def __init__(self, window: arcade.Window = None):
        super().__init__(window)
        self.observer: Observer = None
        self.player: Player = None
        self.scene: arcade.Scene = None
        self.camera_sprite = None
        self.camera_gui = None
        self.skill_slot_1: arcade.Sprite = None  # Skill slot 1
        self.skill_slot_2: arcade.Sprite = None  # Skill slot 2
        self.projectiles: arcade.SpriteList = None
        self.physics_engine = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.icon_scale = 0.1
        self.icon_margin_x = 10
        self.icon_margin_y = 75
        self.icon_size = 64
        self.active_keys: Dict[tuple, bool] = None
        self.collided_pickupables: list[Pickupable]
        self.pickup_button: arcade.Sprite = None
        # self.text_object: arcade.Text = None

    def setup(self):
        """Reset the game state."""
        self.active_keys = {}
        self.flag = True

        self.observer = Observer()
        self.observer.register_handler("projectile_shot", self._on_projectile_shot)
        self.observer.register_handler("pickup_request", self._on_pickup_request)
        self.observer.register_handler(
            "pickup_button_key_change", self._on_player_pickup_button_key_change
        )
        self.player = Player(
            name="Hero",
            char_class="Wizard",
            image_file=os.path.join(ASSET_DIR, "characters", "wizard_td2.PNG"),
            scale=0.2,
            initial_angle=0,
        )
        self.player.add_observer(self.observer)

        # Create scene
        self.scene = arcade.Scene()

        # Add obstacles to the scene
        obstacle_image = os.path.join(ASSET_DIR, "obstacles", "obstacle.png")
        obstacle = Obstacle(obstacle_image, 0.2, health=50)
        obstacle.center_x = 400
        obstacle.center_y = 300
        self.scene.add_sprite_list("Obstacles", use_spatial_hash=True)
        self.scene.add_sprite("Obstacles", obstacle)

        # Add pickupables to the scene
        self.scene.add_sprite_list_after(
            name="Pickupables",
            after="Obstacles",
            use_spatial_hash=True,
        )
        self.scene.add_sprite(
            "Pickupables", Pickupable(COIN_IMAGE_PATH, 0.5, ELEMENTS["FIRE"], 150, 10))
        self.scene.add_sprite(
            "Pickupables", Pickupable(COIN_IMAGE_PATH, 0.5, ELEMENTS["ICE"], 250, 20))
        self.scene.add_sprite(
            "Pickupables", Pickupable(COIN_IMAGE_PATH, 0.5, ELEMENTS["FIRE"], 250, 120))

        self.camera_sprite = arcade.Camera(window=self.window)
        self.camera_gui = arcade.Camera(window=self.window)

        # Create crafted skill slots (UI element)
        self.projectiles = arcade.SpriteList()
        # Skill slot 1
        scale_factor_1 = 0.4
        skill_slot_1_img = os.path.join(ASSET_DIR, "skill_slots_d_f", "D.png")
        self.skill_slot_1 = arcade.Sprite(skill_slot_1_img, scale=scale_factor_1)
        self.skill_slot_1.center_x = self.skill_slot_1.width // 2
        self.skill_slot_1.center_y = self.skill_slot_1.height // 2

        # Skill slot 2
        scale_factor_2 = 0.4
        skill_slot_2_img = os.path.join(ASSET_DIR, "skill_slots_d_f", "F.png")
        self.skill_slot_2 = arcade.Sprite(skill_slot_2_img, scale=scale_factor_2)
        self.skill_slot_2.center_x = (
            self.skill_slot_1.center_x + self.skill_slot_2.width
        )
        self.skill_slot_2.center_y = self.skill_slot_2.height // 2

        # Set up physics engine
        self.physics_engine = PhysicsEngineBoundary(
            player_sprite=self.player,
            walls=self.scene["Obstacles"],
            boundary_left=-GAME_MAX_BOUNDS,
            boundary_right=GAME_MAX_BOUNDS,
            boundary_up=GAME_MAX_BOUNDS,
            boundary_down=-GAME_MAX_BOUNDS,
        )

        # Set up pickup button icon
        self.pickup_button = self._set_pickup_button()  # button background
        self.pickup_key_text_font: int = 24
        self.pickup_button_text_object = arcade.Text(
            chr(self.player.pickup_button_key).capitalize(),
            0,
            0,
            arcade.color.BLACK,
            self.pickup_key_text_font,
        )
        # # Set pickup button text width and height
        height_offset = (self.pickup_key_text_font // 10) * (
            self.pickup_key_text_font % 10 + 1
        )
        self.pickup_button_text_width = self.pickup_button_text_object.content_width
        self.pickup_button_text_height = (
            self.pickup_button_text_object.content_height - height_offset
        )

    def _on_player_pickup_button_key_change(
        self, event: PickupButtonKeyChangeRequestEvent
    ):
        """Update pickup button text when pickup button key changes."""
        self.pickup_button_text_object.text = chr(event.key).capitalize()

    def _set_pickup_button(
        self,
        pickup_button_dir: os.path = os.path.join(
            ASSET_DIR, "pickup_button", "button_background.png"
        ),
        pickup_button_image_scale: float = 0.3,
    ):
        # Set pickup_button
        return arcade.Sprite(
            pickup_button_dir,
            scale=pickup_button_image_scale,
        )

    @property
    def element_icons(self):
        """Define self.element_icons."""
        # TODO: refactor element_icons logic if causes a performance bottleneck
        # For example "element_acquired event" can trigger an update when necessary
        if self.player:
            return [
                arcade.load_texture(element_type["image_file"])
                for element_type in self.player.elements
            ]
        else:
            return None

    def on_draw(self):
        """Drawing code."""
        self.clear()

        # Activate player camera to draw Sprites
        # sprites outside of the player camera are not drawn
        self.camera_sprite.use()
        self.player.draw()
        self.scene.draw()
        self.projectiles.draw()

        # Activate GUI camera before drawing GUI elements
        # This is to ensure GUI elements are drawn w.r.t the window
        self.camera_gui.use()
        self._draw_ui()
        self._draw_pickup_icon()

    def update(self, delta_time):
        """Main update window."""
        self.player.update(self.mouse_x, self.mouse_y, delta_time)
        self.scene.update()
        self.physics_engine.update()
        self.projectiles.update()
        self._check_collision_between_player_and_pickupable()
        handle_projectile_collisions(self.projectiles, self.scene["Obstacles"])
        # Position the camera to the player
        self._center_camera_to_sprite(self.camera_sprite, self.player)

    def _on_projectile_shot(self, event: ProjectileShotEvent):
        self.projectiles.append(event.projectile)

    def _check_collision_between_player_and_pickupable(self):
        self.collided_pickupables: list[Pickupable] = (
            arcade.check_for_collision_with_list(self.player, self.pickupables)
        )

    def _get_pickup_button_coordinates(self, pickupable: Pickupable):
        # Calculate directional vector between player and pickupable
        diff_x: float = pickupable.center_x - self.player.center_x
        diff_y: float = pickupable.center_y - self.player.center_y

        return pickupable.center_x + diff_x, pickupable.center_y + diff_y

    def _draw_pickup_button(self, pickupable: Pickupable) -> arcade.Sprite:
        # Place button image at the mirror reflection of player wrt pickupable
        x, y = self._get_pickup_button_coordinates(pickupable)
        self.pickup_button.center_x = x
        self.pickup_button.center_y = y

        # Draw the button background
        self.pickup_button.draw()

    def _draw_text_on_pickup_button(self):
        # Calculate initial coordinates of text
        self.pickup_button_text_object.x = (
            self.pickup_button.center_x - self.pickup_button_text_width / 2
        )
        self.pickup_button_text_object.y = (
            self.pickup_button.center_y - self.pickup_button_text_height / 2
        )

        # Draw the text on the button background
        self.pickup_button_text_object.draw()

    def _draw_pickup_icon(self):
        if len(self.collided_pickupables) >= 1:
            for pickupable in self.collided_pickupables:
                # Draw button background
                self._draw_pickup_button(pickupable)
                # Draw the text on the button background
                self._draw_text_on_pickup_button()
        else:
            return

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
            event.entity_pickup_sprite, self.scene["Pickupables"]
        )
        if len(collided_sprites) >= 1:
            # Item is at pick up range
            closes_pickupable: Pickupable = arcade.get_closest_sprite(
                event.entity_pickup_sprite, self.collided_pickupables
            )[0]
            item_to_add = self.collided_pickupables[0]
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
        for key_tuple, is_active in self.active_keys.items():
            # NOTE: keys which are also modifiers are pressed and released
            # differently. CTRL is (65507, 18) when pressed, (65507, 16) when
            # released. A more detailed check for those keys might be necessary
            # in future if those are actively used.
            if is_active:
                self.on_key_release(*key_tuple)
        self.active_keys = {}  # reset the dictionary

    def _draw_ui(self):
        # Draw picked up elements to top left corner
        for i, icon in enumerate(self.element_icons):
            x = self.icon_margin_x + i * (self.icon_size + self.icon_margin_x)
            y = self.window.height - self.icon_margin_y
            if i == self.player.elements.get_current_index():
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

        # Draw combined skill icons
        if self.player.crafted_skill_slots[0] is not None:
            scale_factor_crafted_skill_1 = 0.3
            skill_1_img = os.path.join(
                ASSET_DIR, "skills", f"{self.player.crafted_skill_slots[0]}.png"
            )
            skill_1 = arcade.Sprite(skill_1_img, scale=scale_factor_crafted_skill_1)
            skill_1.center_x = skill_1.width // 2
            skill_1.center_y = skill_1.height // 2
            skill_1.draw()

        if self.player.crafted_skill_slots[1] is not None:
            scale_factor_crafted_skill_2 = 0.3
            skill_2_img = os.path.join(
                ASSET_DIR, "skills", f"{self.player.crafted_skill_slots[1]}.png"
            )
            skill_2 = arcade.Sprite(skill_2_img, scale=scale_factor_crafted_skill_2)
            skill_2.center_x = skill_2.width // 2 + skill_2.width
            skill_2.center_y = skill_2.height // 2
            skill_2.draw()

        # Draw usable skill slots to bottom left corner
        self.skill_slot_1.draw()
        self.skill_slot_2.draw()

    @staticmethod
    def _center_camera_to_sprite(camera: arcade.Camera, sprite: arcade.Sprite):
        screen_center_x = sprite.center_x - (camera.viewport_width / 2)
        screen_center_y = sprite.center_y - (camera.viewport_height / 2)
        player_centered = (screen_center_x, screen_center_y)

        camera.move_to(player_centered)


class PauseView(arcade.View):
    """Pause screen of the game."""

    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self._view_to_draw: arcade.View = None

    def update_view_to_draw(self, new_view: arcade.View):
        """Update the View to be drawn in the pause state."""
        self._view_to_draw = new_view

    def on_draw(self):
        """Draw the game as is and the pause view extras."""
        self.clear()
        if self._view_to_draw:
            self._view_to_draw.on_draw()

        # Draw the Pause text on the given View as overlay
        arcade.draw_text("PAUSED", self.window.width / 2, self.window.height / 2 + 50,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         self.window.width / 2,
                         self.window.height / 2,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Q to quit",
                         self.window.width / 2,
                         self.window.height / 2 - 30,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")

    def on_key_release(self, key, modifiers):
        """Key release logic."""
        if key == arcade.key.Q:
            arcade.exit()
