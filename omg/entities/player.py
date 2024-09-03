import arcade
from typing import TypeVar, Type

import arcade.key
from omg.mechanics import movement
from omg.entities.projectile import ProjectileFactory
from omg.entities.projectile import COMBINED_ELEMENT_DICTIONARY
from omg.structural.observer import ObservableSprite
from omg.entities.events import PickupRequestEvent, ProjectileShotEvent
from omg.entities.items import CircularBuffer
from omg.entities.projectile import CraftingSkillFactory

MOVEMENT_SPEED_FORWARD = 1
MOVEMENT_SPEED_SIDE = 1
N_SKILLS_MAX = 5
T = TypeVar("T")  # Define a type variable


class Player(ObservableSprite):
    """Controllable player logic."""

    def __init__(self, name, char_class, image_file, scale, initial_angle=0):
        """Initialize Player instance."""
        super().__init__(image_file, scale)
        self.name = name
        self.char_class = char_class
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0
        self.angle = initial_angle  # Set initial angle here

        # Movement
        self.movement_logic = movement.CompassDirected(
            forward=arcade.key.W,
            backward=arcade.key.S,
            left=arcade.key.A,
            right=arcade.key.D,
        )
        self.movement_logic = movement.MouseDirected(
            forward=arcade.key.W,
            backward=arcade.key.S,
            left=arcade.key.A,
            right=arcade.key.D,
        )
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
        self.element = SkillManager(N_SKILLS_MAX)
        self.item_pickup_radius = 5
        # Initialize an empty element_buffer
        self.to_be_combined_element_buffer: list[str] = []
        # Initialize crafted skill slots as None
        self.crafted_skill_slots: list[str] = [None, None]

    def on_key_press(self, key, modifiers):
        """Call whenever a key is pressed."""
        self.movement_logic.on_key_press(key, modifiers)

        if key == arcade.key.H:
            skill_name = self.crafted_skill_slots[0]
            self.shoot(skill_name)
        elif key == arcade.key.J:
            skill_name = self.crafted_skill_slots[1]
            self.shoot(skill_name)
        elif key == arcade.key.SPACE:
            self.to_be_combined_element_buffer.append(
                self.element.get_current()["name"]
            )
        elif key == arcade.key.Q:
            self.element.set_prev()
        elif key == arcade.key.E:
            self.element.set_next()
        elif key == arcade.key.F:
            self.pickup_element()

    def on_key_release(self, key, modifiers):
        """Call when the user releases a key."""
        self.movement_logic.on_key_release(key, modifiers)

    def _update_crafted_skill_slots(self, new_skill: str):
        """Update crafted skill slots after combining elements."""
        self.crafted_skill_slots[1] = self.crafted_skill_slots[0]
        self.crafted_skill_slots[0] = new_skill

    def update(self, mouse_x, mouse_y, delta_time):
        """Update the sprite."""
        (self.change_x, self.change_y, self.angle) = (
            self.movement_logic.calculate_player_state(
                self.center_x,
                self.center_y,
                mouse_x,
                mouse_y,
                self.mov_speed_lr,
                self.mov_speed_ud,
            )
        )
        self._regenerate_mana(delta_time)

        # Update combined elements
        if len(self.to_be_combined_element_buffer) == 2:
            # Get the name of the skill after combining elements
            new_skill = "".join(self.to_be_combined_element_buffer[::])

            # Remove "ElementFactory" from the element name
            new_skill = new_skill.replace("ElementFactory", "")

            # Update crafted skill slots
            self._update_crafted_skill_slots(new_skill)

            # Empty the element cash
            self.to_be_combined_element_buffer = []

    def shoot(self, skill_name: str):
        """Shoot a projectile and inform the observers."""
        # mana_cost = COMBINED_ELEMENT_DICTIONARY[skill_name].mana_cost
        crafted_skill = CraftingSkillFactory()
        crafted_skill._set_skill_attributes(skill_name)

        mana_cost = crafted_skill.mana_cost
        if skill_name is None or self.current_mana < mana_cost:
            return

        self.current_mana -= mana_cost
        # selected_skill = COMBINED_ELEMENT_DICTIONARY[skill_name]
        # projectile = selected_skill.create(
        projectile = crafted_skill.create(
            init_px=self.center_x, init_py=self.center_y, angle=self.angle
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

    def add_skill(self, element: Type[ProjectileFactory]):
        """Add skill to the player."""
        self.element.add_item(element)

    def pickup_element(self):
        """Publish a skill pickup request event."""
        # Player will try to pickup the items in a circle around it
        pick_up_sprite = arcade.SpriteCircle(
            radius=self.item_pickup_radius,
            color=arcade.color.RED,
        )  # transparent circular sprite to define the hitbox
        pick_up_sprite.center_x = self.center_x
        pick_up_sprite.center_y = self.center_y
        pick_up_event = PickupRequestEvent(
            self.element,  # send skill manager
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
        current_mana_width = mana_bar_width * (
            self.current_mana / self.max_mana
        )
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
