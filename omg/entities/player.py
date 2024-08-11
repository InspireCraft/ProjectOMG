import arcade
from typing import Generic, List, TypeVar, Type, Iterator
from omg.mechanics import movement
from omg.entities.projectile import ProjectileFactory, ProjectileShotEvent
from omg.structural.observer import ObservableSprite

MOVEMENT_SPEED_FORWARD = 1
MOVEMENT_SPEED_SIDE = 1
N_SKILLS_MAX = 5
T = TypeVar('T')  # Define a type variable


class Player(ObservableSprite):
    """Controllable player logic."""

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

        # Projectile types
        self.projectile_types: List[Type[ProjectileFactory]] = []
        self.current_projectile_index = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        self.movement_logic.on_key_press(key, modifiers)

        if key == arcade.key.SPACE:
            self.shoot()
        elif key == arcade.key.KEY_1:
            self._select_projectile(0)
        elif key == arcade.key.KEY_2:
            self._select_projectile(1)

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        self.movement_logic.on_key_release(key, modifiers)

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

    def shoot(self):
        """Shoots a projectile and informs the observes with an ProjectileShotEvent."""
        if not self.projectile_types or self.current_mana < 20:
            return

        self.current_mana -= 20
        selected_skill = self.projectile_types[self.current_projectile_index]
        projectile = selected_skill.create(
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

    # TODO: rename as skill
    def add_projectile(self, projectile: Type[ProjectileFactory]):
        """Add projectile factory to the player."""
        self.projectile_types.append(projectile)

    def _select_projectile(self, index):
        if 0 <= index < len(self.projectile_types):
            self.current_projectile_index = index

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


class CircularBuffer(Generic[T]):
    """Circular buffer to hold a determined size of items."""

    def __init__(self, max_size):
        self.buffer: List[T] = [None] * max_size  # Initialize with max size
        self.max_size = max_size
        self.current_size = 0
        self.index = 0

    def add(self, item: T):
        """Add item to the buffer. If the buffer is full, replace an item."""
        self.index = (self.index + 1) % self.max_size if self.current_size == self.max_size else self.current_size
        self.buffer[self.index] = item
        if self.current_size < self.max_size:
            self.current_size += 1

    def get_current(self) -> T:
        """Get the current item with respect to the current index."""
        if self.current_size == 0:
            return None
        return self.buffer[self.index]

    def get_current_index(self) -> int:
        """Return the current index."""
        return self.index

    def get_next(self) -> T:
        """Get next item with respect to the current index. Update the index."""
        if self.current_size == 0:
            return None
        self.index = (self.index + 1) % self.current_size
        return self.buffer[self.index]

    def get_prev(self) -> T:
        """Get previous item with respect to the current index. Update the index."""
        if self.current_size == 0:
            return None
        self.index = (self.index - 1) % self.current_size
        return self.buffer[self.index]

    def set_next(self):
        """Shift current index to the next item."""
        if self.current_size == 0:
            return
        self.index = (self.index + 1) % self.current_size

    def set_prev(self):
        """Shift current index to the previous item."""
        if self.current_size == 0:
            return
        self.index = (self.index - 1) % self.current_size

    def __iter__(self) -> Iterator[T]:
        """Iterate over the buffer from the start to the valid range."""
        start = 0
        end = self.current_size
        for i in range(start, end):
            yield self.buffer[i % self.max_size]
