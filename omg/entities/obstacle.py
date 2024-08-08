import arcade


class Obstacle(arcade.Sprite):
    """Class to represent destructable obstacles in the game."""

    def __init__(self, image_file, scale, health):
        super().__init__(image_file, scale)
        self.max_health = health
        self.current_health = health

    def take_damage(self, damage):
        """Take damage logic."""
        self.current_health -= damage
        if self.current_health <= 0:
            self.kill()

    def draw(self):
        """Draw the sprite."""
        super().draw()
        self._draw_health_bar()

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
