import arcade
from typing import TypeVar, Type
from omg.mechanics import movement
from omg.entities.projectile import ProjectileFactory
from omg.structural.observer import ObservableSprite
from omg.entities.events import PickupRequestEvent, ProjectileShotEvent
from omg.entities.items import CircularBuffer

from omg.mechanics.animations import Animations
import os

MOVEMENT_SPEED_FORWARD = 1
MOVEMENT_SPEED_SIDE = 1
N_SKILLS_MAX = 5
T = TypeVar("T")  # Define a type variable

ASSET_DIR = os.path.join(
    os.path.join(os.path.dirname(__file__), ".."), "assets", "images"
)


class Player(ObservableSprite):
    """Controllable player logic."""

    def __init__(self, name, char_class, char_scale, initial_angle=0):
        super().__init__(scale=char_scale,)
        self.name = name
        self.char_class = char_class
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0
        self.character_face_angle = initial_angle  # Character facing angle
        self.shoot_angle = self.character_face_angle  # Character shooting angle

        # Movement
        self.movement_logic = movement.CompassDirected(
            forward=arcade.key.W,
            backward=arcade.key.S,
            left=arcade.key.A,
            right=arcade.key.D,
        )

        # Animations
        self.animation_logic = Animations(
            slash_key=arcade.key.KEY_1,
            cast_key=arcade.key.KEY_2,
            thrust_key=arcade.key.KEY_3,
            shoot_key=arcade.key.KEY_4,
        )

        # self.movement_logic = movement.MouseDirected(
        #     forward=arcade.key.W,
        #     backward=arcade.key.S,
        #     left=arcade.key.A,
        #     right=arcade.key.D,
        # )
        self.mov_speed_lr = MOVEMENT_SPEED_SIDE
        self.mov_speed_ud = MOVEMENT_SPEED_FORWARD
        # Health
        self.max_health = 100
        self.current_health = 100

        # Mana
        self.max_mana = 100
        self.current_mana = 100
        self.mana_regen_rate = 5  # Mana regenerated per second
        self.mana_regen_cooldown = 0

        # Skills
        self.skills = SkillManager(N_SKILLS_MAX)
        self.item_pickup_radius = 5

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        self.movement_logic.on_key_press(key, modifiers)
        self.animation_logic.on_key_press(key, modifiers)

        if key == arcade.key.SPACE:
            self.shoot()
        elif key == arcade.key.Q:
            self.skills.set_prev()
        elif key == arcade.key.E:
            self.skills.set_next()
        elif key == arcade.key.F:
            self.pickup_skill()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        self.movement_logic.on_key_release(key, modifiers)
        self.animation_logic.on_key_release(key, modifiers)

    def update(self, mouse_x, mouse_y, delta_time):
        """Update the sprite."""
        self.movement_logic.action_finished = self.animation_logic.action_finished
        (self.change_x, self.change_y, self.character_face_angle, self.shoot_angle) = (
            self.movement_logic.calculate_player_state(
                self.center_x,
                self.center_y,
                mouse_x,
                mouse_y,
                self.mov_speed_lr,
                self.mov_speed_ud,
            )
        )
        is_moving = self.movement_logic.move_direction != (0, 0)
        self.texture = self.animation_logic.update(
            delta_time,
            player_change_x=self.change_x,
            player_change_y=self.change_y,
            is_moving=is_moving
        )
        self._regenerate_mana(delta_time)

    def shoot(self):
        """Shoots a projectile and informs the observes with an ProjectileShotEvent."""
        if self.skills.current_size == 0 or self.current_mana < 20:
            return

        self.current_mana -= 20
        selected_skill = self.skills.get_current()
        projectile = selected_skill.create(
            init_px=self.center_x, init_py=self.center_y, angle=self.shoot_angle
        )

        projectile_event = ProjectileShotEvent(projectile)
        self.notify_observers(projectile_event)

    def _regenerate_mana(self, delta_time):
        self.mana_regen_cooldown += delta_time
        if self.mana_regen_cooldown >= 1:
            self.current_mana += self.mana_regen_rate
            if self.current_mana > self.max_mana:
                self.current_mana = self.max_mana
            self.mana_regen_cooldown = 0

    def add_skill(self, skill: Type[ProjectileFactory]):
        """Add skill to the player."""
        self.skills.add_item(skill)

    def pickup_skill(self):
        """Publish a skill pickup request event."""
        # Player will try to pickup the items in a circle around it
        pick_up_sprite = arcade.SpriteCircle(
            radius=self.item_pickup_radius,
            color=arcade.color.RED,
        )  # transparent circular sprite to define the hitbox
        pick_up_sprite.center_x = self.center_x
        pick_up_sprite.center_y = self.center_y
        pick_up_event = PickupRequestEvent(
            self.skills,  # send skill manager
            pick_up_sprite,
        )
        self.notify_observers(pick_up_event)

    def set_movement_keys(self, forward, backward, left, right):
        """Bind keys to the movement logic."""
        self.movement_logic.key_forward = forward
        self.movement_logic.key_backward = backward
        self.movement_logic.key_left = left
        self.movement_logic.key_right = right

    def draw(self):
        """Draw the sprite."""
        super().draw()
        self._draw_health_bar()
        self._draw_mana_bar()

    def _draw_health_bar(self):
        health_bar_width = 50
        health_bar_height = 5
        health_bar_x = self.center_x
        health_bar_y = self.center_y + self.height / 2 + 10
        arcade.draw_rectangle_filled(
            health_bar_x,
            health_bar_y,
            health_bar_width,
            health_bar_height,
            arcade.color.RED,
        )
        current_health_width = health_bar_width * (
            self.current_health / self.max_health
        )
        arcade.draw_rectangle_filled(
            health_bar_x - (health_bar_width - current_health_width) / 2,
            health_bar_y,
            current_health_width,
            health_bar_height,
            arcade.color.GREEN,
        )

    def _draw_mana_bar(self):
        mana_bar_width = 50
        mana_bar_height = 5
        mana_bar_x = self.center_x
        mana_bar_y = (
            self.center_y + self.height / 2 + 2
        )  # Slightly below the health bar
        arcade.draw_rectangle_filled(
            mana_bar_x,
            mana_bar_y,
            mana_bar_width,
            mana_bar_height,
            arcade.color.DARK_BLUE,
        )
        current_mana_width = mana_bar_width * (self.current_mana / self.max_mana)
        arcade.draw_rectangle_filled(
            mana_bar_x - (mana_bar_width - current_mana_width) / 2,
            mana_bar_y,
            current_mana_width,
            mana_bar_height,
            arcade.color.LIGHT_BLUE,
        )


class SkillManager(CircularBuffer[ProjectileFactory]):
    """Manages skills of an entity."""

    pass
