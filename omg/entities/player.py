from typing import Dict, TypeVar, Union

import arcade
import arcade.key

from omg.entities.events import (
    PickupRequestEvent,
    ProjectileShotEvent,
    PickupButtonKeyChangeRequestEvent,
)
from omg.entities.items import CircularBuffer
from omg.entities.projectile import SkillFactory, crafted_skill_dictionary
from omg.mechanics import movement
from omg.structural.observer import ObservableSprite


from omg.mechanics.animations import Animations
import os

MOVEMENT_SPEED_VERTICAL = 5
MOVEMENT_SPEED_HORIZONTAL = 5
N_ELEMENTS_MAX = 5
T = TypeVar("T")  # Define a type variable


class Player(ObservableSprite):
    """Controllable player logic."""

    def __init__(
        self,
        name: str,
        animation_file: str,
        scale,
        initial_angle=0
    ):
        """Initialize Player instance."""
        # TODO: Fix super().__init__(animation_idle)
        animation_idle = str(os.path.join(animation_file, "idle_down0.png"))
        super().__init__(animation_idle, scale)

        self.name = name
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0
        self.character_face_angle = initial_angle  # Character facing angle
        self.shoot_angle = self.character_face_angle  # Character shooting angle

        # Initialize pickup button key
        self._button_key_observer = []
        self._pickup_button_key = arcade.key.F

        # Initialize item pickup sprite
        self.item_pickup_radius = 50
        self._pick_up_sprite = arcade.SpriteCircle(
            radius=self.item_pickup_radius,
            color=arcade.color.RED,
        )  # transparent circular sprite to define the hitbox

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

        self.mov_speed_lr = MOVEMENT_SPEED_HORIZONTAL
        self.mov_speed_ud = MOVEMENT_SPEED_VERTICAL

        # Health
        self.max_health = 100
        self.current_health = 100

        # Mana
        self.max_mana = 100
        self.current_mana = 100
        self.mana_regen_rate = 5  # Mana regenerated per second
        self.mana_regen_cooldown = 0

        # Skills
        self.elements = ElementManager(N_ELEMENTS_MAX)

        # Initialize an empty element_buffer
        self.to_be_combined_element_buffer: list[str] = []
        # Initialize crafted skill slots as None
        self.crafted_skill_slots: list[str] = [None, None]
        self.crafted_skill = SkillFactory()

    @property
    def pickup_button_key(self):
        """Define self.player.pickup_button_key."""
        return self._pickup_button_key

    @pickup_button_key.setter
    def pickup_button_key(self, new_value):
        self._pickup_button_key = new_value
        event = PickupButtonKeyChangeRequestEvent(new_value)
        self.notify_observers(event)

    @property
    def pickup_sprite(self):
        """Define self.player.pickup_sprite."""
        return self._pick_up_sprite

    @pickup_sprite.getter
    def pickup_sprite(self):
        self._pick_up_sprite.center_x = self.center_x
        self._pick_up_sprite.center_y = self.center_y
        return self._pick_up_sprite

    def on_key_press(self, key, modifiers):
        """Call whenever a key is pressed."""
        self.movement_logic.on_key_press(key, modifiers)
        self.animation_logic.on_key_press(key, modifiers)

        if key == arcade.key.H:
            skill_name = self.crafted_skill_slots[0]
            self.shoot(skill_name)
        elif key == arcade.key.J:
            skill_name = self.crafted_skill_slots[1]
            self.shoot(skill_name)
        elif key == arcade.key.SPACE:
            current_element = self.elements.get_current()
            if current_element:
                self.to_be_combined_element_buffer.append(current_element["name"])
        elif key == arcade.key.Q:
            self.elements.set_prev()
        elif key == arcade.key.E:
            self.elements.set_next()
        elif key == self.pickup_button_key:
            self.pickup_element()

    def on_key_release(self, key, modifiers):
        """Call when the user releases a key."""
        self.movement_logic.on_key_release(key, modifiers)
        self.animation_logic.on_key_release(key, modifiers)

    def _update_crafted_skill_slots(self, new_skill: str):
        """Update crafted skill slots after combining elements."""
        self.crafted_skill_slots[1] = self.crafted_skill_slots[0]
        self.crafted_skill_slots[0] = new_skill

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

        # Update combined elements
        if len(self.to_be_combined_element_buffer) == 2:
            # Get the name of the skill after combining elements
            new_skill = "".join(self.to_be_combined_element_buffer[::])

            # Update crafted skill slots
            self._update_crafted_skill_slots(new_skill)

            # Empty the element buffer
            self.to_be_combined_element_buffer = []

    def shoot(self, skill_name: str):
        """Shoot a projectile and inform the observers."""
        skill_attributes: dict = crafted_skill_dictionary.get(skill_name, None)
        if skill_attributes:
            self.crafted_skill.set_skill_attributes(skill_attributes)
        else:
            return

        mana_cost = self.crafted_skill.mana_cost
        if self.current_mana < mana_cost:
            return

        self.current_mana -= mana_cost
        projectile = self.crafted_skill.create(
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

    def pickup_element(self):
        """Publish a skill pickup request event."""
        pick_up_event = PickupRequestEvent(self.elements, self.pickup_sprite)
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


class ElementManager(CircularBuffer[Dict[str, Union[str, float]]]):
    """Manages skills of an entity."""

    pass
