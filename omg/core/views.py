import os.path
from typing import Dict
from pyglet.graphics import Batch

import arcade
import arcade.key
from arcade.experimental import Shadertoy

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


# TODO: Manage assets in a more generic way
ASSET_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "assets", "images"
)
COIN_IMAGE_PATH = ":resources:images/items/coinGold.png"
ARCHER_PATH = str(os.path.join(ASSET_DIR, "characters", "demo_archer", "sprites"))

SCREEN_WIDTH = 800  # Also defines player's POV
SCREEN_HEIGHT = 600  # Also defines player's POV
# player's coordinates are limited to -GAME_MAX_BOUNDS, GAME_MAX_BOUNDS
GAME_MAX_BOUNDS = 10000
SCREEN_TITLE = "2D Shooter RPG"

SHADER_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "shaders"
)
SHADER_LIGHT_SIZE = 300


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
        self.physics_engine = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.icon_scale = 0.1
        self.icon_margin_x = 10
        self.icon_margin_y = 75
        self.icon_size = 64
        self.active_keys: Dict[tuple, bool] = None
        self.pickup_button: arcade.Sprite = None

        # Framebuffers for shaders that enable raycasting
        # TODO: move logic to a separate class,
        # reference:https://api.arcade.academy/en/stable/tutorials/raycasting/index.html?
        self.shadertoy = None
        self.channel0 = None  # first framebuffer
        self.channel1 = None  # second framebuffer
        self._load_shader()
        self.raycasting_mode: bool = False

        # Debug text objects
        self._debug_text_batch = Batch()
        self._debug_text_objects = {
            'mouse_pos': arcade.Text(
                "Mouse",
                101, 101, arcade.color.WHITE, 20, batch=self._debug_text_batch
            ),
            'player_pos': arcade.Text(
                "Player",
                101, 135, arcade.color.WHITE, 20, batch=self._debug_text_batch
            ),
            'debug_label': arcade.Text(
                "Debug mode",
                self.window.width - 250, self.window.height - 50,
                arcade.color.RED, 20, batch=self._debug_text_batch
            )
        }

        # Debug state
        self.debug_mode: bool = False

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
            animation_file=ARCHER_PATH,
            scale=1.0,
            initial_angle=0,
        )
        self.player.add_observer(self.observer)

        # Create scene
        self.scene = arcade.Scene()

        self._collided_pickupables: list[Pickupable] = arcade.SpriteList()

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
            "Pickupables", Pickupable(COIN_IMAGE_PATH, 0.5, ELEMENTS["FIRE"], 150, 10)
        )
        self.scene.add_sprite(
            "Pickupables", Pickupable(COIN_IMAGE_PATH, 0.5, ELEMENTS["ICE"], 420, 120))
        self.scene.add_sprite(
            "Pickupables", Pickupable(COIN_IMAGE_PATH, 0.5, ELEMENTS["FIRE"], 250, 120)
        )
        # Add projectiles to the scene
        self.scene.add_sprite_list("Projectiles", use_spatial_hash=False)
        self.camera_sprite = arcade.camera.Camera2D(window=self.window)
        self.camera_gui = arcade.camera.Camera2D(window=self.window)

        # GUI elements, these are not added to the scene
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

    def _load_shader(self):

        # Create the shader toy
        raycasting_shader_path = os.path.join(SHADER_DIR, "raycasting.glsl")
        window_size = self.window.get_size()
        self.shadertoy = Shadertoy.create_from_file(window_size, raycasting_shader_path)

        # Create the channels 0 and 1 frame buffers.
        # Make the buffer the size of the window, with 4 channels (RGBA)
        self.channel0 = self.shadertoy.ctx.framebuffer(
            color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)]
        )
        self.channel1 = self.shadertoy.ctx.framebuffer(
            color_attachments=[self.shadertoy.ctx.texture(window_size, components=4)]
        )

        # Assign the frame buffers to the channels
        self.shadertoy.channel_0 = self.channel0.color_attachments[0]
        self.shadertoy.channel_1 = self.channel1.color_attachments[0]

    @property
    def element_icons(self):
        """Define self.element_icons."""
        # TODO: refactor element_icons logic if causes a performance bottleneck
        # For example "element_acquired event" can trigger an update when necessary
        if self.player:
            return [
                arcade.texture.default_texture_cache.load_or_get_texture(
                    element_type["image_file"]
                )
                for element_type in self.player.elements
            ]
        else:
            return None

    def on_draw(self):
        """Drawing code."""
        # Activate player camera to draw Sprites
        # sprites outside of the player camera are not drawn
        self.camera_sprite.use()
        # Raycasting part
        if self.raycasting_mode:
            # TODO: encapsulate this logic in a separate class

            # Raycasting is achieved by using Shaders. Shaders are programs that
            # run on the GPU and the result is rendered to the screen. The
            # shader is run for each pixel on the screen. The shader can read
            # from textures (framebuffers) and write to the screen. The shader
            # can also write to textures (framebuffers).

            # Define which sprites are sources of shadows, which are affected by
            # light etc
            shadow_sources = ["Obstacles",]
            affected_by_light = ["Projectiles", "Pickupables"]
            not_affected_by_light = [
                key for key in self.scene._name_mapping.keys()
                if key not in affected_by_light
            ]

            # Select the channel 0 frame buffer to draw on
            # Specify the targets that create a shadow
            # (draw them on channel0 framebuffer)
            self.channel0.use()
            self.channel0.clear()
            self.scene.draw(shadow_sources)

            # Calculate the light position. We have to subtract the camera position
            # from the player position to get screen-relative coordinates.
            left, bottom = self.camera_sprite.bottom_left
            p = (
                self.player.position[0] - left,
                self.player.position[1] - bottom
            )

            # Set the uniform data (data accessible in the shader)
            self.shadertoy.program['lightPosition'] = p
            self.shadertoy.program['lightSize'] = SHADER_LIGHT_SIZE

            # Select the channel 1 frame buffer to draw on
            # Specify the targets that is affected by shadows (or light)
            # Draw them on channel1 framebuffer
            self.channel1.use()
            self.channel1.clear()
            self.scene.draw(affected_by_light)
            # Select this window to draw on
            self.window.use()
            # Clear to background color
            self.clear()

            # Run the shader and render to the window
            self.shadertoy.render()
            self.scene.draw(not_affected_by_light)
            self.player.draw()
        else:
            # Default logic without raycasting
            self.clear()
            self.scene.draw()
            self.player.draw()

        if self.debug_mode:
            self.scene.draw_hit_boxes(arcade.color.RED)
            self.player.draw_hit_box(arcade.color.RED)
            self.player.pickup_sprite.draw_hit_box(arcade.color.RED)
        # Activate GUI camera before drawing GUI elements
        # This is to ensure GUI elements are drawn w.r.t the window
        self.camera_gui.use()
        self._draw_ui()
        self._draw_pickup_icon()
        if self.debug_mode:
            self._draw_debug_info()

    def on_update(self, delta_time):
        """Main update window.

        The main update is divided into two parts:

        First is to update the Sprites individually without taking any
        interactions with the other Sprites into account.

        The second part is to update the Sprites which have interactions with
        each other.
        """
        # Scene updates sprites individually
        self.scene.update(delta_time)
        # Mouse is tracked in the window coordinates, but the player logic needs
        # the mouse in the camera coordinates. Thus, the mouse position relative
        # to the window should be mapped to the mouse coordinates relative to
        # the camera before passing it to the player.
        bottomleft_coord = self._find_bottomleft_coord_of_camera(self.camera_sprite)
        mouse_in_camera_x = self.mouse_x + bottomleft_coord[0]
        mouse_in_camera_y = self.mouse_y + bottomleft_coord[1]
        self.player.update(mouse_in_camera_x, mouse_in_camera_y, delta_time)

        # Update behaviour between the player and the pickupables
        self._collided_pickupables = arcade.check_for_collision_with_list(
            self.player.pickup_sprite, self.scene["Pickupables"]
        )

        # Update behaviour between the player and the obstacles
        self.physics_engine.update()

        # Update behaviour between the projectiles and the obstacles
        handle_projectile_collisions(self.scene["Projectiles"], self.scene["Obstacles"])

        # Update behaviour between the camera and the player, positions the
        # camera to the player
        self._center_camera_to_sprite(self.camera_sprite, self.player)

    def on_resize(self, width, height):
        """Resize the window. Handles the resizing of the subcomponents."""
        val = super().on_resize(width, height)
        self.shadertoy.resize((width, height))
        self.camera_sprite.match_window()
        self.camera_gui.match_window()
        return val

    def _on_projectile_shot(self, event: ProjectileShotEvent):
        self.scene["Projectiles"].append(event.projectile)

    def _get_pickup_button_coordinates(self, pickupable: Pickupable):
        # Calculate directional vector between player and pickupable
        diff_x: float = pickupable.center_x - self.player.center_x
        diff_y: float = pickupable.center_y - self.player.center_y

        # This is a GUI element, so we need to convert the coordinates from
        # camera coordinates to window coordinates
        window_bottomleft = self._find_bottomleft_coord_of_camera(self.camera_sprite)
        x_window_coord = pickupable.center_x + diff_x - window_bottomleft[0]
        y_window_coord = pickupable.center_y + diff_y - window_bottomleft[1]

        return x_window_coord, y_window_coord

    def _draw_pickup_button(self, pickupable: Pickupable) -> arcade.Sprite:
        # Place button image at the mirror reflection of player wrt pickupable
        x_window_coord, y_window_coord = self._get_pickup_button_coordinates(pickupable)
        self.pickup_button.center_x = x_window_coord
        self.pickup_button.center_y = y_window_coord

        # Draw the button background
        arcade.draw_sprite(self.pickup_button)

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
        if len(self._collided_pickupables) >= 1:
            for pickupable in self._collided_pickupables:
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
                event.entity_pickup_sprite, collided_sprites
            )[0]
            item_to_add = closes_pickupable.item
            item_manager = event.entity
            item_manager.add_item(item_to_add)
            # remove reference to the pickupables list
            closes_pickupable.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        """Key press logic."""
        self.active_keys[(key, modifiers)] = True  # mark the key as `active`
        # Delegate the input
        self.player.on_key_press(key, modifiers)

        # Debug mode toggle
        if key == arcade.key.F1:
            self.debug_mode = not self.debug_mode

        # Raycasting toggle
        if key == arcade.key.F2:
            self.raycasting_mode = not self.raycasting_mode

    def on_key_release(self, key, modifiers):
        """Key release logic."""
        self.active_keys[(key, modifiers)] = False  # mark the key as `not active`
        # Delegate the input
        self.player.on_key_release(key, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        """Adds mouse functionality to the game.

        x: Current mouse x-position in the window ( 0<x<self.window.width).
        y: Current mouse x-position in the window ( 0<x<self.window.height).

        """
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
            rectangle = arcade.rect.XYWH(
                x + self.icon_size // 2,
                y + self.icon_size // 2,
                self.icon_size,
                self.icon_size
            )
            if i == self.player.elements.get_current_index():
                arcade.draw_rect_outline(
                    rectangle,
                    arcade.color.RED,
                    border_width=3
                )
            arcade.draw_texture_rect(
                texture=icon,
                rect=rectangle,
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
            arcade.draw_sprite(skill_1)

        if self.player.crafted_skill_slots[1] is not None:
            scale_factor_crafted_skill_2 = 0.3
            skill_2_img = os.path.join(
                ASSET_DIR, "skills", f"{self.player.crafted_skill_slots[1]}.png"
            )
            skill_2 = arcade.Sprite(skill_2_img, scale=scale_factor_crafted_skill_2)
            skill_2.center_x = skill_2.width // 2 + skill_2.width
            skill_2.center_y = skill_2.height // 2
            arcade.draw_sprite(skill_2)

        # Draw usable skill slots to bottom left corner
        arcade.draw_sprite(self.skill_slot_1)
        arcade.draw_sprite(self.skill_slot_2)

    def _draw_debug_info(self):
        """Print debug text information on the screen."""
        if self.player:
            pass
            # Update the text content for position values
            self._debug_text_objects['mouse_pos'].text = (
                f"Mouse: ({self.mouse_x}, {self.mouse_y})"
            )
            self._debug_text_objects['player_pos'].text = (
                f"Player: ({self.player.center_x:.1f}, {self.player.center_y:.1f})"
            )

        # Fastest way to draw text objects
        self._debug_text_batch.draw()

    @staticmethod
    def _center_camera_to_sprite(camera: arcade.camera.Camera2D, sprite: arcade.Sprite):
        """Scroll the window to the player."""
        camera.position = (sprite.center_x, sprite.center_y)

    @staticmethod
    def _find_bottomleft_coord_of_camera(camera: arcade.camera.Camera2D):
        """Find the bottom left corner of the window in camera coordinates.

        This is used to calculate the position of objects defined relative to
        the window. It assumes that the camera is centered on the player, hence
        the camera position points to the middle of the window.
        """
        return (
            camera.position[0] - (camera.viewport_width / 2),
            camera.position[1] - (camera.viewport_height / 2)
        )


class PauseView(arcade.View):
    """Pause screen of the game."""

    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self._view_to_draw: arcade.View = None
        self.camera = arcade.camera.Camera2D(window=self.window)
        self.camera.use()
        self._pause_view_text_batch = Batch()
        self._text_offsets = {
            'paused': 50,
            'esc': 0,
            'Q': -30,
        }

        self._pause_view_texts = {
            'paused': arcade.Text(
                "PAUSED",
                self.window.width / 2,
                self.window.height / 2 + self._text_offsets['paused'],
                arcade.color.WHITE,
                font_size=50,
                anchor_x="center",
                batch=self._pause_view_text_batch,
            ),
            'esc': arcade.Text(
                "Press Esc. to return",
                self.window.width / 2,
                self.window.height / 2 + self._text_offsets['esc'],
                arcade.color.WHITE,
                font_size=20,
                anchor_x="center",
                batch=self._pause_view_text_batch,
            ),
            'Q': arcade.Text(
                "Press Q to quit",
                self.window.width / 2,
                self.window.height / 2 + self._text_offsets['Q'],
                arcade.color.WHITE,
                font_size=20,
                anchor_x="center",
                batch=self._pause_view_text_batch,
            )
        }

    def on_resize(self, width, height):
        """Resize the window. Handles the resizing of the subcomponents."""
        # TODO: text position updates correctly but is not drawn correctly
        super().on_resize(width, height)
        self.camera.match_window()
        self._view_to_draw.on_resize(width, height)
        center_x = self.window.width / 2
        center_y = self.window.height / 2
        for key, text in self._pause_view_texts.items():
            text.position = (center_x, center_y + self._text_offsets[key])

    def update_view_to_draw(self, new_view: arcade.View):
        """Update the View to be drawn in the pause state."""
        self._view_to_draw = new_view

    def on_draw(self):
        """Draw the game as is and the pause view extras."""
        self.camera.use()
        self.clear()
        if self._view_to_draw:
            self._view_to_draw.on_draw()
        self._pause_view_text_batch.draw()

    def on_key_release(self, key, modifiers):
        """Key release logic."""
        if key == arcade.key.Q:
            arcade.exit()
