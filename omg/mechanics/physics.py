import arcade


class PhysicsEngineBoundary(arcade.PhysicsEngineSimple):
    """Physics engine to handle collisions and boundary checking."""

    def __init__(self, player_sprite, walls,
                 boundary_left, boundary_right, boundary_up, boundary_down):
        super().__init__(player_sprite, walls)
        self.boundary_left = boundary_left
        self.boundary_right = boundary_right
        self.boundary_up = boundary_up
        self.boundary_down = boundary_down

    def update(self):
        """Moves the player and resolves the collisions."""
        super().update()

        # Apply boundary checks
        self.check_boundaries()

    def check_boundaries(self):
        """Check and handle if the player sprite is outside the given boundaries."""
        if self.player_sprite.left < self.boundary_left:
            self.player_sprite.left = self.boundary_left
        elif self.player_sprite.right > self.boundary_right:
            self.player_sprite.right = self.boundary_right

        if self.player_sprite.bottom < self.boundary_down:
            self.player_sprite.bottom = self.boundary_down
        elif self.player_sprite.top > self.boundary_up:
            self.player_sprite.top = self.boundary_up
