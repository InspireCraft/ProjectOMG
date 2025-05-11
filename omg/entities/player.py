from typing import Dict, TypeVar, Union
import math

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
from omg.entities.weapons import Weapons

MOVEMENT_SPEED_VERTICAL = 5
MOVEMENT_SPEED_HORIZONTAL = 5
N_ELEMENTS_MAX = 5
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
        # self.movement_logic = movement.MouseDirected(
        #     forward=arcade.key.W,
        #     backward=arcade.key.S,
        #     left=arcade.key.A,
        #     right=arcade.key.D,
        # )
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

        # Melee attack
        self._weapon: Weapons = None
        self._weapon_damagezone_sprites: arcade.SpriteList = None
        self._melee_dmg = 10  # base_melee_dmg value of player
        self._melee_atk_speed = 1  # number of seconds between attacks
        self._melee_range = 55  # attack range for melee attacks
        self._stab_counter = 0

        # self._weapon_sprite = self._summon_weapon_sprite()
    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, value):
        self._weapon = value
        self._weapon_damagezone_sprites = arcade.SpriteList()
        for _ in range(self.weapon.num_of_dmg_zones):
            self._weapon_damagezone_sprites.append(
                arcade.SpriteCircle(radius=13, color=arcade.color.RED)
            )

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
    def weapon_damagezone_sprites(self):
        return self._weapon_damagezone_sprites

    @weapon_damagezone_sprites.getter
    def weapon_damagezone_sprites(self):
        # TODO: Check if conditions with weapon.name
        print(self._stab_counter)
        if self._stab_counter == 0:
            x, y = self._calculate_weapon_center()
        else:
            x, y = self._calculate_weapon_center()
            dx, dy = self._calculate_stab_xy()
            x += dx
            y += dy
            self._stab_counter -= 1
        radians = math.radians(self.angle) + math.pi / 2
        if len(self._weapon_damagezone_sprites) == 1:
            for s in self._weapon_damagezone_sprites:
                s.center_x = x + (self.weapon.sprite.height // 2) * math.cos(radians)
                s.center_y = y + (self.weapon.sprite.height // 2) * math.sin(radians)
        else:
            constant_x = (self.weapon.sprite.height // 2) * math.cos(radians - math.pi / 3)
            constant_y = (self.weapon.sprite.height // 2) * math.sin(radians - math.pi / 3)
            delta_space = self.weapon.sprite.height // len(self._weapon_damagezone_sprites)
            for idx, s in enumerate(self._weapon_damagezone_sprites):
                s.center_x = x + constant_x - (delta_space * math.cos(radians - math.pi / 3)) * idx
                s.center_y = y + constant_y - (delta_space * math.sin(radians - math.pi / 3)) * idx

        return self._weapon_damagezone_sprites

    @property
    def stab_counter(self):
        """Define self.player.stab_counter."""
        return self._stab_counter

    @stab_counter.setter
    def stab_counter(self, new_value):
        self._stab_counter = new_value

    @stab_counter.getter
    def stab_counter(self):
        if self._stab_counter > 0:
            return self._stab_counter
        else:
            return 0

    def _calculate_stab_xy(self):
        # TODO: NOW DAMAGE ZONES ARE CHANGING BASED ON CHR POSITION AND ANGLE
        # TODO: MAKE IT STATIC
        # TODO: STABBING ONLY HAS TRUSTING MOTION, DRAWING THE WEAPON BACK TO ITS
        # TODO: IS NOT COVERED YET => BUT EASY TO IMPLEMENT
        # TODO: ATK SPEED IS BASED ON HOW FAST ONE CLICKS => CHANGE IT !!!!!
        cx = 10
        cy = 10
        radians = math.radians(self.angle) + math.pi / 2
        return cx * math.cos(radians) * (11 - self._stab_counter), cy * math.sin(radians) * (11 - self._stab_counter)

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

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            print("Left mouse button pressed")
            self._stab_counter = 10
            print(self._stab_counter)

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
        if self.weapon is not None:
            x, y = self._calculate_weapon_center()
            self._draw_weapon(x, y)

    def _calculate_weapon_center(self):
        radians = math.radians(self.angle)
        x = self.center_x + self.weapon.distance_to_body * math.cos(radians)
        y = self.center_y + self.weapon.distance_to_body * math.sin(radians)
        return x, y

    def _draw_weapon(self, x, y):
        self.weapon.sprite.center_x, self.weapon.sprite.center_y = x, y
        self.weapon.sprite.angle = self.angle
        self.weapon.sprite.draw()

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
