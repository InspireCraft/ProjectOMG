import unittest
from unittest.mock import MagicMock, create_autospec, patch
import arcade
from omg.mechanics.physics import PhysicsEngineBoundary

class TestPhysicsEngineBoundary(unittest.TestCase):
    def setUp(self):
        self.screen_width = 800
        self.screen_height = 600

        # Create mock player sprite and walls sprite list
        self.player_sprite = create_autospec(arcade.Sprite, instance=True)
        self.walls = create_autospec(arcade.SpriteList, instance=True)

        # Initialize the PhysicsEngineBoundary with the mock player sprite and walls
        self.physics_engine = PhysicsEngineBoundary(
            self.player_sprite,
            self.walls,
            screen_width=self.screen_width,
            screen_height=self.screen_height
        )

    def test_player_within_boundaries(self):
        # Player is within the boundaries
        self.player_sprite.left = 100
        self.player_sprite.right = 200
        self.player_sprite.bottom = 100
        self.player_sprite.top = 200

        self.physics_engine.check_boundaries()

        self.assertEqual(self.player_sprite.left, 100)
        self.assertEqual(self.player_sprite.right, 200)
        self.assertEqual(self.player_sprite.bottom, 100)
        self.assertEqual(self.player_sprite.top, 200)

    def test_player_outside_left_boundary(self):
        # Player is outside the left boundary
        self.player_sprite.left = -10
        self.player_sprite.right = 50
        self.player_sprite.bottom = 100
        self.player_sprite.top = 200

        self.physics_engine.check_boundaries()
        self.assertEqual(self.player_sprite.left, 0)
        self.assertEqual(self.player_sprite.bottom, 100)
        self.assertEqual(self.player_sprite.top, 200)

    def test_player_outside_right_boundary(self):
        # Player is outside the right boundary
        self.player_sprite.left = 750
        self.player_sprite.right = 810
        self.player_sprite.bottom = 100
        self.player_sprite.top = 200

        self.physics_engine.check_boundaries()

        self.assertEqual(self.player_sprite.right, self.screen_width)
        self.assertEqual(self.player_sprite.bottom, 100)
        self.assertEqual(self.player_sprite.top, 200)

    def test_player_outside_bottom_boundary(self):
        # Player is outside the bottom boundary
        self.player_sprite.left = 100
        self.player_sprite.right = 200
        self.player_sprite.bottom = -20
        self.player_sprite.top = 50

        self.physics_engine.check_boundaries()

        self.assertEqual(self.player_sprite.bottom, 0)
        self.assertEqual(self.player_sprite.left, 100)
        self.assertEqual(self.player_sprite.right, 200)

    def test_player_outside_top_boundary(self):
        # Player is outside the top boundary
        self.player_sprite.left = 100
        self.player_sprite.right = 200
        self.player_sprite.bottom = 550
        self.player_sprite.top = 610

        self.physics_engine.check_boundaries()

        self.assertEqual(self.player_sprite.top, self.screen_height)
        self.assertEqual(self.player_sprite.left, 100)
        self.assertEqual(self.player_sprite.right, 200)

    @patch.object(arcade.PhysicsEngineSimple, 'update', MagicMock())
    def test_update_calls_check_boundaries(self):
        # Mock the check_boundaries method and also update() method of
        # arcade.PhysicsEngineSimple
        self.physics_engine.check_boundaries = MagicMock()

        # Call update and ensure check_boundaries is called
        self.physics_engine.update()

        self.physics_engine.check_boundaries.assert_called_once()

if __name__ == "__main__":
    unittest.main()
