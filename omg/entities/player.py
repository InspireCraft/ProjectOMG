import arcade
from typing import List, Type
from mechanics import movement
from entities.projectile import ProjectileFactory, Projectile
from structural.observer import Observer

MOVEMENT_SPEED_FORWARD = 1
MOVEMENT_SPEED_SIDE = 1


class ObservableSprite(arcade.Sprite):
    observers: List[Observer] = []

    def add_observer(self, observer: Observer):
        """Add an observer to the list."""
        self.observers.append(observer)

    def remove_observer(self, observer: Observer):
        """Remove an observer from the list."""
        self.observers.remove(observer)

    def notify_observers(self, event_type: str, *args, **kwargs):
        """Notify all observers of an event."""
        for observer in self.observers:
            observer.on_event(event_type, *args, **kwargs)

class Player(ObservableSprite):
    def __init__(self, name, char_class, image_file, scale, initial_angle=0):
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
            right=arcade.key.D
        )
        self.movement_logic = movement.MouseDirected(
            forward=arcade.key.W,
            backward=arcade.key.S,
            left=arcade.key.A,
            right=arcade.key.D
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

        # Projectile types
        self.projectile_types: List[Type[ProjectileFactory]] = []
        self.current_projectile_index = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        self.movement_logic.on_key_press(key, modifiers)

        if key == arcade.key.SPACE:
            self.shoot()
        elif key == arcade.key.KEY_1:
            self.select_projectile(0)
        elif key == arcade.key.KEY_2:
            self.select_projectile(1)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        self.movement_logic.on_key_release(key, modifiers)

    def update(self, mouse_x, mouse_y, delta_time):

        (self.change_x, self.change_y, self.angle) = self.movement_logic.calculate_player_state(
            self.center_x, self.center_y,
            mouse_x, mouse_y,
            self.mov_speed_lr, self.mov_speed_ud
        )
        self.regenerate_mana(delta_time)

    def shoot(self):
        if not self.projectile_types or self.current_mana < 20:
            return

        self.current_mana -= 20
        selected_skill = self.projectile_types[self.current_projectile_index]
        projectile = selected_skill.create(self.center_x, self.center_y, self.angle)
        self.notify_observers('projectile_shot', projectile)

    def regenerate_mana(self, delta_time):
        self.mana_regen_cooldown += delta_time
        if self.mana_regen_cooldown >= 1:
            self.current_mana += self.mana_regen_rate
            if self.current_mana > self.max_mana:
                self.current_mana = self.max_mana
            self.mana_regen_cooldown = 0

    # TODO: rename as skill
    def add_projectile(self, projectile: Projectile):
        self.projectile_types.append(projectile)

    def select_projectile(self, index):
        if 0 <= index < len(self.projectile_types):
            self.current_projectile_index = index

    def set_movement_keys(self, forward, backward, left, right):
        self.movement_logic.key_forward = forward
        self.movement_logic.key_backward = backward
        self.movement_logic.key_left = left
        self.movement_logic.key_right = right

    def draw(self):
        super().draw()
        self.draw_health_bar()
        self.draw_mana_bar()

    def draw_health_bar(self):
        health_bar_width = 50
        health_bar_height = 5
        health_bar_x = self.center_x
        health_bar_y = self.center_y + self.height / 2 + 10
        arcade.draw_rectangle_filled(
            health_bar_x,
            health_bar_y,
            health_bar_width,
            health_bar_height,
            arcade.color.RED
        )
        current_health_width = health_bar_width * (self.current_health / self.max_health)
        arcade.draw_rectangle_filled(
            health_bar_x - (health_bar_width - current_health_width) / 2,
            health_bar_y,
            current_health_width,
            health_bar_height,
            arcade.color.GREEN
        )

    def draw_mana_bar(self):
        mana_bar_width = 50
        mana_bar_height = 5
        mana_bar_x = self.center_x
        mana_bar_y = self.center_y + self.height / 2 + 2  # Slightly below the health bar
        arcade.draw_rectangle_filled(
            mana_bar_x,
            mana_bar_y,
            mana_bar_width,
            mana_bar_height,
            arcade.color.DARK_BLUE
        )
        current_mana_width = mana_bar_width * (self.current_mana / self.max_mana)
        arcade.draw_rectangle_filled(
            mana_bar_x - (mana_bar_width - current_mana_width) / 2,
            mana_bar_y,
            current_mana_width,
            mana_bar_height,
            arcade.color.LIGHT_BLUE
        )
