import arcade


class PhysicsEngineBoundary(arcade.PhysicsEngineSimple):
    """Physics engine to handle collisions and boundary checking."""

    def __init__(self, player_sprite, walls, screen_width, screen_height):
        super().__init__(player_sprite, walls)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        """Moves the player and resolves the collisions."""
        super().update()

        # Apply boundary checks
        self.check_boundaries()

    def check_boundaries(self):
        """Check and handle if the player sprite is outside the screen boundaries."""
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        elif self.player_sprite.right > self.screen_width:
            self.player_sprite.right = self.screen_width
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        elif self.player_sprite.top > self.screen_height:
            self.player_sprite.top = self.screen_height
